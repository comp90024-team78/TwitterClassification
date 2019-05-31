#!/bin/bash
sudo apt-get -y install nginx
sudo mkdir /var/www/web_app
sudo chown -R ubuntu:ubuntu /var/www/web_app/
sudo apt-get -y install python3-pip
sudo pip3 install virtualenv
sudo bash -c 'cat > /var/www/web_app/assignment_2.py <<EOF

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
	
EOF'
cd /var/www/web_app
virtualenv web_app_virtual
. web_app_virtual/bin/activate
pip3 install flask
pip3 install couchdb
deactivate
sudo pip3 install uwsgi
sudo bash -c 'cat > /etc/nginx/sites-enabled/default  <<EOF
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

sudo bash -c 'cat >  /var/www/web_app/web_app_uwsgi.ini <<EOF
[uwsgi]
#application base folder
base = /var/www/web_app

#python module to import
app = assignment_2
module = %(app)

home = %(base)/web_app_virtual
pythonpath = %(base)

#socket file location
socket = /var/www/web_app/%n.sock

#permissions for the socket file
chmod-socket    = 666

#the variable that holds a flask application inside the module imported at line #6
callable = app

#location of log files
logto = /var/log/uwsgi/%n.log

EOF'

sudo mkdir -p /var/log/uwsgi
sudo chmod -R +777  /var/log/uwsgi
sudo bash -c 'cat >  /etc/systemd/system/uwsgi.service <<EOF
[Unit]
Description=uWSGI Emperor service
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target

EOF'

sudo service nginx restart

sudo systemctl daemon-reload
sudo systemctl start uwsgi
sudo systemctl enable uwsgi
sudo mkdir /etc/uwsgi && sudo mkdir /etc/uwsgi/vassals
sudo ln -s /var/www/web_app/web_app_uwsgi.ini /etc/uwsgi/vassals
sudo chown -R www-data:www-data /var/www/web_app/
sudo chown -R www-data:www-data /var/log/uwsgi/
