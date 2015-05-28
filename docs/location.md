Adding a New Location
==================

Since our content is not apt to change frequently, we have hardcoded in city information in several places.  When you add a paper, you will need to make sure that not only is the city being searched by solr represented in the search dropdown, but that your publication is added to the map.

site.html
-------------

If you have a brand new city, you will need to add it to the dropdown "All Cities" in `nebraska/templates/site.html`.  You'll need to check the solr index to make sure that the value of the option matches the solr field.  Ask Karin or Jessica if you need this information or for instructions on how to access the solr web interface directly.

places.html
---------------

Regardless of whether or not your city is new, you'll need to add it to `nebraska/templates/places.html`.  Get the lccn for your new publication and open the file.  There is some json (stored directly in that file for the time being) where you will need to add your location to the appropriate city or add a new location using the others as an example.

```
{
  "name": "Bellevue City",
  "latlong": [41.16, -95.93],
  "papers": {
    "Nebraska Palladium": "sn84020241",
    "Bellevue Gazette": "sn85033100"
  }
},
```

Now your paper should show up on the historic map at the top of the screen.  You'll need to make sure that you add it to the div rows below the map so that users with javaScript disabled will be able to browse by location.

Historic Overlay
===================

The historic overlay of Nebraska is being hosted on the rosie geoserver.  There is a backup on spacely should anything happen to rosie, since that is a non-production server.  However, if the geoserver is unavailable, the historic overlay will simply not be displayed, but the underlying map will be present.  There will be many errors in the console because of the failing tiling of the historic layer, but the map will remain functional.