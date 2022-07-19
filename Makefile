clean:
	echo "clean"

install_virtualenv:
	python3 -m pip install --user virtualenv

create_venv:
	virtualenv .penv

activate_venv:
	source .penv/bin/activate

install_requirements:
	pip3 install -r requirements.txt

install_detectron2:
	python3 -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

download_checkpoints:
	mkdir checkpoints && \
	curl https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x/138363331/model_final_997cc7.pkl -o checkpoints/model_final_997cc7.pkl && \
	curl https://dl.fbaipublicfiles.com/video-pose-3d/pretrained_h36m_detectron_coco.bin -o checkpoints/pretrained_h36m_detectron_coco.bin
build_wheel:
	python3 setup.py bdist_wheel

build_egg:
	python3 setup.py bdist_egg

build:
	make create_venv && \
	make install_requirements && \
	make install_detectron2 && \
	make download_checkpoints

install:
	pip3 install -e .

test:
	pytest tests/

pylint:
	pylint --rcfile=pylintrc features && \
	python -m pycodestyle --max-line-length=120 features --config pycodestyle

install_redis_server:
	source "./source/redis.sh"

run_redis_server:
	make install_redis_server && \
	redis-stable/src/redis-server

run_celery_server:
	source .penv/bin/activate && \
	celery -A features.server.app.celery worker --pool solo --loglevel=info

run_features_flask_server:
	source .penv/bin/activate && \
	source "./source/environment_variables.sh" && \
	flask run

run_recommendations_flask_server:
	source .penv/bin/activate && \
	source "./source/recommendations_environment_variables.sh" && \
	flask run

run_all_servers_for_flask_server:
	make run_redis_server &
	make run_features_flask_server &
	make run_celery_server


