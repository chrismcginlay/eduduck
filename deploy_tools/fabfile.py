# Fabfile.py based on "Test Driven Web Development with Python, H. Percival, pp 144"
from fabric.contrib.files import append, exists, sed, contains
from fabric.api import env, local, run, sudo
import random
import os, sys

REPO_URL = "https://github.com/chrismcginlay/eduduck.git"
SITES_DIR = "/home/chris/sites"

def provision():
    """ Install required software for EduDuck.
    
    This will install global package requirements using apt and pip.
    Note that vhost specific python packages will be installed via deploy().
    Run provision(), then deploy(), then possibly restore().
    """
    
    apt_packages = [
        'python-virtualenv',
        'python-pip',
        'mysql-server',
        'libmysqlclient-dev',
        'python-dev',
        'nginx',
        'git',
    ]

    pip_packages = [
        'virtualenvwrapper',
    ]
    
    apt_cmd = "apt-get install -y " + " ".join([pkg for pkg in apt_packages])
    sudo(apt_cmd)

    pip_cmd = "pip install " + " ".join([pkg for pkg in pip_packages])
    sudo(pip_cmd)
    
def deploy(settings):
    """ Deploy a standard configuration of EduDuck with an empty database.
    
    Run this after completing provision() to install an instance 
    of the EduDuck framework.  There will be no users, courses etc. 
    
    The tool requires that you specify the settings file to use. This will
    be one of [dev, staging, production].
    
    Consider running restore() next.
    """
    
    # env.host is not set at global scope, only within a task
    SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)
    #TODO verify following is redundant
    #sys.path.append("{0}/{1}/".format(SITES_DIR, env.host))

    _create_dir_tree_if_not_exists(env.host)
    _get_source(SOURCE_DIR)
    _config_nginx(env.host, SOURCE_DIR)
    _update_virtualenv(SOURCE_DIR)
    _prepare_environment_variables(env.host)
    _write_gunicorn_upstart_script(env.host, SOURCE_DIR)
    _ready_logfiles()
    _prepare_database(SOURCE_DIR, settings, env.host)
    _update_static_files(SOURCE_DIR, settings)
    _restart_services(env.host)
    
def restore():
    """ Repopulate a deployed instance of EduDuck from backup.
    
    Use this to repopulate a userbase into your EduDuck deployment. It will 
    repopulate the database, re-instate media files such as videos etc.
    """
    
    _restore_database()
    _restore_media_files(SOURCE_DIR)



# Private helper functions, don't call directly.

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

    gunicorn_template_head = sdir + "/deploy_tools/gunicorn_upstart.head.template"
    gunicorn_template_tail = sdir + "/deploy_tools/gunicorn_upstart.tail.template"
    gunicorn_template_mid  = sdir + "/deploy_tools/gunicorn_upstart.mid.template"
    gunicorn_template_done = sdir + "/deploy_tools/gunicorn_upstart.template"
    gunicorn_config_path = "/etc/init/gunicorn-{0}.conf".format(site_name)
    env_var_path = sdir + "/../virtualenv/bin/virtualenv_envvars.txt"

    #prepend env to each line of env_var_path > gunicorn_template_mid
    sed_cmd = "awk '$0=\"env \"$0' {0} > {1}".format(
        env_var_path, 
        gunicorn_template_mid)
    run(sed_cmd)

    #join the head, mid and tail
    sudo("cat {0} > {1}".format(gunicorn_template_head, gunicorn_template_done))
    sudo("cat {0} >> {1}".format(gunicorn_template_mid, gunicorn_template_done))
    sudo("cat {0} >> {1}".format(gunicorn_template_tail, gunicorn_template_done))
    
    #NB this sed sources the freshly written config, not the template
    sed_cmd = "sed \"s/SITENAME/{0}/g\" {1} | tee {2}"
    sed_cmd = sed_cmd.format(site_name, gunicorn_template_done, gunicorn_config_path)
    sudo(sed_cmd)
    
