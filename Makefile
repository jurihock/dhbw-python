BASEURL = \/docs\/html\/

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
	@rm -rf docs/doctrees
	@rm -rf docs/html
	@sphinx-apidoc -o docs --tocfile index --separate --force .
	@sphinx-build -M html docs docs
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/data-url_root=".\/"/data-url_root="$(BASEURL)"/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/href="dhbw/href="$(BASEURL)dhbw/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/href="genindex/href="$(BASEURL)genindex/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/href="index/href="$(BASEURL)index/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/href="py-modindex/href="$(BASEURL)py-modindex/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/href="search/href="$(BASEURL)search/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/href="_static/href="$(BASEURL)_static/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/src="_static/src="$(BASEURL)_static/g' {} \;
	@find docs/html -type f -name '*.html' -exec sed -i '' 's/"searchindex.js"/"$(BASEURL)searchindex.js"/g' {} \;

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
