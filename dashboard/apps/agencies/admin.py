import os
from django.contrib import admin
from django.conf import settings

from models import Agency, DataFormat, PortalLink, ResultLink 


class DataFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug':('name',)}

class PortalLinkInline(admin.TabularInline):
    model = PortalLink 
    extra = 0
    fieldsets = (
        (None, {
            'description':"<p><p>",
            'fields':('agency', 'live_or_cert', 'url','descrip',),
        }),
    )

class ResultLinkInline(admin.StackedInline):
    model = ResultLink
    filter_horizontal = ('formats',)
    extra = 0

class AgencyAdmin(admin.ModelAdmin):
    inlines = [
        PortalLinkInline,
        ResultLinkInline,
    ]
    list_display = ('name', 'state',)
    list_display_link = ('url',)
    list_filter = ('gov_level',)
    prepopulated_fields = {'slug':('name',)}
    save_on_top = True

    fieldsets = (
        (None, {
            'fields':(
                ('name', 'slug',),
                'gov_level', 
                ('url', 'fec_page',),
            ),
        }),
        ('Address', {
            'fields':('street','city','state',),
        }),
        ('Profile', {
            'description':"<p>Notes on data sources, key contacts, history of FOIA, etc.<p>",
            'fields':('description',),
        }),
    )

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js'
        ]

admin.site.register(Agency, AgencyAdmin)
admin.site.register(DataFormat, DataFormatAdmin)
