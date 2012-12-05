import os
from django.contrib import admin
from django.conf import settings

from models import Contact, DataFormat, ElecData, Log, Office, Organization, State

class DataFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug':('name',)}

class ContactAdmin(admin.ModelAdmin):
    pass

class OfficeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class ContactInline(admin.StackedInline):
    #TODO: Add custom validation to ensure that at least one form
    # of contact info has been entered (phone, mobile, email_work, email_personal)
    model = Contact
    extra = 0

class OrganizationAdmin(admin.ModelAdmin):
    #TODO: Add check to ensure that if gov agency is checked, 
    #gov_level must also be selected and vice versa 
    list_display = ('name', 'state',)
    list_display_link = ('url',)
    list_filter = ('gov_level', 'gov_agency',)
    prepopulated_fields = {'slug':('name',)}
    save_on_top = True
    inlines = [
        ContactInline,
    ]

    fieldsets = (
        (None, {
            'fields':(
                ('name', 'slug',),
                ('gov_agency', 'gov_level',),
                ('url', 'fec_page',),
            ),
        }),
        ('Address', {
            'fields':('street','city','state',),
        }),
        ('Profile', {
            'description':"<p>Notes on data sources, key contacts, etc.<p>",
            'fields':('description',),
        }),
    )

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js'
        ]

class ElecDataInline(admin.StackedInline):
    #TODO:validation rule - to ensure district only filled out for special elections
    #TODO: validation rule -  If special election, enforce that Offices covered only checked for appropriate office and no others
    #TODO: js helper - Create JS copy button that lets you populate values of new inline using values of a previous inline
    #TODO: fieldsets - create fieldset that includes grouped booleans for reporting level and offices covered
    model = ElecData
    extra = 0
    filter_horizontal = ['formats']
    prepopulated_fields = {'end_date':('start_date',)}

class LogInline(admin.StackedInline):
    model = Log
    extra = 0

class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [
        ElecDataInline,
        LogInline,
    ]
    readonly_fields = ('name',)
    fieldsets = (
        (None, {
            'fields':('name', 'note',)
        }),
    )

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js'
        ]

    def save_formset(self, request, form, formset, change):
        if formset.model in (ElecData, Log):
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            formset.save_m2m()
        else:
            formset.save()

class ElecDataAdmin(admin.ModelAdmin):
    #TODO: dynamic attribute filter - create dynamic attribute that captures P/S/H/G -- ie core data -- for filter list
    #TODO: fieldsets - create fieldset that includes grouped booleans for reporting level and offices covered
    model = ElecData
    filter_horizontal = ['formats']
    list_display = ['__unicode__', 'end_date']
    list_filter = [
        'start_date',
        'race_type',
        'runoff_for',
        'special',
        'unexpired_term',
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
        'local',
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(Contact, ContactAdmin)
admin.site.register(DataFormat, DataFormatAdmin)
admin.site.register(ElecData, ElecDataAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(State, StateAdmin)
