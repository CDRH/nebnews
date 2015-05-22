Add / Change a Template
=================

For the sake of familiarity, here is how Django's setup compares to Rails:

(Rails)  routes -> controller -> view (includes partials as needed)
(Django) urls -> view -> template (builds on top of / overrides existing templates)

This means if you are adding a new page, you'll need to change several files.  
If you are changing a page's contents, you will likely just need to locate the correct template, 
and try to verify that this template isn't being used by any of the other templates before you 
start changing lots of stuff.  
If you're changing an h1 or a title or something that looks like it might be coming from a variable, 
then you will need to visit the associated view.

Add a Brand New Page
----------------

To add a completely brand new page, open up urls.py.  At the top of this file, you will see 
url patterns based on `chronam.nebraska.views`, which is where you'll be adding your stuff.

```python
    url(r'^regex_pattern/$', 'view_function', name='name_of_this_route'),
```

Next, you'll need to make its friend in the view file.  Because you put your new url pattern under 
the `chronam.nebraska.views` portion, you'll open up `nebraska/views.py`.  There are several examples 
in that directory of static files that simply add a title and then point to the template to be rendered. 
Variables used in the view are passed straight to the template if you specify `dictionary=locals()` 
when rendering. 
If you need to do database calls, etc, you'll need to look at other examples lower down or checkout how 
django handles queries.

Finally, in `nebraska/templates`, add your own file to the mix.  As long as it matches the name that you 
said it would be under in `nebraska/views.py`, you should be good to go.  You'll need to include a template 
at the top of the file to overwrite.

```python
    {% extends "site_base.html" %}
```

You can then override content from `site_base.html` by including blocks by the same name as those 
in the original template.  The below line with `block.super` means you will not be overwriting the
 original, but rather appending to it.  Omit `block.super` if you only want your own thing going on.

```python
    {% block head_content %}
        {{ block.super }}
        <link href="{% static 'bootstrap/css/datepicker.css' %}" rel="stylesheet" media="screen">
    {% endblock head_content %}
```

Now you'll need to restart django.  You may want debug to be on at this point, or else you may only see a 
500 error because something is wrong in `urls.py`, etc, which won't be helpful.

    touch /opt/chronam/conf/chronam.wsgi
    
Change an Existing Page
----------------

Check out the above instructions if you are looking to change something that's like in the urls or views, 
but if all you want to do is add a bit to a template, then this is the place for you.

If you are editing a page then this template must exist somewhere.  Anything in `nebraska/templates` will 
automatically have been given preference over similar templates in `core/templates`, so check nebraska 
first.  If you find your template, edit it.  If you don't, copy the template from `core/templates` into 
`nebraska/templates`.  That way, as much of our customization as possible will be in one place.  You will 
not need to restart django if you are just changing the templates.
