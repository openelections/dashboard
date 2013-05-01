from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.localflavor.us.us_states import US_STATES
from django.utils.translation import ugettext_lazy as _

from models import (
    Contact,
    DataFormat,
    Election,
    Log,
    Office,
    Organization,
    Party,
    State,
    Volunteer,
    VolunteerLog,
    VolunteerRole
)

### FIELDSET ###
ELECTION_FIELDSET = (
    ('Data Source', {
        'fields': ('organization', 'portal_link', 'direct_link', 'result_type', 'formats'),
        'classes': ('grp-collapse grp-closed',),
    }),
    ('Election Meta', {
        'fields': ('state', ('start_date', 'end_date'), 'race_type', 'primary_type', 'primary_party', 'absentee_and_provisional'),
        'classes': ('grp-collapse grp-closed',),
    }),
    ('Special Election', {
        'description': """Special elections are edge cases that we itemize. <br>If this is a special,
                          check the box and fill in the office. If it's a House race, include the District number
                          as an integer or 'AL' for At-Large.""",
        'fields': (('special', 'office', 'district'),),
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
        'fields': ('note',),
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


class ContactAdmin(admin.ModelAdmin):
    pass


class OfficeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ContactInline(admin.StackedInline):
    # TODO: Add custom validation to ensure that at least one form of contact
    # info has been entered (phone, mobile, email_work, email_personal)
    model = Contact
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    #TODO: Add check to ensure that if gov agency is checked,
    # gov_level must also be selected and vice versa
    list_display = ('name', 'state',)
    list_display_link = ('url',)
    list_filter = ('gov_level', 'gov_agency',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    inlines = [
        ContactInline,
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
    #TODO: validation rule - ensure district only filled out for special elections
    #TODO: validation rule - If special election, enforce that Offices covered only checked for appropriate office and no others
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
        if db_field.name in set(['office', 'organization', 'formats']):
            # Force queryset evaluation and cache in .choices
            formfield.choices = formfield.choices
        return formfield

class LogInline(admin.StackedInline):
    model = Log
    extra = 0


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'state_volunteers']
    inlines = [
        ElectionInline,
        LogInline,
    ]
    readonly_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'note',)
        }),
    )

    class Media:
        js = ('admin/js/custom_datepicker.js',)


    def save_formset(self, request, form, formset, change):
        if formset.model in (Election, Log):
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


class ElectionAdmin(admin.ModelAdmin):
    model = Election
    filter_horizontal = ['formats']
    list_display = ['id', 'state', 'start_date', 'end_date', 'race_type', 'primary_type', 'primary_party', 'special', 'offices']
    list_display_links = ['id']
    save_on_top = True
    list_filter = [
        'start_date',
        'race_type',
        'primary_type',
        'primary_party',
        'special',
        'office',
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
    fieldsets = ELECTION_FIELDSET

    class Media:
        js = ('admin/js/custom_datepicker.js',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def offices(self, obj):
        if obj.special:
            return obj.special_key(as_string=True)
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
        'email',
        'twitter',
        'phone',
        'mobile'
    )
    list_display_links = ('last_name',)
    list_select_related = True
    list_filter = (VolunteersByStateFilter,)
    inlines = [VolunteerLogInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'middle_name', 'last_name', 'affil', 'title'),
        }),
        ('Contact Info', {
            'fields': ('phone', 'mobile', 'email', 'website', 'twitter', 'skype'),
        }),
        (None, {
            'fields': ('roles', 'states', 'note',),
        }),
    )

    def assigned_states(self, obj):
        return ", ".join(obj.states.values_list('postal', flat=True))
    assigned_states.short_description = "States covered by this volunteer"


class VolunteerLogAdmin(admin.ModelAdmin):
    fieldsets = VOLUNTEER_FIELDSET


class VolunteerRoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Contact, ContactAdmin)
admin.site.register(DataFormat, DataFormatAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(VolunteerLog, VolunteerLogAdmin)
admin.site.register(VolunteerRole, VolunteerRoleAdmin)
