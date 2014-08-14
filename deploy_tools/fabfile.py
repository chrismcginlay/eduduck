# Fabfile.py based on "Test Driven Web Development with Python, H. Percival, pp 144"
from fabric.contrib.files import append, exists, sed, contains
from fabric.api import env, local, run, sudo, warn
from fabric.colors import yellow, green
from fabric.operations import prompt
import random
import os, sys

REPO_URL = "https://github.com/chrismcginlay/eduduck.git"
# NB: this will require ssh keys to be registered with github account
#REPO_URL = "git@github.com:chris/eduduck.git"

# Adjust the following to suit your taste. 
SITES_DIR = "/home/chris/sites"

def provision():
    """ Install required software for EduDuck.
    
    This will install global package requirements using apt and pip.
    Note that vhost specific python packages will be installed via deploy().
    (This will be done in the _update_virtualenv function via requirements file).
    Run provision(), then deploy(), then possibly restore().
    """

    # If MySQL is already installed, skip.
    try:
        run("dpkg -s mysql-server")
    except:
        passwd = prompt('Please enter MySQL root password, leave blank for auto generated password:')
        if not passwd:
            random.seed()
            charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
            passwd = "".join(random.choice(charset) for i in range(20))
        debconf_cmd = "debconf-set-selections <<< 'mysql-server mysql-server/root_password password {0}'".format(passwd)
        sudo(debconf_cmd)
        debconf_cmd = "debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password {0}'".format(passwd)
        sudo(debconf_cmd)
        
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

    try:
        warn(yellow("NB MySQL root pw {0}".format(passwd)))
    except:
        print(green("Condition: Emerald"))


def deploy(settings):
    """ Deploy a standard configuration of EduDuck with an empty database.
    
    Use this to deploy staging or production. Not for dev.
    Run this after completing provision() to install an instance 
    of the EduDuck framework.  There will be no users, courses etc. 
    
    The tool requires that you specify the settings file to use. This will
    be one of [staging, production].
    
    Consider running restore() next.
    """
    
    # env.host is not set at global scope, only within a task
    SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)

    _create_dir_tree_if_not_exists(env.host, settings)
    _get_source(SOURCE_DIR)
    _config_nginx(env.host, SOURCE_DIR, settings)
    _update_virtualenv(SOURCE_DIR, settings)
    _prepare_environment_variables(settings, env.host)
    _write_gunicorn_upstart_script(env.host, SOURCE_DIR, settings)
    _ready_logfiles()
    _prepare_database(SOURCE_DIR, settings, env.host)
    _update_static_files(SOURCE_DIR, settings)
    _restart_services(env.host, settings)
    
def devbox():
    """ Set up a development box.

    Run this after completing provision() to install an instance of
    EduDuck, configured for development work. After this has finished,
    you can issue `python manage.py runserver` from the source directory."""

    global settings
    settings = 'dev'

    # env.host is not set at global scope, only within a task
    SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)
    
    _create_dir_tree_if_not_exists(env.host, settings)
    _get_source(SOURCE_DIR)
    _update_virtualenv(SOURCE_DIR, settings)
    _prepare_environment_variables(settings, env.host)
    _ready_logfiles()
    _prepare_database(SOURCE_DIR, settings, env.host)
 
def restore():
    """ Repopulate a deployed instance of EduDuck from backup.
    
    Use this to repopulate a userbase into your EduDuck deployment. It will 
    repopulate the database, re-instate media files such as videos etc.
    """
    
    _restore_database()
    _restore_media_files(SOURCE_DIR)


def git_update(settings):
    """ Git pull the latest code from github, then run collectstatic,  
    and restart services just in case 
    """

    # env.host is not set at global scope, only within a task
    SOURCE_DIR = "{0}/{1}/source".format(SITES_DIR, env.host)
    _get_source(SOURCE_DIR)
    _update_static_files(SOURCE_DIR, settings)
    _restart_services(env.host, settings)



# Private helper functions, don't call directly.

def _create_dir_tree_if_not_exists(site_name, settings):
    if settings=='dev':
        subdirs = ("source", "virtualenv")
    else:
        subdirs = ("static", "media", "source", "virtualenv")
    for subdir in subdirs:
        run("mkdir -p {0}/{1}/{2}".format(SITES_DIR, site_name, subdir))
        
