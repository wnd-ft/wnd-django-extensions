install:
	pip install -r requirements-dev.txt

test:
	python tests/manage.py test ${TEST_FLAGS}
