create-environment:
	conda env create --file environment.yml

update-environment:
	conda env update --file environment.yml --prune

pylint:
	pylint --rcfile=pylintrc workout && \
	python -m pycodestyle --max-line-length=120 workout --config pycodestyle

install_detectron2:
	cd workout/ml/pose_estimation/ && \
	rm -rf detectron2 && \
	git clone https://github.com/facebookresearch/detectron2.git && \
	python -m pip install -e detectron2

install:
	conda env update --file environment.yml --prune && \
	make install_detectron2 && \
	python -m pip install -e .

wheel:
	python setup.py bdist_wheel
