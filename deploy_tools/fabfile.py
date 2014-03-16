# Fabfile.py based on "Test Driven Web Development with Python, H. Percival, pp 144"
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/chrismcginlay/eduduck.git"
SITES_DIR = "/home/chris/sites"

def deploy():
    # env.host is not set at global scope, only within a task
    SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)
    _create_dir_tree_if_not_exists(env.host)
    _get_source(SOURCE_DIR)
    _provision_nginx()
    _update_settings(env.host, SOURCE_DIR)
    _prepare_database()
    _update_virtualenv(SOURCE_DIR)
    _update_static(SOURCE_DIR)
    _update_media(SOURCE_DIR)
    
def _create_dir_tree_if_not_exists(site_name):
    for subdir in ("static", "media", "source", "virtualenv"):
        run("mkdir -p {0}/{1}/{2}".format(SITES_DIR, site_name, subdir))
        
def _get_source(sdir):
    #if git not at head, issue push warning and..
    #local("cd {0}; git push").format(SOURCE_DIR)) 
    if exists(sdir + '/.git'):
        run("cd {0}; git fetch".format(sdir))
    else:
        run("git clone {0} {1}".format(REPO_URL, sdir))
    current_commit = local("git log -n 1 --format=%H", capture = True)
    run("cd {0}; git reset --hard {1}".format(sdir, current_commit))
     
def _provision_nginx():
    if not exists("/etc/nginx/sites-available/{0}".format(site_name):
        #sed "s/SITENAME/superlists.ottg.eu/g" deploy_tools/nginx.template.conf | \
        #     sudo tee /etc/nginx/sites-available/superlists.ottg.eu
    
    #sudo ln -s ../sites-available/superlists.ottg.eu \
    #    /etc/nginx/sites-enabled/superlists.ottg.eu
    pass

def _update_settings(site_name, sdir):
    import pdb; pdb.set_trace()
    settings_file = sdir + "/Eduduck/settings/base.py"
    secret_key_file = "/etc/nginx/sites-available/" + site_name + "/secret_key.py"
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
    pass
    
def _update_virtualenv(sdir):
    virtualenv_dir = sdir + "/../virtualenv"
    if not exists(virtualenv_dir + "/bin/pip"): #
        run("virtualenv --python=python2.7 {0}".format(virtualenv_dir))
    run("{0}/bin/pip install -r {1}/requirements/base.txt".format(
        virtualenv_dir, sdir))
    
def _update_static_files(sdir):
    run("cd {0}; ../virtualenv/bin/python3 manage.py collectstatic --noinput".format(sdir))
    

def _update_media():
    # not sure where these would be deployed from - some backup service?
    pass