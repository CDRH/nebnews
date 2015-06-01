Nebraska Newspapers
=======

The Nebraska Newspapers project is the University of Nebraska's
adaptation of the Library of Congress's 
[Chronicling America](http://chroniclingamerica.loc.gov) application.
This project makes historic Nebraskan newspapers available to be
viewed, browsed, and searched online.  For information about the 
contributors to the Nebraska Newspapers, please visit the [Nebraska Newspapers About Page](http://nebnewspapers.unl.edu/about/).  For more information about the
purpose and awardees of the Chronicling America project, please refer to the
[Chronicling America](http://chroniclingamerica.loc.gov/about/) website.

If you are interested in using the Chronicling America application,
we strongly recommend that you work directly from the original code base,
[https://github.com/LibraryOfCongress/chronam](https://github.com/LibraryOfCongress/chronam).
  You may also be interested in the University of Oregon's Chronicling America
rendition, [Historic Oregon Newspapers](https://github.com/uoregon-libraries/oregonnews), 
which uses a [custom image server](https://github.com/uoregon-libraries/rais-image-server).

The documentation which follows is primarily oriented toward future
maintenance and troubleshooting of the Nebraska Newspapers website.

### Documentation Contents

- [Installation](./docs/install.md)
- [Adding a Batch](./docs/new_batch.md)
- [Adding / Editing a webpage](./docs/change_page.md)
- [Configuration](./docs/config.md)
- [Adding / Editing an Essay](./docs/essays.md)
- [Adding / Editing CSS / JS](./docs/static.md)
- [Info About Locations](./docs/location.md)
- [Updating from Chronam Repo](./docs/updating.md)
- [Information About Nebraska Batches and Issues](./docs/batches.md)
- [Troubleshooting](./docs/troubleshooting.md)

### Quick Reference

To restart django

```
touch /opt/chronam/conf/chronam.wsgi
```

To get into django command mode

```
source /opt/chronam/ENV/bin/activate
export DJANGO_SETTINGS_MODULE=chronam.settings
django-admin.py  # will list commands if executed as is
```
