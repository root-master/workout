# workout Vision Features App
An AI-driven Personal Training App


### Build
###### INSTALL VIRTUALENV
In MAC OS
```bash
pip3 install virtualenv
```

In LINUX
```bash
sudo apt-get install python3.8
sudo apt-get install python3.8-dev

sudo ln -s /usr/bin/python2.7 /usr/bin/python
sudo ln -s /usr/bin/python3.8 /usr/bin/python3
python3 -m pip install virtualenv
sudo apt install virtualenv python3-virtualenv
```

###### ACTIVATE VIRTUALENV
```bash
virtualenv .penv -p python3
source .penv/bin/activate
```

###### Install REQUIREMENTS
```bash
source .penv/bin/activate
pip3 install -r requirements.txt
```

###### Install DETECTRON2
```bash
source .penv/bin/activate
python3 -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

###### Install repo
```bash
pip3 install -e .
```

###### INSTALL REDIS SERVER
```bash
source .penv/bin/activate
source ./source/redis.sh
```

### Deploy

###### RUN REDIS SERVER
```bash
source .penv/bin/activate
redis-stable/src/redis-server
```

###### RUN THE CELERY WORKER
```bash
source .penv/bin/activate
celery -A features.server.app.celery worker --loglevel=info
```

###### RUN THE FLASK SERVER
```bash
source .penv/bin/activate
export FLASK_RUN_PORT=8080
export FLASK_RUN_HOST="0.0.0.0"
export FLASK_ENV="production"
export FLASK_APP="features/server/app.py"

flask run
```

###### RUN THE FLASK SERVER using gunicorn
```bash
gunicorn features.server.app:flask_app
```

### HTTPS on EC2
1. deploy flask on ec2
2. allocate an elastic IP
3. Route 53: route ml.workout.vision to elastic IP 
4. In Google Domains, Create DNS NS ml.workout.vision to amazon nameservers in Route 53 
https://medium.com/@samuel.ngigi/deploying-python-flask-to-aws-and-installing-ssl-1216b41f8511
5. Setup Nginx to proxy 80 to 8000
6. Use Certbot to magically create SSL and HTTPS
###### nginx
```
sudo rm /etc/nginx/sites-enabled/default 
sudo rm /etc/nginx/sites-available/default
sudo touch /etc/nginx/sites-available/ml.workout.vision
sudo chown -R $USER:$USER /etc/nginx/sites-available/ml.workout.vision
```

Add this to /etc/nginx/sites-available/ml.workout.vision
```
server {
listen 80;
location / {
proxy_pass http://127.0.0.1:8000/;
}
}
```

```
sudo ln -f -s /etc/nginx/sites-available/ml.workout.vision /etc/nginx/sites-enabled/ml.workout.vision
sudo service nginx restart
```

###### certbot
https://certbot.eff.org/instructions?ws=nginx&os=ubuntubionic
```
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx
```