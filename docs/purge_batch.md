Purge Batch
==========

Perhaps you've uploaded a batch that has some incorrect information in it or you just flat out want it gone.

No problem, you can purge it.  You will need to have to get the virtual environment running.

```
cd /opt/chronam
source /opt/chronam/ENV/bin/activate
export DJANGO_SETTINGS_MODULE=chronam.settings
django-admin.py purge_batch batch_nbu_name_ver01
```

This will pull its records from mysql and the solr index.
