Configuration
================

During the setup, you will copy the `settings_template.py` file to `settings.py`.  For the most part, you can leave the settings alone, but there are a few things you may wish to change.

#### DEBUG

When set to True, you will see stacktraces instead of 404 / 500 pages and caching of static files will be turned off.  There are a few other side effects that you can find throughout where the code is looking to see if DEBUG is set or not.  When false, the opposite is true.  For the live site, DEBUG is set to False.

#### APPEND_SLASH

We added this to the django template and it means that if somebody types in `nebnewspapers.unl.edu/places` that django will be able to find the route for `^places/$` despite the trailing slash.

#### DATABASES

The database connection info is stored in here.  If you are experiencing database difficulty, check with Jason to see if anything has been altered recently.

#### USE_TIFF

If you want to use tiffs, set this to True.  If you prefer to use jp2000s, use False

#### PREGEN_THUMBNAILS

This is a custom setting that Nebraska is using.  If you want to rely on on-the-fly thumbnail generation, feel free to set it to False.  However, as our thumbnails are currently being pregenerated, we have set this to True.

#### SOLR_LANGUAGES

We changed these to be only English and Czech, but it is possible that it will be necessary to add them in the future, also.  If you do, you will need to check that those languages are in the solr schema / config itself, and in a few dropdowns around the site.