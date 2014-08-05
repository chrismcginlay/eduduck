# Debugging the Staging Server

## Services
sudo restart nginx
sudo stop gunicorn-staging.eduduck.com
sudo start gunicorn-staging.eduduck.com

## Logs
sudo zless /var/log/upstart/gunicorn-staging.eduduck.com.log
sudo tail /var/log/nginx/error.log
sudo tail /var/log/nginx/access.log

## Bad things - switching DEBUG on.

### First need to restrict access via nginx:
  openssl passwd -crypt some_password
  sudo vim /etc/nginx/conf.d/staging.eduduck.com/htpasswd
Enter chris:encrypted output from openssl command on a line by itself.
  sudo chmod 640 /etc/nginx/conf.d/staging.eduduck.com/htpasswd
  sudo chown root:www-data /etc/nginx/conf.d/staging.eduduck.com/htpasswd
  
Edit (sudo) /etc/nginx/sites-enabled/staging.eduduck.com and place two lines 
after server_name staging.eduduck.com:
    auth_basic "Temporarily restricted for debug.";
    auth_basic_user_file /etc/nginx/conf.d/staging.eduduck.com/htpasswd;
    
Restart nginx: sudo service nginx restart.
    
### Next set DEBUG True
Edit sites/staging.eduduck.com/source/EduDuck/settings/staging.py 
Set DEBUG to True