def _get_source(sdir):
    #if git not at head, issue push warning and..
    #local("cd {0}; git push").format(SOURCE_DIR)) 
    if exists(sdir + '/.git'):
        run("cd {0}; git fetch".format(sdir))
    else:
        run("git clone {0} {1}".format(REPO_URL, sdir))
    current_commit = local(
        "cd {0}; git log -n 1 --format=%H".format(sdir), capture = True)
    run("cd {0}; git reset --hard {1}".format(sdir, current_commit))
    
    #Uncomment the following if you need to checkout and test a branch in staging.
    #run("cd {0}; git checkout NN-your_branch".format(sdir))
    run("cd {0}; git checkout master".format(sdir))    
    #run("cd {0}; git checkout 89-fabfile_db".format(sdir))
        
def _config_nginx(site_name, sdir, settings):
    if settings=='dev':
        return
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

def _write_gunicorn_upstart_script(site_name, sdir, settings):
    if settings=='dev':
        return
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
    
def _update_virtualenv(sdir, settings):
    virtualenv_dir = sdir + "/../virtualenv"
    if not exists(virtualenv_dir + "/bin/pip"): #
        run("virtualenv --python=python2.7 {0}".format(virtualenv_dir))
    run("{0}/bin/pip install -r {1}/requirements/base.txt".format(
        virtualenv_dir, sdir))
    if settings == 'dev':
        run("{0}/bin/pip install -r {1}/requirements/dev.txt".format(
            virtualenv_dir, sdir))
    if settings == 'staging':
        run("{0}/bin/pip install -r {1}/requirements/staging.txt".format(
            virtualenv_dir, sdir))
    if settings == 'production':
        run("{0}/bin/pip install -r {1}/requirements/production.txt".format(
            virtualenv_dir, sdir))
  
