SHELL := /bin/bash

.PHONY: tests tidy docs clean

tests:
	py.test

tidy: tests
	pep8 kubeconfig tests
	pyflakes kubeconfig tests
	pep257 kubeconfig
	pylint kubeconfig

docs:
	pushd docs && make html && popd

clean:
	rm -rf build/
	rm -rf tests/htmlcov/
