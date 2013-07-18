Revised installation instructions for development and testing.

1. Install virtualenv =>1.9. To check the version in Ubuntu:

  $ sudo apt-get -s install python-virtualenv
  
  On Ubuntu at least, if not in general, this will also install pip. If you are satisfied with the version number for virtualenv:

  $ sudo apt-get install python-virtualenv
  
2. Check the version of pip

  $ pip --version

  It should be version =>1.3 for SSL support.

3. Install virtualenvwrapper to facilitate creation and activation of virtualenvironments.

  $ sudo pip install virtualenvwrapper

  From http://virtualenvwrapper.readthedocs.org/en/latest/:

  $ export WORKON_HOME=~/Envs
  $ mkdir -p $WORKON_HOME
  $ source /usr/local/bin/virtualenvwrapper.sh
  $ mkvirtualenv towel
 
  Append source command to .bashrc:

  $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
  
  When wishing to work on the environment 'towel' in future sessions just issue:

  $ workon towel
  
4. Within the virtualenvironment, check the Python version which should be 2.7 at present, not 3.x

  $ python --version
  
5. Install django version 1.4. WE ARE NOT READY FOR DJANGO 1.5 YET

  $ sudo pip install django==1.4
  
6. Install required packages

  $ sudo pip install django-registration pytz django-haystack

7. Next, time to get the Eduduck code and pop it onto your homedir someplace. I keep mine under a directory titled coding, but, hey, fry your own bacon dude.

  $ cd coding
  $ git clone git@github.com:mrintegrity/eduduck.git ~/coding/eduduck
  (You may of course need to add an ssh key to your github if its a new OS install)

8. Build the search index for django-haystack

If this is a staging or production install then we are using the elasticsearch backend for django-haystack, so on installation, you need to build the search index one time:
   
   $ python manage.py rebuild_index

Then add python manage.py update_index to the crontab, something like this (not tested):

   @daily PYTHONPATH=/home/username/webapps/django/lib/pythonX.Y /usr/local/bin/pythonX.Y ~/webapps/django/myproj/manage.py update_index --settings=staging

If it's just development install then django-haystack uses a simple backend and this is not required.


9. Run the development server and happy hacking

  $ cd ~/coding/eduduck
  $ python manage.py runserver



  
  
