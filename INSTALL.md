Revised Installation Instructions for EduDuck Instances
=======================================================

Most of the work required to get EduDuck up and running is now handled by an
automated provisioning and deployment tool, via fabric. http://docs.fabfile.org

This is the preferred method to set up a development or testing environment,
or for staging or production servers.

## Requirements:

    * Ubuntu 13.04. Other versions and OSs can most likely be made to work.
    * Staging and production deploys are assumed to be going on to freshly 
    installed iron or a new virtual server.
    * Root access or at least a user in sudoers group on target server.
    * SSH access to the server

1. Software on local machine

$local: pip-2.7 install fabric
$local: sudo apt-get install openssh-client
You just need to get a copy of deploy_tools/fabfile.py in your home directory.

2. Preparations of target machine

Tested on a fresh installation of Ubuntu 13.04.
Everything will be set up via the useraccount for user 'roberta' etc.

$server: sudo adduser roberta
$server: sudo usermod -a -G sudo roberta

Likely that server will already have ssh provision:
$server: sudo apt-get install openssh-server

Copy your local public SSH key from $local ~/.ssh/id_rsa.pub up to 
$server's /home/roberta/.ssh/authorized_keys

3. Server provisioning

The fabfile provision() function will install the requisite system-wide 
applications. NB: other packages will be installed into virtualenvs later.

From the deploy_tools directory, on your local machine (ssh on 7822):

$local:~/deploy_tools fab provision:host=roberta@example.com:7822

or, if this is a development box you are preparing

$local:~/deploy_tools fab provision:host=sue@localhost

If everything installed OK, proceed to deployment.

4. Instance deployment

It's super-easy to use the deploy() function now to put development, staging
and production instances of EduDuck onto the target machine. Be ready to give
github credentials, server sudo password, MySQL root as the script runs.

$local:~/deploy_tools fab deploy:host=sue@localhost, settings=dev

or 

$local:~/deploy_tools fab deploy:host=roberta@staging.example.com, settings=staging

or 

$local:~/deploy_tools fab deploy:host=roberta@example.com, settings=production

MySQL, nginx and gunicorn should be configured and services started at the end.
To test, simply visit the URL.


## Things not taken care of yet.
9. Build the search index for django-haystack

If this is a staging or production install then we are using the elasticsearch backend for django-haystack, so on installation, you need to build the search index one time:
   
   $ python manage.py rebuild_index

Then add python manage.py update_index to the crontab, something like this (not tested):

   @daily PYTHONPATH=/home/username/webapps/django/lib/pythonX.Y /usr/local/bin/pythonX.Y ~/webapps/django/myproj/manage.py update_index --settings=staging

If it's just development install then django-haystack uses a simple backend and this is not required.

10. Maybe install elasticsearch if you want to test that locally

cd ~
sudo apt-get update
sudo apt-get install openjdk-7-jre-headless -y
 
 
### Check http://www.elasticsearch.org/download/ for latest version of ElasticSearch and replace wget link below
 
# NEW WAY / EASY WAY
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.0.deb
sudo dpkg -i elasticsearch-0.90.0.deb
sudo service elasticsearch start
