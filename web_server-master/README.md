# Web Server Deployment

# Install/Configure Nginx
Nginx is the first thing that needs to be installed for the web server to start working, install it by using the command

> sudo apt-get -y install nginx

After successfully installing nginx we will need to create a directory where our web application will reside

> sudo mkdir /var/www/web_app

Give ownership permission such that the user is able to modify the files in the folder

> sudo chown -R ubuntu:ubuntu /var/www/web_app/

Configure the default file of nginx to point to the respective folder

> sudo bash -c 'cat \> /etc/nginx/sites-enabled/default  \<\<EOF
server {
    listen      80;
    server_name localhost;
    charset     utf-8;
    client_max_body_size 75M;
    location / { try_files \$uri @yourapplication; }
    location @yourapplication {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/web_app/web_app_uwsgi.sock;
    }    
}
EOF'

# Install/Configure Python Flask
> sudo apt-get -y install python3-pip

Virual Env needs to be configured

> sudo pip3 install virtualenv

> cd /var/www/web_app

> virtualenv web_app_virtual

> . web_app_virtual/bin/activate

Install the libaries by activating the virtual environment

> pip3 install flask
> pip3 install couchdb

Deactive it to exit

> deactivate

#Install Configure uwsgi

Install uwsgi so that we can link Nginx with Python Flask

> sudo pip3 install uwsgi

Setup the configuration

> sudo bash -c 'cat \>  /var/www/web_app/web_app_uwsgi.ini \<\<EOF
[uwsgi]
#application base folder
base = /var/www/web_app
\
\#python module to import
app = assignment_2
module = %(app)
\
home = %(base)/web_app_virtual
pythonpath = %(base)
\
\#socket file location
socket = /var/www/web_app/%n.sock
\
\#permissions for the socket file
chmod-socket    = 666
\
\#the variable that holds a flask application inside the module imported at line #6
callable = app
\
\#location of log files
logto = /var/log/uwsgi/%n.log
\
EOF'

Create log directory

> sudo mkdir -p /var/log/uwsgi
> sudo chmod -R +777  /var/log/uwsgi

Setup uwsgi to run at startup

> sudo bash -c 'cat \>  /etc/systemd/system/uwsgi.service \<\<EOF
[Unit]
Description=uWSGI Emperor service
After=syslog.target
\
[Service]
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all
\
[Install]
WantedBy=multi-user.target
\
EOF'

Enable uwsgi and provide permission

> sudo systemctl daemon-reload

> sudo systemctl start uwsgi

> sudo systemctl enable uwsgi

> sudo mkdir /etc/uwsgi && sudo mkdir /etc/uwsgi/vassals

> sudo ln -s /var/www/web_app/web_app_uwsgi.ini /etc/uwsgi/vassals

> sudo chown -R www-data:www-data /var/www/web_app/

> sudo chown -R www-data:www-data /var/log/uwsgi/

# Finalization

Git clone and copy the files in the folder /var/www/web_app

Restart nginx and uwsgi

> sudo service nginx restart

> sudo systemctl restart uwsgi

