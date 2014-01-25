from dashboard.apps.hub.models import Election, State
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import simplejson
