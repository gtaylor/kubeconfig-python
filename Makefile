.PHONY: tests tidy clean

tests:
	py.test

tidy: tests
	pep8 kubeconfig tests
	pyflakes kubeconfig tests
	pep257 kubeconfig
	pylint kubeconfig

clean:
	rm -rf build/
	rm -rf tests/htmlcov/
