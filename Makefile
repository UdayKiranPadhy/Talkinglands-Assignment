.PHONY: clean clean-pyc clean-build clean-test clean-all help clean-files

help:
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-test - remove test artifacts"
	@echo "clean-all - remove all build, test, and Python artifacts"

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf *.egg
	rm -rf .eggs/

clean-test:
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	rm -rf .pytest_cache/
	rm -rf coverage.xml
	rm -rf .coverage.*

clean-all: clean-pyc clean-build clean-test
	rm -rf .venv/
	rm -rf venv/

clean-files: clean-pyc clean-build clean-test
	