def _prepare_environment_variables(settings, hostname):
    """ Prepare activate to export required env vars into the virtualenv 
    
    Ideally, you will provide secrets and other environment variables in 
    the virtualenv/bin/virtualenv_envvars.txt file.
    
    However, that directory doesn't exist until you run this command. Solution
    might be to split this deploy command into two parts, allowing the user to
    create the virtualenv_envvars file.
    
    If not, we'll make it up as we go and you can clear up the mess later
    """
    
    virtenv_dir = "{0}/{1}/virtualenv/bin".format(SITES_DIR, hostname)
    virtenv_activate = virtenv_dir + '/activate'
    env_config = virtenv_dir + "/virtualenv_envvars.txt"
    
    if settings=='dev':
        # The dev SECRET_KEY doesn't need to be secret, as it's never deployed
        # In fact, it can be anything you like on each dev box.
        secret_key = '$9(8c0@dl9^0m@jautyrv&amp;y92!-ae6ymo+sl=&amp;^3ptfiw*ojt7j' 
        database_name = 'ed_dev'
        database_user = 'ed_dev'
        database_port = ''
        database_password = 'quickquackquock'
        email_host_user = 'eduduck@mailinator.com'
        email_host = 'mailinator.com'
        email_host_password = ''
        email_port = ''

    else: # Not dev!
        # First the SECRET_KEY
        random.seed()
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        secret_key = "".join(random.choice(charset) for i in range(69))

        # Database parameters.
        # Staging and production should be using seperate databases:
        random.seed()
        database_password = "".join(random.choice(charset) for i in range(69))
        database_user = 'the_{0}_duckinator'.format(settings)
        database_name = '{0}_eduduck'.format(settings)
        database_port = ''
        
        # Email parameters
        email_host_user = 'educk@unpossible.info'
        email_host = 'a2s73.a2hosting.com'
        email_host_password = 'set this after installation'
        email_port = ''

    if not contains(env_config, 'SECRET_KEY'):
        append(env_config, "SECRET_KEY={0};".format(secret_key))
    if not contains(env_config, 'DATABASE_NAME'):
        append(env_config, "DATABASE_NAME={0}".format(database_name))
    if not contains(env_config, 'DATABASE_USER'):
        append(env_config, "DATABASE_USER={0}".format(database_user))
    if not contains(env_config, 'DATABASE_PASSWORD'):
        append(env_config, "DATABASE_PASSWORD='{0}'".format(database_password))
    if not contains(env_config, 'DATABASE_PORT'):
        append(env_config, "DATABASE_PORT={0}".format(database_port))
    if not contains(env_config, 'EMAIL_HOST_USER'):
        append(env_config, "EMAIL_HOST_USER={0}".format(email_host_user))
    if not contains(env_config, 'EMAIL_HOST_PASSWORD'):
        append(env_config, "EMAIL_HOST_PASSWORD={0}".format(email_host_password))
    if not contains(env_config, "EMAIL_HOST"):
        append(env_config, "EMAIL_HOST={0}".format(email_host))
    if not contains(env_config, 'EMAIL_USE_TLS'):
        append(env_config, "EMAIL_USE_TLS=True")
    if not contains(env_config, 'EMAIL_PORT'):
        append(env_config, "EMAIL_PORT={0}".format(email_port))
    warn(yellow("Remember to set EMAIL_HOST_PASSWORD in {0}".format(env_config)))
 
    # PYTHONPATH
    append(env_config, "PYTHONPATH={0}/{1}/source".format(SITES_DIR, hostname))
    
    # Modify the virtualenv activate script, by adding an export command at the
    # end. (If the export already exists, do nothing other than warn
    if not contains(virtenv_activate, '# Pull in environment variables'):
        append(virtenv_activate, "# Pull in environment variables")
        export_cmd = "export $(cat {0})".format(env_config)
        append(virtenv_activate, export_cmd)
    else:
        warn(yellow(
            "Just note that the virtualenv/bin/activate already had some exports"))
        
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
    get_var = "source {0}; echo $DATABASE_NAME;".format(path_to_activate)
    dbname = run(get_var) 
    get_var = "source {0}; echo $DATABASE_PASSWORD;".format(path_to_activate)
    dbpass = run(get_var)
    get_var = "source {0}; echo $DATABASE_USER;".format(path_to_activate)
    dbuser = run(get_var)
    get_var = "source {0}; echo $DATABASE_NAME;".format(path_to_activate)
    dbname = run(get_var)

    # TODO
    # There is an odd thing going on here with passwords sometimes.
    # Sometimes password is not set (SHOW GRANTS FOR duckinator@localhost;) 
    # SET PASSWORD FOR 'duckinator'@'localhost' = PASSWORD('pw'); seems to work
    # but the IDENTIFIED BY bit doesn't work on my local machine.
    
    # if the database user does not exist, create it
    print(green("Does db user exist? MySQL root password"))
    out = run("mysql -u root -p -e 'select distinct User from mysql.user;'")
    if out.find(dbuser)==-1: # -1 on fail to find
        create_user_cmd = "create user {0}@localhost identified by '{1}';".format(dbuser, dbpass)
        print(green("No, user doesn't exist. MySQL root password"))
        run("mysql -u root -p -e \"" + create_user_cmd + "\"")
        
    # if database does not exist create it
    try:
        print(green("Does the db exist? MySQL root password"))
        out = run("mysql -u root -p -e 'use {0};'".format(dbname))
    except:        
        print(green("No, db doesn't exist. MySQL root password"))
        run("mysqladmin -u root -p create {0}".format(dbname))

    # Grant required privileges. Idempotent.
    perms = "SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX"
    sql = "GRANT {0} ON {1}.* TO {2}@LOCALHOST IDENTIFIED BY '{3}';".format(
        perms,
        dbname,
        dbuser,
        dbpass,
    )
    print(green("Grant db permissions: MySQL root password"))
    run("mysql -u root -p -e \"" + sql + "\"")

    sync_cmd = "source {0}/{1}/virtualenv/bin/activate; django-admin.py syncdb --settings=EduDuck.settings.{2} --noinput".format(
        SITES_DIR,
        env.host,
        settings
    )
    run(sync_cmd)
    
def _update_static_files(sdir, settings):
    if settings=='dev':
        return
    run("source {0}/{1}/virtualenv/bin/activate; django-admin.py collectstatic  --settings=EduDuck.settings.{2} --noinput".format(
        SITES_DIR,
        env.host,
        settings
    ))
    

def _restore_database():
    """ Repopulate an existing userbase into a freshly deployed EduDuck"""

    pass

def _restore_media_files():
    if settings=='dev':
        return
    """ Restore backups of user uploaded files to media server"""
    
    # not sure where these would be deployed from - some backup service?
    pass

def _restart_services(site_name, settings):
    if settings=='dev':
        return
    
    sudo("service nginx reload")
    cmd = "status gunicorn-{0}".format(site_name)
    check_nginx = sudo(cmd)
    if check_nginx.find("start/running"):
        sudo("stop gunicorn-{0}".format(site_name))
    sudo("start gunicorn-{0}".format(site_name))
