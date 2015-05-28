Changing / Adding CSS / JS
=================

The chronam software comes with both a static file manager and a caching helper.  When the `settings.py` file is set with `DEBUG = False` then both will be used.  If you have that flag set to True, then the cacher will not operate in order to help the developer / designer tinkering with static files like js and css.

The ideal workflow is as follows.  We are, unfortunately, not using it.  See the next section for more information about our version.

Adding a Static File (the Traditional Way)
----------------

Let's say you want to add a CSS file.  Stick it in `nebraska/static`.  In your template, you would include it like this:

```python
{% extends "something.html" %}
{% load static from staticfiles %}

{% block head_content %}
  {{ block.super }}
  <link href="{% static 'awesome.css' %}" />

```

Now you are going to need to run a command that will collect you new static file and add it to a section of the repository accessible by Apache.

```
source /opt/chronam/ENV/bin/activate
export DJANGO_SETTINGS_MODULE=chronam.settings
django-admin.py collectstatic
```

That will ask you if you are sure and if you are reasonably sure that you haven't removed any static files that would be important, then go ahead and okay it.  If it errors out, check that all the static files required by things like bootstrap are actually there and that the permissions on files all seem okay, etc.

Now your page should be displaying with your new css.

Adding a Static File (the Less Traditional Way)
-----------------

Though the static file caching is operational (django is requesting things like awesome.min.37184931.css and similarly named files exist in .static_media), the numbers do not match and so none of the stylesheets, javascript, or site images like arrows are showing up.  As a quick fix, we are simply linking to files with relative paths.

```
<link type="text/css" rel="stylesheet" href="/media/jquery-ui.css" />
```

Apache is looking for requests to /media/ in the .static-media directory, so as long as a file by that name exists there, it should be good to go.  This type of path will not work if you are running the application under a sub-uri.