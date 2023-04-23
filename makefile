.PHONY: all setup tests dist
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

SOURCE = telemulator3
TESTS = tests
PIP = $(PYTHON) -m pip install
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
PYLINT = $(PYTHON) -m pylint
FLAKE8 = $(PYTHON) -m flake8
PEP257 = $(PYTHON) -m pep257

all: tests

test:
	$(PTEST) -s $(TESTS)/test/$(T)

tests: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

flake8:
	$(FLAKE8) $(TESTS)
	$(FLAKE8) $(SOURCE)

lint:
	$(PYLINT) $(TESTS)/test
	$(PYLINT) $(SOURCE)

pep257:
	$(PEP257) $(SOURCE)
	$(PEP257) --match='.*\.py' $(TESTS)/test

package:
	$(PYTHON) -m build -n

pypitest: package
	$(PYTHON) -m twine upload --config-file .pypirc --repository testpypi dist/*

pypi: package
	$(PYTHON) -m twine upload --config-file .pypirc dist/*

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt
	$(PIP) -r tests/requirements.txt
	$(PIP) -r deploy.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
