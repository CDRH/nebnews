# Create your views here.
import csv
import json

from django.conf import settings
from django.core import urlresolvers
from django.core.urlresolvers import reverse

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

def places(request):
  return render_to_response('places.html', 
                            dictionary=locals(), 
                            context_instance=RequestContext(request))

def nebraska_publishing(request):
  return render_to_response('nebraska_publishing.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def adding(request):
  return render_to_response('adding.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def nnp(request):
  return render_to_response('nnp.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))
def ndnp(request):
  return render_to_response('ndnp.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def access(request):
  return render_to_response('access.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

def contact(request):
  return render_to_response('contact.html',
                            dictionary=locals(),
                            context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def newspapers(request, state=None, format='html'):
    if state and state != "all_states":
        state = unpack_url_path(state)
        if state is None:
            raise Http404
        else:
            state = state.title()
    else:
        state = request.REQUEST.get('state', None)
    
    language = request.REQUEST.get('language', None)
    if language:
        language_display = models.Language.objects.get(code__contains=language).name
    ethnicity = request.REQUEST.get('ethnicity', None)

    if not state and not language and not ethnicity:
        page_title = 'All Digitized Newspapers'
    else:
        page_title = 'Results: Digitized Newspapers'

    titles = models.Title.objects.filter(has_issues=True)
    titles = titles.annotate(first=Min('issues__date_issued'))
    titles = titles.annotate(last=Max('issues__date_issued'))

    if state:
        titles = titles.filter(places__state__iexact=state)

    if language:
        titles = titles.filter(languages__code__contains=language)

    if ethnicity:
        try:
            e = models.Ethnicity.objects.get(name=ethnicity)
            ethnicity_filter = Q(subjects__heading__icontains=ethnicity)
            for s in e.synonyms.all():
                ethnicity_filter |= Q(subjects__heading__icontains=s.synonym)
            titles = titles.filter(ethnicity_filter)
        except models.Ethnicity.DoesNotExist:
            pass

    _newspapers_by_state = {}
    for title in titles:
        if state:
            _newspapers_by_state.setdefault(state, set()).add(title)
        else:
            for place in title.places.all():
                if place.state:
                    _newspapers_by_state.setdefault(place.state, set()).add(title)

    newspapers_by_state = [(s, sorted(t, key=lambda title: title.name_normal)) for s, t in sorted(_newspapers_by_state.iteritems())]
    crumbs = list(settings.BASE_CRUMBS)

    if format == "html":
        return render_to_response("newspapers.html",
                                  dictionary=locals(),
                                  context_instance=RequestContext(request))
    elif format == "txt":
        host = request.get_host()
        return render_to_response("newspapers.txt",
                                  dictionary=locals(),
                                  context_instance=RequestContext(request),
                                  mimetype="text/plain")
    elif format == "csv":
        csv_header_labels = ('Persistent Link', 'State', 'Title', 'LCCN', 'OCLC', 
                             'ISSN', 'No. of Issues', 'First Issue Date', 
                             'Last Issue Date', 'More Info')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="chronam_newspapers.csv"'
        writer = csv.writer(response)
        writer.writerow(csv_header_labels)
        for state, titles in newspapers_by_state:
            for title in titles:
                writer.writerow(('http://%s%s' % (request.get_host(), 
                                                  reverse('chronam_issues', 
                                                           kwargs={'lccn': title.lccn}),),
                                 state, title, title.lccn or '', title.oclc or '',
                                 title.issn or '', title.issues.count(), title.first, 
                                 title.last, 
                                 'http://%s%s' % (request.get_host(),
                                                  reverse('chronam_title_essays',
                                                           kwargs={'lccn': title.lccn}),),))
        return response

    elif format == "json":
        host = request.get_host()
        results = {"newspapers": []}
        for state, titles in newspapers_by_state:
            for title in titles:
                results["newspapers"].append({
                    "lccn": title.lccn,
                    "title": title.display_name,
                    "url": "http://" + host + title.json_url,
                    "state": state
                })

        return HttpResponse(json.dumps(results, indent=2), mimetype='application/json')
    else:
        return HttpResponseServerError("unsupported format: %s" % format)