sudo rm /etc/apt/sources.list.d/cuda*
sudo apt remove --autoremove nvidia-cuda-toolkit
sudo apt remove --autoremove nvidia-*

sudo apt update
sudo apt install gcc


# Verify You Have a CUDA-Capable GPU
lspci | grep -i nvidia

# Verify You Have a Supported Version of Linux
uname -m && cat /etc/*release

# Verify the System Has gcc Installed
gcc --version

# Verify the System has the Correct Kernel Headers and Development Packages Installed
uname -r
sudo apt-get install linux-headers-$(uname -r)

# install python3.8
sudo apt-get install python3.8
sudo rm -rf /usr/bin/python3
sudo ln -s /usr/bin/python3.8 /usr/bin/python3

# install python3.8-dev
sudo apt-get install python3.8-dev

# install pip3
sudo apt-get -y install python3-pip

# install virtualenv
pip3 install virtualenv

# install CUDA 11.3
wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda_11.3.0_465.19.01_linux.run
sudo sh  cuda_11.3.0_465.19.01_linux.run  --silent --override --toolkit --samples --toolkitpath=/usr/local/cuda-11.3 --samplespath=/usr/local/cuda --no-opengl-libs

if [ -d ``/usr/local/cuda-10.1/bin/`` ]; then
 export PATH=/usr/local/cuda-11.2/bin${PATH:+:${PATH}}
 export LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
fi" >> ~/.profile

