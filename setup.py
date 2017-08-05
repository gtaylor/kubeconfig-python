from setuptools import setup, find_packages


setup(
    name='kubeconfig',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
    ],
    tests_require=[
        'mock',
        'pytest-cov',
        'pytest',  # this must be last due to a bug in setuptools
                   # https://github.com/pypa/setuptools/issues/196
    ],
    setup_requires=[
        'pytest-runner',
    ],
)
