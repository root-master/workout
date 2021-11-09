clean:
	echo "clean"

create_environment:
	conda env create --file environment.yml

update_environment:
	conda env update --file environment.yml --prune

activte_environment:
	conda activate workout

install_torch_cpu:
	conda install pytorch torchvision torchaudio -c pytorch

install_torch_gpu:
	conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch

install_detectron2:
	python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

download_checkpoints:
	mkdir checkpoints && \
	cd checkpoints && \
	curl https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x/138363331/model_final_997cc7.pkl -o model_final_997cc7.pkl

install_cpu:
	make update_environment && \
	make install_torch_cpu && \
	make install_detectron2 && \
	make download_checkpoints

install_gpu:
	make update_environment && \
	make install_torch_gpu && \
	make install_detectron2 && \
	make download_checkpoints

build_wheel:
	python setup.py bdist_wheel

build_egg:
	python setup.py bdist_egg

test:
	pytest tests/

pylint:
	pylint --rcfile=pylintrc features && \
	python -m pycodestyle --max-line-length=120 features --config pycodestyle

build_cpu:
	make clean pylint install_cpu build_wheel build_egg

build_gpu:
	make clean pylint install_gpu build_wheel build_egg
