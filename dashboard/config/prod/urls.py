from django.conf.urls.defaults import patterns, include, url
from dashboard.config.base.urls import urlpatterns

urlpatterns += patterns('dashboard.apps.hub.views',
    url(r'^api/v1/state/(?P<state>[a-z]+)/year/(?P<year>\d{4})/$', 'elections_for_state_and_year'),
)
