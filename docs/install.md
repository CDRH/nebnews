Install Nebraska Newspapers
==============

The following instructions are for Centos 6.  The Library of Congres's [chronam](https://github.com/LibraryOfCongress/chronam/blob/master/install_ubuntu.md) project contains instructions for installing on Ubuntu.

Enable Extra Packages if necessary:

    sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

Install system dependencies:

    sudo yum install mysql-server mysql-devel httpd python-virtualenv gcc libxml2-devel libxslt-devel libjpeg-devel zlib-devel mod_wsgi java-1.6.0-openjdk-devel git

When you install mysql-server, you will be prompted for a root password. If
you choose one, make a note of what it is. Later you will be asked to enter
the password when you create the database for the project.

Get chronam
-----------

    sudo mkdir /opt/chronam
    sudo chown $USER:users /opt/chronam
    git clone https://github.com/CDRH/nebnews.git /opt/chronam

Configure Solr
--------------

Download solr from a mirror site (instructions use solr 4. Solr 5 would likely work if you spend the time getting it hooked up)

    wget http://archive.apache.org/dist/lucene/solr/4.4.0/solr-4.4.0.tgz
    tar zxvf solr-4.4.0.tgz
    sudo mv solr-4.4.0/example/ /opt/solr/
    sudo cp /opt/chronam/conf/schema.xml /opt/solr/solr/collection1/conf/schema.xml
    sudo cp /opt/chronam/conf/solrconfig.xml /opt/solr/solr/collection1/conf/solrconfig.xml

Update the dataDir field in /opt/solr/solr/conf/solrconfig.xml and
point to a directory for where the solr index will live.

    sudo useradd -d /opt/solr -s /bin/bash solr
    sudo chown solr:solr -R /opt/solr

    sudo cp /opt/chronam/conf/jetty7.sh /etc/init.d/jetty
    sudo chmod +x /etc/init.d/jetty

The jetty-redhat config file contains a default heap space allocation- "-Xms2g -Xmx2g".  Change the 2g 
to a sensible default for your system if 2g is too much or too little.

    sudo cp /opt/chronam/conf/jetty-redhat /etc/default/jetty
    sudo cp /opt/chronam/conf/jetty-logging.xml /opt/solr/etc/jetty-logging.xml

    sudo service jetty start

Configure Image Rendering:
--------------------------

If you have the Aware JPEG 2000 library this is how you install it:

    wget --no-check-certificate --http-user your-username --http-password your-password https://svn.rdc.lctl.gov/svn/ndnp/third-party/j2k-3.18.9-linux-x86-64.tar.gz
    tar -zxvf j2k-3.18.9-linux-x86-64.tar.gz
    sudo cp j2k-3.18.9-linux-x86-64/include/* /usr/local/include/
    sudo cp j2k-3.18.9-linux-x86-64/lib/libawj2k.so.2.0.1 /usr/local/lib/
    sudo ln -s /usr/local/lib/libawj2k.so.2.0.1 /usr/local/lib/libawj2k.so
    sudo echo "/usr/local/lib" > /etc/ld.so.conf.d/aware.so.conf
    sudo ldconfig /usr/local/lib/

If not, install GraphicsMagick.  GraphicsMagick is what the Nebraska Newspapers is using.

    sudo yum install GraphicsMagick

Configure Apache
----------------

    sudo cp /opt/chronam/conf/chronam.conf /etc/httpd/conf.d/chronam.conf
    sudo install -o `whoami` -g users -d /opt/chronam/static
    sudo install -o `whoami` -g users -d /opt/chronam/.python-eggs

Update the KeepAlive directive in /etc/httpd/conf/httpd.conf config from 'Off' 
to 'On'. If you are the Library of Congress you will also want to canonicalize 
URLs that used by the Chronicling America application at the Library of Congress:

    sudo cp /opt/chronam/conf/chronam-canonical.conf /etc/httpd/conf.d/

More Dependencies
----------------

After you have installed the system level dependencies you will need to 
install some application specific dependencies, and configure the application.

First you will need to set up the local Python environment and install some
Python dependencies:

    cd /opt/chronam/
    virtualenv ENV
    source /opt/chronam/ENV/bin/activate
    cp conf/chronam.pth ENV/lib/python2.6/site-packages/chronam.pth

(There is another small difference here between RedHat and Ubuntu, you may need to change the 2.6 above to a 2.7)

    pip install -U distribute
    pip install -r requirements.pip

Next you need to create some directories for data:

    mkdir /opt/chronam/data/batches
    mkdir /opt/chronam/data/cache
    mkdir /opt/chronam/data/bib

And you will need a MySQL database. If this is a new server, you will need to
start MySQL and assign it a root password:

    sudo service mysqld start
    /usr/bin/mysqladmin -u root password '' # pick a real password
    
You will probably want to change the password 'pick_one' in the example below
to something else:

    echo "DROP DATABASE IF EXISTS chronam; CREATE DATABASE chronam CHARACTER SET utf8; GRANT ALL ON chronam.* to 'chronam'@'localhost' identified by 'pick_one'; GRANT ALL ON test_chronam.* TO 'chronam'@'localhost' identified by 'pick_one';" | mysql -u root -p

You will need to use the settings template to create your application settings.
Add your database password to the settings.py file:

    cp /opt/chronam/settings_template.py /opt/chronam/settings.py

For Django management commands to work you will need to have the
DJANGO_SETTINGS_MODULE environment variable set. You may want to add 
this to your ~/.profile so you do not need to remember to do it 
everytime you log in.

    export DJANGO_SETTINGS_MODULE=chronam.settings


Next you will need to initialize database schema and load some initial data:

    django-admin.py syncdb --noinput --migrate
    django-admin.py chronam_sync --skip-essays

And finally you will need to collect static files (stylesheets, images) 
for serving up by Apache in production settings:

    django-admin.py collectstatic --noinput

Load Data
--------

As mentioned above, the NDNP data that awardees create and ship to the Library
of Congress is in the public domain and is made available on the Web as 
`batches`. Each batch contains newsaper issues for one or more newspaper 
titles. To use chronam you will need to have some of this batch data to load. If
you are an awardee you probably have this data on hand already, but if not
you can use a tool like [wget](http://www.gnu.org/software/wget/) to bulk 
download the batches. For example:

    cd /opt/chronam/data/
    wget --recursive --no-host-directories --cut-dirs 1 --reject index.html* --include-directories /data/batches/batch_uuml_thys_ver01/ http://chroniclingamerica.loc.gov/data/batches/batch_uuml_thys_ver01/

In order to load data you will need to run the load_batch management command by
passing it the full path to the batch directory. So assuming you have downloaded
batch_dlc_jamaica_ver01 you will want to:

    django-admin.py load_batch /opt/chronam/data/batches/batch_uuml_thys_ver01

If this is a new server, you may need to start the web server:

    sudo service httpd start

After this completes you should be able to view the batch in the batches report
via the Web:

    http://www.example.org/batches/

Run Unit Tests
--------------

For the unit tests to work you will need to have the batch_dlc_jamaica_ver01
available. You can use the wget command in the previous section to get get it.
After that you should be able to:

    cd /opt/chronam/
    django-admin.py test core

