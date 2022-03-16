clean:
	echo "clean"

create_environment:
	conda env create --file environment.yml

update_environment:
	conda env update --file environment.yml --prune

activte_environment:
	conda activate detectron2

install_torch_cpu:
	# conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 -c pytorch
	 pip3 install torch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0

install_torch_gpu:
	# conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
	pip3 install torch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0

install_detectron2:
	python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

download_checkpoints:
	mkdir checkpoints && \
	cd checkpoints && \
	curl https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x/138363331/model_final_997cc7.pkl -o model_final_997cc7.pkl
build_wheel:
	python setup.py bdist_wheel

build_egg:
	python setup.py bdist_egg

install:
	pip install -e .

install_cpu:
	make update_environment && \
	make install_torch_cpu && \
	make install_detectron2 && \
	make download_checkpoints

install_gpu:
	make update_environment && \
	make install_torch_gpu && \
	make install_detectron2 && \
	make download_checkpoints && \
	make install

test:
	pytest tests/

pylint:
	pylint --rcfile=pylintrc features && \
	python -m pycodestyle --max-line-length=120 features --config pycodestyle

build_cpu:
	make clean pylint install_cpu build_wheel build_egg

build_gpu:
	make clean pylint install_gpu build_wheel build_egg

.EXPORT_ALL_VARIABLES:
	export FLASK_RUN_PORT=5002 && \
	export FLASK_RUN_HOST="0.0.0.0" && \
	export FLASK_ENV="production" && \
	export FLASK_APP="features/server/app.py"

run_redis_server:
	source "./source/redis.sh"

run_celery_server:
	celery -A features.server.app.celery worker --loglevel=info

run_features_flask_server:
	flask run

run_all:
	make run_redis_server &
	make run_features_flask_server &
	make run_celery_server


