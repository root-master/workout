# workout
An AI-driven Personal Training

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

####### Install REQUIREMENTS
```bash
source .penv/bin/activate
pip3 install -r requirements.txt
```

####### Install DETECTRON2
```bash
source .penv/bin/activate
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

###### INSTALL REDIS SERVER
```bash
source .penv/bin/activate
source ./source/redis.sh
```

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
