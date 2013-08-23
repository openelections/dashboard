from dashboard.apps.hub.models import Election, State
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import simplejson

def elections_for_state_and_year(request, state, year):
    st = get_object_or_404(State, postal=state.upper())
    if int(year) < 2000:
        raise Http404
    else:
        elections = Election.objects.filter(start_date__year=year, state_id=st.postal).order_by('-start_date')
        if len(elections) > 0:
            details = [{'id': e.slug, 'start_date': e.start_date.strftime('%Y-%m-%d'), 'end_date': e.end_date.strftime('%Y-%m-%d'), 'result_type': e.result_type, 'election_type': e.race_type, 'special': e.special, 'offices': e.offices_for_api, 'reporting_levels': e.reporting_levels, 'absentee_provisional': e.absentee_and_provisional, 'note': e.level_note, 'source_url' : e.direct_link, 'portal_url' : e.portal_link} for e in elections ]
            return HttpResponse(simplejson.dumps({'division': elections[0].division, 'state': st.postal, 'year': year, 'elections': details}), content_type="application/json")
        else:
            raise Http404
        
