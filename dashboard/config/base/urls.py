from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from dashboard.apps.hub import api
from dashboard.apps.hub.views import elections_for_state_and_year

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(api.ElectionResource())
v1_api.register(api.OrganizationResource())
v1_api.register(api.StateResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^api/v1/state/(?P<state>[a-z]+)/year/(?P<year>\d{4})/$', elections_for_state_and_year),
    url(r'^api/', include(v1_api.urls)),
)
