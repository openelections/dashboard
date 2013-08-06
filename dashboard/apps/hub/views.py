from dashboard.apps.hub.models import Election
from django.http import HttpResponse
from django.utils import simplejson

def elections_for_state_and_year(request, state, year):
    response = simplejson.dumps([{'id': e.slug, 'year': year, 'start_date': e.start_date.strftime('%Y-%m-%d'), 'end_date': e.end_date.strftime('%Y-%m-%d'), 'division': e.division, 'result_type': e.result_type, 'election_type': e.race_type, 'special': e.special, 'offices': e.offices_for_api, 'reporting_levels': e.reporting_levels, 'absentee_provisional': e.absentee_and_provisional, 'note': e.level_note, 'source_url' : e.direct_link, 'portal_url' : e.portal_link} for e in Election.objects.filter(start_date__year=year, state_id=state.upper()).order_by('-start_date')])
    return HttpResponse(response, content_type="application/json")
    