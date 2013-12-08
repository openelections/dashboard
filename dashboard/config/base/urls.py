from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from dashboard.apps.hub import api

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(api.ElectionResource())
v1_api.register(api.OrganizationResource())
v1_api.register(api.StateResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^api/', include(v1_api.urls)),
)
