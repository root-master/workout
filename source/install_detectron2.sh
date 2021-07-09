# see https://medium.com/@bh.parsa/installing-detectron2-on-an-aws-ec2-instance-9cc1910d425f
# see https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md

sudo rm /etc/apt/sources.list.d/cuda*
sudo apt remove --autoremove nvidia-cuda-toolkit
sudo apt remove --autoremove nvidia-*

sudo apt update
sudo add-apt-repository ppa:graphics-drivers
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list'
sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda_learn.list'

sudo apt update
sudo apt install cuda-10.1
sudo apt install libcudnn7

# sudo nano ~/.profile
sudo echo "# set PATH for cuda 10.1 installation
if [ -d “/usr/local/cuda-10.1/bin/” ]; then
 export PATH=/usr/local/cuda-10.1/bin${PATH:+:${PATH}}
 export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
fi" >> ~/.profile

conda create --name detectron2 python=3.7
conda activate detectron2
conda update libgcc

pip install pyyaml==5.1
pip install pycocotools>=2.0.1
pip install opencv-python==4.1.2.30
conda install pytorch torchvision torchaudio cudatoolkit=10.1 -c pytorch
python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.8/index.html
