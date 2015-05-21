# Create your views here.
import csv
import json
import datetime
import os

from django import forms as django_forms

from django.conf import settings
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.forms import fields

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.utils.encoding import smart_str
from django.db.models import Max, Min, Q

from chronam.core.decorator import cache_page
from chronam.core.utils.utils import _page_range_short, _rdf_base
from chronam.core import models, index
from chronam.core.rdf import titles_to_graph
from chronam.core.utils.url import unpack_url_path
from chronam.core.utils.utils import HTMLCalendar, create_crumbs


# Home
def home(request):
    # The featured content is being pulled by ajax
    return render_to_response('home.html',
                           dictionary=locals(),
                           context_instance=RequestContext(request))        

def featured(request):
    file = open(os.path.join(settings.DIRNAME, 'featured.json'))
    return HttpResponse(file, mimetype='application/json')

# Static pages with no variables, etc
def places(request):
  page_title = "Newspapers by City"
  return render_to_response('places.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))

def nebraska_publishing(request):
  page_title = "Publishing History"
  return render_to_response('nebraska_publishing.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

#Changing all headers to about -KMD
def adding(request):
  page_title = "About Nebraska Newspapers"
  return render_to_response('adding.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def nnp(request):
  page_title = "About Nebraska Newspapers"
  return render_to_response('nnp.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))
def ndnp(request):
  page_title = "About Nebraska Newspapers"
  return render_to_response('ndnp.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def access(request):
  page_title = "About Nebraska Newspapers"
  return render_to_response('access.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def contact(request):
  page_title = "About Nebraska Newspapers"
  return render_to_response('contact.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def fourohfour(request):
    page_title = "Page Not Found"
    return render_to_response('404.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))

def fivehundred(request):
    page_title = "Something is Wrong"
    return render_to_response('500.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))

# Dynamic pages

# newspapers page is not using json queries, etc.
# but the url has been left so those queries will
# hit the newspapers version in the core
@cache_page(settings.DEFAULT_TTL_SECONDS)
def newspapers(request):
    page_title = 'All Digitized Newspapers'

    titles = models.Title.objects.filter(has_issues=True)
    titles = titles.annotate(first=Min('issues__date_issued'))
    titles = titles.annotate(last=Max('issues__date_issued'))

    _newspapers_by_state = {}
    for title in titles:
        for place in title.places.all():
            if place.state:
                _newspapers_by_state.setdefault(place.state, set()).add(title)

    newspapers_by_state = [(s, sorted(t, key=lambda title: title.name_normal)) for s, t in sorted(_newspapers_by_state.iteritems())]
    crumbs = list(settings.BASE_CRUMBS)

    return render_to_response("newspapers.html",
                            dictionary=locals(),
                            context_instance=RequestContext(request))
    

@cache_page(settings.DEFAULT_TTL_SECONDS)
def calendar_issues(request, year=None):
    issues = models.Issue.objects.all().order_by('date_issued')
    if issues.count() > 0:
        if year is None:
            _year = issues[0].date_issued.year
        else:
            _year = int(year)
    else:
        _year = 1900  # no issues available
    year_view = HTMLCalendar(firstweekday=6, issues=issues, all_issues=True).formatyear(_year)
    dates = issues.dates('date_issued', 'year')

    class SelectYearForm(django_forms.Form):
        year = fields.ChoiceField(choices=((d.year, d.year) for d in dates),
                                  initial=_year)
    select_year_form = SelectYearForm()
    page_title = "Browse All Issues"
    page_name = "calendar"
    return render_to_response('calendar.html', dictionary=locals(),
                              context_instance=RequestContext(request))


