# Fabfile.py based on "Test Driven Web Development with Python, H. Percival, pp 144"
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random
import os, sys

REPO_URL = "https://github.com/chrismcginlay/eduduck.git"
SITES_DIR = "/home/chris/sites"

env.user = 'chris'
# local public key
env.key_filename = "/home/chris/.ssh/id_rsa.pub"

def provision():
    """ Install required software for EduDuck """
    
    apt_packages = [
        'python-virtualenv',
        'python-pip',
        'mysql-server',
        'libmysqlclient-dev',
        'python-dev',
        'python-mysqldb',
        'nginx',
        'git'
    ]

    pip_packages = [
        'virtualenvwrapper'
    ]
    
    apt_cmd = "apt-get install -y " + " ".join([pkg for pkg in apt_packages])
    sudo(apt_cmd)

    pip_cmd = "pip install " + " ".join([pkg for pkg in pip_packages])
    sudo(pip_cmd)
    
def deploy(settings):
    # env.host is not set at global scope, only within a task
    SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)
    sys.path.append("{0}/{1}/".format(SITES_DIR, env.host))

    #_create_dir_tree_if_not_exists(env.host)
    #_get_source(SOURCE_DIR)
    #_config_nginx(env.host, SOURCE_DIR)
    _write_gunicorn_upstart_script(env.host, SOURCE_DIR)
    _update_settings(env.host, SOURCE_DIR)
    #_update_virtualenv(SOURCE_DIR)
    #_ready_logfiles()
    _prepare_database(SOURCE_DIR, settings)
    _update_static_files(SOURCE_DIR)
    _update_media_files(SOURCE_DIR)
    
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
    
    #TODO delete the following on issue 83 close
    run("cd {0}; git checkout 83-auto_deploy".format(sdir))
     
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

def _write_gunicorn_upstart_script(site_name, sdir):
    import pdb; pdb.set_trace()
    gunicorn_template_path = sdir + "/deploy_tools/gunicorn_upstart.template"
    sed_cmd = "sed \"s/SITENAME/{0}/g\" {1} | tee /etc/init/gunicorn-{0}"
    sed_cmd = sed_cmd.format(site_name, gunicorn_template_path)
    sudo(sed_cmd)

def _update_settings(site_name, sdir):
    settings_file = sdir + "/EduDuck/settings/base.py"
    secret_key_file = "/etc/nginx/conf.d/" + site_name + "/secret_key.py"
    nginx_config = "/etc/nginx/sites-enabled/" + site_name
    if not exists(secret_key_file):
        random.seed()
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.choice(charset) for i in range(69))
        append(secret_key_file, "env SECRET_KEY={0};".format(key), use_sudo=True)
    append(nginx_config, secret_key_file, use_sudo=True)
    
def _update_virtualenv(sdir):
    virtualenv_dir = sdir + "/../virtualenv"
    if not exists(virtualenv_dir + "/bin/pip"): #
        run("virtualenv --python=python2.7 {0}".format(virtualenv_dir))
        run("{0}/bin/pip install -r {1}/requirements/base.txt".format(
            virtualenv_dir, sdir))
        
def _ready_logfiles():
    sudo("touch /var/log/eduduck.log")
    sudo("touch /var/log/eduduck_db.log")
    sudo("chown "+env.user+" /var/log/eduduck.log")
    sudo("chown "+env.user+" /var/log/eduduck_db.log")
    sudo("chmod 700 /var/log/eduduck.log")
    sudo("chmod 700 /var/log/eduduck_db.log")
    
def _prepare_database(sdir, settings):
    # if database does not exist create it
    #TODO utilise same environment vars setup as for production and staging
    dbname = "eduduck"
    dbuser = "duckinator"
    dbpass = "AB0XAt5BgDJh"
    try:
        out = run("mysqlshow -u root -p {0}".format(dbname))
    except:
        run("mysqladmin -u root -p create {0}".format(dbname))
        perms = "SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX"
        sql = "\"GRANT {0} ON {1}.* TO {2}@LOCALHOST IDENTIFIED BY '{3}';\"".format(
            perms,
            dbname,
            dbuser,
            dbpass,
        )
        run("mysql -u root -p -e " + sql)

    sync_cmd = "source {0}/{1}/virtualenv/bin/activate; django-admin.py syncdb --settings=EduDuck.settings.{2} --noinput".format(
        SITES_DIR,
        env.host,
        settings
    )
    run(sync_cmd)
    
def _update_static_files(sdir):
    run("cd {0}/{1}/virtualenv/bin/; django-admin.py collectstatic --setttings=EduDuck.settings.{2} --noinput".format(
        SITES_DIR,
        env.host,
        settings
    ))
    

def _update_media_files():
    # not sure where these would be deployed from - some backup service?
    pass