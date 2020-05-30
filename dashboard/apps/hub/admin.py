from decimal import Decimal

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from localflavor.us.us_states import US_STATES
from django.db import connection
from django.utils.translation import ugettext_lazy as _

from .models import (
#    Contact,
    DataFormat,
    Election,
    Log,
    Office,
    Organization,
    State,
    Volunteer,
    VolunteerLog,
    VolunteerRole
)


### number helpers
ONEPLACE = Decimal(10) ** -1

### FIELDSET ###
ELECTION_FIELDSET = (
    ('Data Source', {
        'fields': ('organization', 'portal_link', 'direct_links', 'result_type', 'formats'),
        'classes': ('grp-collapse grp-closed',),
    }),
    ('Election Meta', {
        'fields': ('state', ('start_date', 'end_date'), 'race_type', 'special', 'primary_type', 'primary_note', 'absentee_and_provisional'),
        'classes': ('grp-collapse grp-closed',),
    }),
    ('Offices Covered', {
        'description': 'Data for this source includes results for:',
        'fields': (
            ('prez', 'senate', 'house', 'gov',),
            ('state_officers', 'state_leg',),
        ),
        'classes': ('grp-collapse grp-closed',),
    }),
    ('Results Availability', {
        'description': 'Availability/status of data at various reporting levels:',
        'fields': (
            'state_level_status', 'county_level_status', 'precinct_level_status',
            'cong_dist_level_status', 'state_leg_level_status',
        ),
        'classes': ('grp-collapse grp-closed',),
    }),
    ('Results Breakdowns', {
        'description': 'The level at which results are broken down. Racewide is the common case and denotes the widest jurisdiction '
                       'or reporting level at which data are available. In the case of presidential, senate or gubernatorial races, '
                      '"Racewide" implies statewide; in the case of U.S. House races, "Racewide" implies district-wide results.<br><br>'
                      'The Congressional District and State Legislative boxes should only be flagged when there are result breakdowns '
                      'at those levels for unrelated offices. In other words, flag the Congressional District box if there are results for the '
                      'presidential race at the congressional district level. Do NOT check the box to denote results for a U.S. House race '
                      '(these should be denoted with the "Racewide" checkbox).',
        'fields': (
            ('state_level', 'county_level', 'precinct_level'),
            ('cong_dist_level', 'state_leg_level',),
            'level_note'
        ),
        'classes': ('grp-collapse grp-closed',),
    }),
    ('Notes', {
        'fields': ('proofed_by', 'note', 'needs_review'),
        'classes': ('grp-collapse grp-closed',),
    }),
)

VOLUNTEER_FIELDSET = (
    (None, {
        'fields': ('user', 'volunteer', 'date', 'subject', 'follow_up', 'gdoc_link', 'notes'),
    }),
)

### ADMIN CLASSES ###


class DataFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


#class ContactAdmin(admin.ModelAdmin):
#    pass


class OfficeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


#class ContactInline(admin.StackedInline):
    # TODO: Add custom validation to ensure that at least one form of contact
    # info has been entered (phone, mobile, email_work, email_personal)
#    model = Contact
#    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    #TODO: Add check to ensure that if gov agency is checked,
    # gov_level must also be selected and vice versa
    list_display = ('name', 'state',)
    list_display_link = ('url',)
    list_filter = ('gov_level', 'gov_agency',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    inlines = [
        #ContactInline,
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'slug',),
                ('gov_agency', 'gov_level',),
                ('url', 'fec_page',),
            ),
        }),
        ('Address', {
            'fields': ('street', 'city', 'state',),
        }),
        ('Profile', {
            'description': "<p>Notes on data sources, key contacts, etc.<p>",
            'fields': ('description',),
        }),
    )


class ElectionInline(admin.StackedInline):
    model = Election
    template = "grappelli/admin/edit_inline/stacked.html"
    extra = 0
    prepopulated_fields = {
        'end_date': ('start_date',)
    }
    fieldsets = ELECTION_FIELDSET

    def queryset(self, request):
        return super(ElectionInline, self).queryset(request).prefetch_related('formats')

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ElectionInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in set(['organization', 'formats']):
            # Force queryset evaluation and cache in .choices
            formfield.choices = formfield.choices
        return formfield

