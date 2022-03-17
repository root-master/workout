# workout
An AI-driven Personal Training

## INSTALL CUDA

[comment]: <> (wget https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux.run)
[comment]: <> (chmod +x cuda_11.6.1_510.47.03_linux.run)
wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda_11.3.0_465.19.01_linux.run

[comment]: <> (sudo sh cuda_11.6.1_510.47.03_linux.run)
sudo sh  cuda_11.3.0_465.19.01_linux.run  --silent --override --toolkit --samples --toolkitpath=/usr/local/cuda-11.3 --samplespath=/usr/local/cuda --no-opengl-libs
sudo apt install nvidia-cuda-toolkit gcc-6
ln -s /usr/local/cuda-version /usr/local/cuda

nvcc --version

###### INSTALL VIRTUALENV
```bash
pip3 install virtualenv
```

```bash
sudo apt-get install python3.8
sudo apt-get install python3.8-dev

sudo ln -s /usr/bin/python2.7 /usr/bin/python
sudo ln -s /usr/bin/python3.8 /usr/bin/python3
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

## EC2 Issues
```bash
sudo rm /var/lib/dpkg/lock
sudo lsof /var/lib/dpkg/lock
sudo kill -9 PID

sudo dpkg --configure -a
sudo apt install
```

nvidia-installer was forced to guess the X library path '/usr/lib' and X module path '/usr/lib/xorg/modules'; these paths were not queryable from  
the system.  If X fails to find the NVIDIA X driver module, please install the `pkg-config` utility and the X.Org SDK/development package for      
your distribution and reinstall the driver. 

