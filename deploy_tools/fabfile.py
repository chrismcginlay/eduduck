# Fabfile.py based on "Test Driven Web Development with Python, H. Percival, pp 144"
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = "https://github.com/chrismcginlay/eduduck.git"
SITES_DIR = "/home/chris/sites"
env.key_file = "/home/chris/.ssh/id_rsa.pub"

def deploy():
    # env.host is not set at global scope, only within a task
    SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)
    _create_dir_tree_if_not_exists(env.host)
    _get_source(SOURCE_DIR)
    _config_nginx(env.host, SOURCE_DIR)
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
     
def _config_nginx(site_name, sdir):
    sudo("mkdir -p /etc/nginx/conf.d/{0}".format(site_name))
    
    if not exists("/etc/nginx/sites-available/{0}".format(site_name)):
        nginx_template_path = sdir + "/deploy_tools/nginx.template.conf"
        sed_cmd = "sed \"s/SITENAME/{0}/g\" {1} | tee /etc/nginx/sites-available/{0}".format(
            site_name,
            nginx_template_path
        )
        sudo(sed_cmd)
    
    if not exists("/etc/nginx/sites-enabled/{0}".format(site_name)):
        sudo ("ln -s /etc/nginx/sites-available/{0} /etc/nginx/sites-enabled/{0}".format(
            site_name
        ))

def _update_settings(site_name, sdir):
    import pdb; pdb.set_trace()
    settings_file = sdir + "/Eduduck/settings/base.py"
    secret_key_file = "/etc/nginx/conf.d/" + site_name + "/secret_key.py"
    nginx_config = "/etc/nginx/sites-enabled/" + site_name
    if not exists(secret_key_file):
        random.seed()
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.choice(charset) for i in range(69))
        append(secret_key_file, "env SECRET_KEY={0};".format(key), use_sudo=True)
    append(nginx_config, secret_key_file, use_sudo)
        
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