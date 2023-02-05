HTML = docs/html -type f -name '*.html'
ROOT = \/docs\/html\/
DOTS = \.\.\/
DOT = \.\/

.PHONY: help boot build docs docs-fix install install-test reinstall uninstall upload upload-test test which

help:
	@echo boot
	@echo build
	@echo docs
	@echo docs-fix
	@echo install
	@echo install-test
	@echo reinstall
	@echo uninstall
	@echo upload
	@echo upload-test
	@echo which
	@echo test

boot:
	@python -m pip install --upgrade build
	@python -m pip install --upgrade twine
	@python -m pip install --upgrade numpydoc
	@python -m pip install --upgrade sphinx-rtd-theme

build:
	@rm -rf dist
	@python -m build

docs:
	@rm -rf docs/*.rst
	@rm -rf docs/doctrees
	@rm -rf docs/html
	@sphinx-apidoc -o docs --tocfile index --separate --module-first .
	@sphinx-build -M html docs docs

docs-fix:
	@find $(HTML) -exec sed -i '' 's|href="dhbw|href="$(ROOT)dhbw|g' {} \;
	@find $(HTML) -exec sed -i '' 's|href="genindex|href="$(ROOT)genindex|g' {} \;
	@find $(HTML) -exec sed -i '' 's|href="index|href="$(ROOT)index|g' {} \;
	@find $(HTML) -exec sed -i '' 's|href="py-modindex|href="$(ROOT)py-modindex|g' {} \;
	@find $(HTML) -exec sed -i '' 's|href="search|href="$(ROOT)search|g' {} \;
	@find $(HTML) -exec sed -i '' 's|href="_modules|href="$(ROOT)_modules|g' {} \;
	@find $(HTML) -exec sed -i '' 's|href="_static|href="$(ROOT)_static|g' {} \;
	@find $(HTML) -exec sed -i '' 's|src="_static|src="$(ROOT)_static|g' {} \;
	@find $(HTML) -exec sed -i '' 's|"searchindex.js"|"$(ROOT)searchindex.js"|g' {} \;
	@find $(HTML) -exec sed -i '' 's|$(DOTS)$(DOTS)$(DOTS)$(DOTS)$(DOTS)|$(ROOT)|g' {} \;
	@find $(HTML) -exec sed -i '' 's|$(DOTS)$(DOTS)$(DOTS)$(DOTS)|$(ROOT)|g' {} \;
	@find $(HTML) -exec sed -i '' 's|$(DOTS)$(DOTS)$(DOTS)|$(ROOT)|g' {} \;
	@find $(HTML) -exec sed -i '' 's|$(DOTS)$(DOTS)|$(ROOT)|g' {} \;
	@find $(HTML) -exec sed -i '' 's|$(DOTS)|$(ROOT)|g' {} \;
	@find $(HTML) -exec sed -i '' 's|"$(DOT)"|"$(ROOT)"|g' {} \;

install:
	@python -m pip install dhbw

install-test:
	@python -m pip install --index-url https://test.pypi.org/simple/ --no-deps dhbw

reinstall:
	@python -m pip uninstall -y dhbw
	@python -m pip install dhbw

uninstall:
	@python -m pip uninstall -y dhbw

upload:
	@python -m twine upload dist/*

upload-test:
	@python -m twine upload --repository testpypi dist/*

test:
	@python -m unittest discover tests

which:
	@which python