class LogInline(admin.StackedInline):
    model = Log
    extra = 0


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'state_volunteers', 'percent_proofed', 'metadata_status', 'pain']
    list_filter = ['metadata_status', 'pain']
    list_editable = ['metadata_status', 'pain']
    inlines = [
        ElectionInline,
        LogInline,
    ]
    readonly_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'metadata_status', 'pain', 'note', 'results_description')
        }),
    )

    class Media:
        js = ('admin/js/custom_datepicker.js',)


    def save_formset(self, request, form, formset, change):
        if formset.model == Election:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            formset.save_m2m()
        else:
            formset.save()

    def state_volunteers(self, obj):
        return ", ".join([vol.full_name for vol in obj.volunteer_set.all()])
    state_volunteers.short_description = "Volunteers assigned to each state"

    def percent_proofed(self, obj):
        sql = '''select (
                    cast(sum(case when proofed_by_id is not null then 1 end) as decimal)/count(*)
                   )*100
                from hub_election
                where state_id = %s;'''

        ### Create single db cursor for raw queries
        cursor = connection.cursor()
        cursor.execute(sql, [obj.postal])
        # Assume zero
        value = cursor.fetchone()[0]
        try:
            pct = value.quantize(ONEPLACE).to_eng_string()
        except AttributeError:
        # States with zero records return None value
            pct = "0"
        # Generic trap for all other error types, to avoid breaking admin
        except:
            pct = "Could not be determined."
        return pct
    percent_proofed.short_description = "% of election records proofed"


class ElectionNeedsReviewListFilter(admin.SimpleListFilter):
    title = _('Needs review')
    parameter_name = 'needs_review'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'No':
            return queryset.filter(needs_review=u'')
        if self.value() == 'Yes':
            return queryset.exclude(needs_review=u'')


class ElectionProofedListFilter(admin.SimpleListFilter):
    title = _('Proofed')
    parameter_name = 'proofed'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'No':
            return queryset.filter(proofed_by__isnull=True)
        if self.value() == 'Yes':
            return queryset.filter(proofed_by__isnull=False)


class ElectionAdmin(admin.ModelAdmin):
    model = Election
    filter_horizontal = ['formats']
    list_display = [
        'id',
        'state',
        'start_date',
        'end_date',
        'race_type',
        'primary_type',
        'special',
        'offices',
        'user_fullname',
        'proofed_by',
        'state_level_status',
        'county_level_status',
        'precinct_level_status',
        'cong_dist_level_status',
        'state_leg_level_status',
    ]
    list_display_links = ['id']
    save_on_top = True
    list_filter = [
        ElectionNeedsReviewListFilter,
        ElectionProofedListFilter,
        'proofed_by',
        'user_fullname',
        'start_date',
        'race_type',
        'primary_type',
        'special',
        'state',
        'result_type',
        'state_level',
        'county_level',
        'precinct_level',
        'prez',
        'senate',
        'house',
        'gov',
        'state_officers',
        'state_leg',
    ]
    list_editable = [
        'proofed_by',
        'state_level_status',
        'county_level_status',
        'precinct_level_status',
        'cong_dist_level_status',
        'state_leg_level_status',
    ]
    fieldsets = ELECTION_FIELDSET

    class Media:
        js = ('admin/js/custom_datepicker.js',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.user_fullname = "%s, %s" % (obj.user.last_name, obj.user.first_name)
        obj.save()

    def offices(self, obj):
        return ', '.join(obj.offices)
    offices.short_description = "Office(s) up for election"


class VolunteerLogInline(admin.StackedInline):
    model = VolunteerLog
    extra = 0
    fieldsets = VOLUNTEER_FIELDSET


class VolunteersByStateFilter(SimpleListFilter):
    title = _('States')
    parameter_name = 'states'

    def lookups(self, request, model_amdin):
        return US_STATES

    def queryset(self, request, queryset):
        val = self.value()
        if not val or val.lower() == 'all':
            return queryset.all()
        if val in set([state[0] for state in US_STATES]):
            return queryset.filter(states=val)


#TODO: Create data_admin dynamic filter based on presence of value in
# User field (to indicate if volunteer has admin privs)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'assigned_states',
        'attended_sprint',
        'last_emailed',
        'note_snippet',
    )
    list_display_links = ('last_name',)
    list_editable = ('attended_sprint', 'last_emailed',)
    list_select_related = True
    list_filter = (
        VolunteersByStateFilter,
        'attended_sprint',
        'last_emailed',
    )
    inlines = [VolunteerLogInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'middle_name', 'last_name', 'affil', 'title'),
        }),
        ('Contact Info', {
            'fields': ('phone', 'mobile', 'email', 'website', 'twitter', 'skype'),
        }),
        ('Activity', {
            'fields': ('roles', 'states', 'attended_sprint', 'last_emailed', 'note'),
        }),
    )

    def assigned_states(self, obj):
        return ", ".join(obj.states.values_list('postal', flat=True))
    assigned_states.short_description = "States covered by this volunteer"

    def note_snippet(self, obj):
        return obj.note.split('\n')[0]
    note_snippet.short_description = "First line of the Note field"


class VolunteerLogAdmin(admin.ModelAdmin):
    fieldsets = VOLUNTEER_FIELDSET


class VolunteerRoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

#admin.site.register(Contact, ContactAdmin)
admin.site.register(DataFormat, DataFormatAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(VolunteerLog, VolunteerLogAdmin)
admin.site.register(VolunteerRole, VolunteerRoleAdmin)
