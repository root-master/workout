clean:
	rm -rf dist
	cd workout/ml/pose_estimation/ && \
	rm -rf detectron2

create_environment:
	conda env create --file environment.yml

update_environment:
	conda env update --file environment.yml --prune

activte_environment:
	source activate workout

pylint:
	pylint --rcfile=pylintrc workout && \
	python -m pycodestyle --max-line-length=120 workout --config pycodestyle

install_detectron2:
	make clean && \
	python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

install:
	make update_environment && \
	make install_detectron2 && \
	python -m pip install -e .

build_wheel:
	python setup.py bdist_wheel

build_egg:
	python setup.py bdist_egg

test:
	pytest tests/

install_gcc:
	sudo yum install gcc72 gcc72-c++

download_checkpoints:
	mkdir checkpoints && \
	cd checkpoints && \
	curl https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x/138363331/model_final_997cc7.pkl -o model_final_997cc7.pkl

build:
	make clean activte_environment pylint install build_wheel build_egg


