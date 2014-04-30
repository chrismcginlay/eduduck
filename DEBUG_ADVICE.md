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
Create an .htaccess and lock down staging.eduduck.com
Edit sites/staging.eduduck.com/source/EduDuck/settings/staging.py 
Set DEBUG to True
*Put it back afterwards - dangerous as exposes internals*