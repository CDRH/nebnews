Updating from the Chronam Repository
==================

Despite efforts made to allocate the majority of our changes to the nebraska directory, we did end up altering many of the core files of the LoC's application.  This means that updating in the future will be more difficult.  The below explains how and why we changed some of these files so that future maintainers may understand some of the decisions behind it.

#### urls.py

There is a little section for nebraska at the top of urls.py that will override routes further below.

#### settings.py

We added two settings to the configuration file: appending slashes and using pregenerated thumbnails

#### conf/chronam.conf

Changed Apache to serve word coordinates directly rather than using django based on advice from Oregon's project

#### core/batch_loader.py

The Plattsmouth papers have an "at" sign in their name.  I could not tell you why, but I did alter some regex in a few documents in order to allow the Plattsmouth batch titles through the filter.

#### core/context_processors.py

Changed site title to "Nebraska Newspapers"

#### core/forms.py

Hard coded min and max years for papers because it appeared that the caching was not being refreshed even after manual attempts to reset it.  Therefore, the cache is simply being ignored in this instance.

#### core/index.py

Facets altered to accept different fields (city, etc).  Some fussing with the language search was carried out because the chronam software's language search was not functional except in the case of keywords.

#### core/middleware.py

This is a "server too busy" page.  Updated to have Nebraska specific message and no image.

#### core/models.py

Title was updated to return a crude "city" property based on the publication location.

#### core/...bootstrap

Multiple stylesheets, etc, were removed from core so that the .static-media directory is not overly cluttered and to prevent some errors that were being thrown by the django command to collect the static media.  Some were altered directly.  Karin has more information about the design choices.

#### core/utils/utils.py

In order to get a "browse all papers by date" view, the calendar already being used for individual papers was coerced into working for both.  If any changes are made to `formatday`, be very careful not to break functionality on both the main calendar and the individual paper calendars.

#### core/views/image.py

The changes we made here involve using pregenerated thumbnails instead of creating new ones on the fly.

#### core/views/static.py

Changed page title to "About Nebraska Newspapers"

#### loc/ to nebraska/

The contents of loc were simply moved to nebraska, at which point much demolition and renovation was carried out.