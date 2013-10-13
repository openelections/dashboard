from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from dashboard.apps.hub.models import Election, State, Organization


class OrganizationResource(ModelResource):

    class Meta:
        queryset = Organization.objects.all()
        allowed_methods = ['get']
        include_resource_ur = False
        excludes = ['description']
        filtering = {
            'name': ['exact', 'iexact'],
            'slug': ['exact', 'iexact'],
            'gov_level': ['exact', 'iexact'],
            'state': ['exact', 'iexact'],
        }


class StateResource(ModelResource):

    class Meta:
        queryset = State.objects.all()
        allowed_methods = ['get']
        include_resource_ur = False
        fields = ['postal', 'name']
        filtering = {
            'name': ALL,
            'postal': ['iexact', 'exact'],
        }


class ElectionResource(ModelResource):

    organization = fields.ForeignKey(OrganizationResource,'organization', full=True)
    state = fields.ForeignKey(StateResource, 'state', full=True)

    class Meta:
        queryset = Election.objects.all()
        allowed_methods = ['get']
        excludes = [
            'created',
            'modified',
            'user',
            'level_note',
            'note',
            'needs_review',
        ]
        filtering = {
            'state': ALL_WITH_RELATIONS,
            'organization': ALL_WITH_RELATIONS,
            'race_type': ALL,
            'start_date': ALL,
            'end_date': ALL,
        }
