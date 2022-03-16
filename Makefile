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
	curl https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x/138363331/model_final_997cc7.pkl -o checkpoints/model_final_997cc7.pkl

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

run_all_servers_for_flask_server:
	make run_redis_server &
	make run_features_flask_server &
	make run_celery_server


