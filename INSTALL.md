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
  
4. Within the virtualenvironment, check the Python version which should be 2.7 at present, not 3.x
  $ python --version
  
5. 
  
  
