from django.conf.urls import patterns, url

from chronam.nebraska.views import places

# Cannot figure out how to hook up this url pattern to
# the project's file, so for now this is not actually being used
# urlpatterns = patterns('nebraska', 
#   url(r'^places$', 'places', name="chronam_places")
# )