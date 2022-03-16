# workout
An AI-driven Personal Training

## INSTALL

###### INSTALL VIRTUALENV
```bash
pip3 install virtualenv
```

###### ACTIVATE VIRTUALENV
```bash
virtualenv .penv
source .penv/bin/activate
```

####### Install REQUIREMENTS
pip3 install -r requirements.txt

####### Install DETECTRON2
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

###### INSTALL & RUN REDIS SERVER
```bash
source ./source/redis.sh
```
###### RUN REDIS SERVER
```bash
redis-stable/src/redis-server
```

###### RUN THE CELERY WORKER
```bash
celery -A features.server.app.celery worker --loglevel=info
```

###### RUN THE FLASK SERVER
```bash
export FLASK_RUN_PORT=5002
export FLASK_RUN_HOST="0.0.0.0"
export FLASK_ENV="production"
export FLASK_APP="features/server/app.py"

flask run
```

