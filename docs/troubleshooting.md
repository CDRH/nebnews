Troubleshooting
===============

Server Responding with 503 / Server Errors
--------------

CHECK JETTY.  Is it running?  Can you curl localhost:8983/solr?  Try restarting jetty first off.

BLAME SELINUX.  If you restarted the server, there's a good chance that SELinux is trying to reinstate its tyrannical rule over serverland.  `setenforce 0` will temporarily get you back into a beautiful permissive environment

APACHE LOGS.  You can get more detailed  information about the errors and traffic in /var/log/httpd.  When did requests start failing?

MYSQL.  Is it running?  Can django see it?

PERMISSIONS.  It's possible that there is some permission issue going on, but hopefully unlikely.  Check that apache / mod_wsgi are operating okay and that 

Permission Denied When Uploading to Server
--------------

You'll need to make sure that the directory where you are uploading the batch files allows you writing permissions.  Verify that you are in the `cdrh` group.

    sudo chown -R apache:cdrh /batches/batch_name/
    sudo chmod -R ug+rwx /batches/batch_name/
    
Marc Error when Loading Batch
-------------

This means that the lccn for the batch does not match any lccns that the Library of Congress recognizes.  
Chalk it up to a typo and be glad that you didn't accidentally get the marc data for a completely
unrelated batch from Ohio or elsewhere!

You're going to need to find the correct lccn for the **paper** version of the paper (even if this one happens to be from microfilm).  Ask Laura for help or [search the Library of Congress](http://chroniclingamerica.loc.gov/search/titles/).  
Once you have located it, change the name of the directory with the incorrect lccn to the correct one.  You will need to
run a find and replace for every instance of the incorrect lccn, including in the batch.xml files in the base 
of the batch directory.  Try rerunning your batch again and hope for the best!

Other Errors When Loading Batches
--------------

Check the following:
- Is your solr index behind a firewall?
- Does your batch.xml correctly describe the directories / files in your batch?
- Are your mysql credentials in settings.py correct?

I Changed Stuff But It's Not Showing Up
--------------

Try restarting Django

    touch /opt/chronam/conf/chronam.wsgi

If Debugging is off in `settings.py` then it is possible that the django cache has not refreshed

Did you try refreshing your browser without a cache?

I changed some CSS or JavaScript and It Isn't Working
-------------
You need to rerun the script that manages static files.  See [the static files documentation](./static.md) for more information.
