from django.urls import include, path
from django.contrib import admin
#from tastypie.api import Api
#from dashboard.apps.hub import api
from django.conf import settings

admin.autodiscover()

#v1_api = Api(api_name='v1')
#v1_api.register(api.ElectionResource())
#v1_api.register(api.OrganizationResource())
#v1_api.register(api.StateResource())

urlpatterns = [
    path(r'grappelli/', include('grappelli.urls')),
    path(r'admin/', admin.site.urls),
#    path(r'api/', include(v1_api.urls))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
