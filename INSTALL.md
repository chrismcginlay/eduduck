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

6. Finally, time to get the Eduduck code and pop it onto your homedir someplace. I keep mine under a directory titled coding, but, hey, fry your own bacon dude.

  $ cd coding
  $ git clone git@github.com:mrintegrity/eduduck.git ~/coding/eduduck
  (You may of course need to add an ssh key to your github if its a new OS install)

7. Run the development server and happy hacking

  $ cd ~/coding/eduduck
  $ python manage.py runserver



  
  
