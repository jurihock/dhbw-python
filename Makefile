.PHONY: help boot build docs install install-test reinstall uninstall upload upload-test which

help:
	@echo boot build docs install install-test reinstall uninstall upload upload-test which

boot:
	@python -m pip install --upgrade build
	@python -m pip install --upgrade twine

build:
	@rm -rf dist
	@python -m build

docs:
	@rm -rf docs/*.rst
	@sphinx-apidoc -o docs --tocfile index --separate --force .
	@sphinx-build -M html docs docs

install:
	@pip install dhbw

install-test:
	@python -m pip install --index-url https://test.pypi.org/simple/ --no-deps dhbw

reinstall:
	@pip uninstall -y dhbw
	@pip install dhbw

uninstall:
	@pip uninstall -y dhbw

upload:
	@python -m twine upload dist/*

upload-test:
	@python -m twine upload --repository testpypi dist/*

which:
	@which python
