Deploying with SSL on Production Server
=======================================

#Requirements
* A multidomain SSL certificate capable of providing SSL for 4 domains:
    - eduduck.com
    - www.eduduck.com
    - static.eduduck.com
    - media.eduduck.com

* A certificate signing request (CSR)
* Reconfigure nginx on production server.
* Upload .key and .csr to suitable location on production server

# CSR
Generate a certificate signing request, suggest that this is done on a development box, under the deploy_tools directory. 
```
openssl req -new -newkey rsa:2048 -nodes -keyout eduduck_com.key -out eduduck_com.csr
```
Answer the questions relating to the domain name. For organisational unit, it is probably OK to just enter NA.
For the Common Name field, enter the domain name the certificate is to be generated for, i.e. eduduck.com.
If a wildcard certificate has been purchased, enter the Common Name as `*.eduduck.com
Leave the Challenge Password field blank
*NB* The .key file is to be kept securely, but must be accessible by nginx eventually. The .csr file is to be submitted when activating the certificate
Ensure the generated files don't end up under version control, from the project root folder, add these entries to .gitignore (unless they are already there):
```
echo $'deploy_tools/*.key\ndeploy_tools/*.csr\ndeploy_tools/*.crt' >> .gitignore
```

# Activate the SSL certificate.

On namecheap, for example, just paste the CSR into the correct page on their website.
*Ensure that the approver's email address is correct and accessible to you.
*Include www., media., and static. subdomains.

# Install the certificate on the production server.

Download the zip file from the certificate provider, then use scp to move it to a temporary location on the production server:
```
scp -P7822 /home/chris/Downloads/name_of_zipfile.zip chris@www.eduduck.com:/home/chris/temp/
```
Also, upload the .key file to the production server.
```
scp -P7822 deploy_tools/eduduck_com.key  chris@www.eduduck.com:/home/chris/temp/
```
Login to the production server and concatenate the various components as follows
```
cd /home/chris/temp/
cat yourfile.crt COMODORSADomainValidationSecureServerCA.crt COMODORSAAddTrustCA.crt AddTrustExternalCARoot.crt >> eduduck_cert_chain.crt
```
Copy to the production server's /etc/ssl/ directory.
```
sudo cp /home/chris/temp/eduduck_c* /etc/ssl/
sudo chmod 400 /etc/ssl/eduduck_c
```

# Nginx configuration

Logged in to the production sever via ssh, edit the file
```
sudo vim /etc/nginx/sites-enabled/www.eduduck.com
```
It should resemble:
```
server {
    listen 443 ssl;
    server_name www.eduduck.com;
    ssl_certificate /etc/ssl/eduduck_com_cert_chain.crt;
    ssl_certificate_key /etc/ssl/eduduck_com.key;
```
Restart nginx.
