Load New Batch
==============

So you've gotten a new validated batch of newspapers and you want to load it into the Nebraska Newspapers project, eh?  Go ahead and mount the network drive in question on your local machine and then ssh into the newspaper server.

Check to see if there is a logical volume for the batch:

    df -h

If you do not see a volume for your batch, then follow the instructions for [adding a logical volume](./add_volume.md).

After you've added the volume, go you can make some directories.

    mkdir -p /batches/prefix_batchname/batch_prefix_name_ver01/data


Upload the Batch to the Server
---------------

Time to upload the batch to the server!  It is in your best interests to exclude tiffs, since we are using jpg2000s, but if you really like waiting you are welcome to remove the "--exclude" flag.

If you know the address of your local machine, use the following command from the server:

    rsync -azv --exclude="*.tif" username@local_machine:/path_to_network_drive/batch/ /batches/prefix_batchname/batch_prefix_name_ver01/data

If you do not know the address of your local machine, then from your computer (not the server) run this command:

    rsync -azv --exclude="*.tif" /path_to_network_drive/batch/ username@newspaper_server.unl.edu:/batches/prefix_batchname/batch_prefix_name_ver01/data

Change the permissions on the batch

    sudo chown -R apache:cdrh /batches/prefix_batchname/
    sudo chmod -R ug+rwx /batches/prefix_batchname/

Load the Batch into the Chronam App (mysql / solr)
---------------

This is when you find out if the batch is organized correctly.  This is also when you find out if python and django have been correctly set up on your server.

    cd /opt/chronam
    source /opt/chronam/ENV/bin/activate
    export DJANGO_SETTINGS_MODULE=chronam.settings
    django-admin.py load_batch /batches/prefix_batchname/batch_prefix_name_ver01

The first of the above commands starts a python virtual environment.  The second loads the settings from the settings.py file in the root of the chronam directory, and the final command starts the load process for your new batch.  It may take several hours to finish loading.  If the process fails, check the [troubleshooting](./troubleshooting.md) document for help.  You can monitor the status of your batch by finding its link at /batches/ in the Nebraska Newspaper website.

Updating the Location
---------------

We did some hardcoding of locations, since our content is not predicted to be changing very much.  Even if you don't have a unique location, you'll need to add your new paper to a few places on the site.  See [adding a location](location.md) for more information.

Does this Paper Have an Essay?
--------------

If this paper is new and should have an essay associated with it, then check out the [adding an essay](essays.md) documentation for some rad instructions.

Generating Thumbnails
--------------

Assuming that your permissions are set correctly, you should be able to view an individual page of the newspaper and receive tiles from the server.  If the images are coming back as 404s or 500s, then make sure that your permissions allow reading, writing, and execution for jp2s.

If you are using pregenerated thumbnails (if `PREGEN_THUMBNAILS` is `True` in settings.py), then you will need to run a script to create jpgs for the search results / browse views.

    cd /opt/chronam
    ./create_thumbnails /batches/prefix_batchname/

There are some settings for that script.  If you open it up, you can see that you have the choice of skipping or overwriting existing thumbnails and you can customize the size of the thumbnails.  Our default size is 360x512.

This script will effectively bring the server to its knees, as it is running the image conversion across all the cores.  If you need the website to stay live while you are pregenerating thumbnails, edit the line of the script where find pipes its results to parallel and remove `--jobs 200%`.  This should dramatically reduce the load on the server.

Even for small batches this script may take several hours to run.

NOTE:  Since we are beginning to add tiffs for each batch, you may wish to alter the script to generate thumbnails from the tiffs instead of the jp2s, which would be about 8 times faster, by our estimations.
