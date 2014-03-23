Provisioning Notes
==================

nginx
Python 2.7
git
pip
virtualenv

Manually
========
Add user (eg chris)
usermod -a -G sudo chris
Copy id_rsa.pub from dev box to .ssh/authorized_keys on target host
Grab deploy_tools/fabfile.py from the github repo.
Run the provisioning routine: 
	$ fab provision:host=chris@staging.eduduck.com:7822