def _update_virtualenv(sdir):
    virtualenv_dir = sdir + "/../virtualenv"
    if not exists(virtualenv_dir + "/bin/pip"): #
        run("virtualenv --python=python2.7 {0}".format(virtualenv_dir))
        run("{0}/bin/pip install -r {1}/requirements/base.txt".format(
            virtualenv_dir, sdir))
        
def _prepare_environment_variables(hostname):
    """ Prepare activate to export required env vars into the virtualenv """

    virtenv_dir = "{0}/{1}/virtualenv/bin".format(SITES_DIR, hostname)
    virtenv_activate = virtenv_dir + '/activate'
    env_config = virtenv_dir + "/virtualenv_envvars.txt"
    
    # First the SECRET_KEY
    if not contains(env_config, 'SECRET_KEY'):
        random.seed()
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.choice(charset) for i in range(69))
        append(env_config, "SECRET_KEY={0};".format(key))
        
    # DB PARAMS
    if not contains(env_config, 'DATABASE_NAME'):
        append(env_config, "DATABASE_NAME=eduduck")
    if not contains(env_config, 'DATABASE_USER'):
        append(env_config, "DATABASE_USER=duckinator")
    if not contains(env_config, 'DATABASE_PASSWORD'):
        append(env_config, "DATABASE_PASSWORD=AB0XAt5BgDJh")
    if not contains(env_config, 'DATABASE_PORT'):
        append(env_config, "DATABASE_PORT=")
    
    # EMAIL PARAMS
    if not contains(env_config, 'EMAIL_HOST_USER'):
        append(env_config, "EMAIL_HOST_USER=educk@unpossible.info")
    if not contains(env_config, 'EMAIL_PASSWORD'):
        append(env_config, "EMAIL_PASSWORD=tobespecified")
    if not contains(env_config, 'EMAIL_PORT'):
        append(env_config, "EMAIL_PORT=25")
    
    # PYTHONPATH
    append(env_config, "PYTHONPATH={0}/{1}/source".format(SITES_DIR, hostname))
    
    # Modify the virtualenv activate script, by adding an export command at the
    # end. (If the export already exists, do nothing.
    if not contains(virtenv_activate, '# Pull in environment variables'):
        append(virtenv_activate, "# Pull in environment variables")
        export_cmd = "export $(cat {0})".format(env_config)
        append(virtenv_activate, export_cmd)
    
def _ready_logfiles():
    sudo("touch /var/log/eduduck.log")
    sudo("touch /var/log/eduduck_db.log")
    sudo("chown "+env.user+" /var/log/eduduck.log")
    sudo("chown "+env.user+" /var/log/eduduck_db.log")
    sudo("chmod 700 /var/log/eduduck.log")
    sudo("chmod 700 /var/log/eduduck_db.log")
    
def _prepare_database(sdir, settings, hostname):

    # load environment variables
    path_to_activate = "{0}/{1}/virtualenv/bin/activate".format(SITES_DIR, hostname)
    dbname = "eduduck"
    get_var = "source {0}; echo $DATABASE_PASSWORD;".format(path_to_activate)
    dbpass = run(get_var)
    get_var = "source {0}; echo $DATABASE_USER;".format(path_to_activate)
    dbuser = run(get_var)
    get_var = "source {0}; echo $DATABASE_NAME;".format(path_to_activate)
    dbname = run(get_var)

    # if database does not exist create it
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
    
def _update_static_files(sdir, settings):
    run("source {0}/{1}/virtualenv/bin/activate; django-admin.py collectstatic  --settings=EduDuck.settings.{2} --noinput".format(
        SITES_DIR,
        env.host,
        settings
    ))
    

def _restore_database():
    """ Repopulate an existing userbase into a freshly deployed EduDuck"""

    pass

def _restore_media_files():
    """ Restore backups of user uploaded files to media server"""
    
    # not sure where these would be deployed from - some backup service?
    pass

def _restart_services(site_name):
    """ Restart nginx and gunicorn etc"""
    
    sudo("service nginx reload")
    cmd = "status gunicorn-{0}".format(site_name)
    check_nginx = sudo(cmd)
    if not check_nginx.find("start/running"):
        sudo("start gunicorn-{0}".format(site_name))
