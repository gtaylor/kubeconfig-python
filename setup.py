from setuptools import setup, find_packages

import kubeconfig


setup(
    name="kubeconfig",
    version=kubeconfig.__version__,
    packages=find_packages(),
    install_requires=[],
    tests_require=[
        "mock",
        "pytest-cov",
        "pytest",  # this must be last due to a bug in setuptools
                   # https://github.com/pypa/setuptools/issues/196
    ],
    setup_requires=[
        "pytest-runner",
    ],
)
