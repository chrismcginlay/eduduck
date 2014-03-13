# Fabfile.py based on "Test Driven Web Development with Python, H. Percival, pp 144"
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/chrismcginlay/eduduck.git"
SITES_DIR = "/home/chris/sites"
SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)

def deploy():
    _create_dir_tree_if_not_exists(env.host)
    _get_source()
    _update_settings(env.host)
    _prepare_database()
    _update_virtualenv()
    _update_static()
    _update_media()
    
def _create_dir_tree_if_not_exists(site_name):
    for subdir in ("static", "media", "source", "virtualenv"):
        run("mkdir -p {0}/{1}/{2}".format(SITES_DIR, site_name, subdir))
        
def _get_source():
    #if git not at head, issue push warning and..
    #local("cd {0}; git push").format(SOURCE_DIR)) 
    if exists(SOURCE_DIR + '/.git'):
        run("cd {0}; git fetch".format(SOURCE_DIR))
    else:
        run("git clone {0} {1}".format(REPO_URL, SOURCE_DIR))
    current_commit = local("git log -n 1 --format=%H", capture = True)
    run("cd {0}; git reset --hard {1}".format(SOURCE_DIR, current_commit))
     
def _update_settings(site_name):
    settings_file = SOURCE_DIR + "Eduduck/settings/base.py"
    secret_key_file = "/etc/nginx/sites-available/" + SOURCE_DIR + "/secret_key.py"
    nginx_config = "/etc/nginx/sites-enabled/" + site_name
        if not exists(secret_key_file):
            random.seed()
            charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
            key = "".join(random.choice(charset) for i in range(69))
            append(secret_key_file, "env SECRET_KEY={0};".format(key))
        append(nginx_config, secret_key_file)
        
def _prepare_database():
    # if database does not exist create it
    # otherwise just syncdb
    
def _update_virtualenv():
    virtualenv_dir = SOURCE_DIR + "/../virtualenv"
    if not exists(virtualenv_dir + "/bin/pip"): #
        run("virtualenv --python=python2.7 {0}".format(virtualenv_dir))
    run("{0}/bin/pip install -r {1}/requirements/base.txt".format(
        virtualenv_dir, source_dir))
    
def _update_static_files():
    run("cd {0}; ../virtualenv/bin/python3 manage.py collectstatic --noinput".format(SOURCE_DIR))
    

def _update_media():
    # not sure where these would be deployed from - some backup service?
    pass