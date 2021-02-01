create-environment:
	conda env create --file environment.yml

update-environment:
	conda env update --file environment.yml --prune

pylint:
	pylint --rcfile=pylintrc workout/ && \
	python -m pycodestyle --max-line-length=120 workout --config pycodestyle
