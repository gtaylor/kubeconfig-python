from setuptools import setup, find_packages


setup(
    name='kubeconfig',
    description='A simple wrapper around Kubernetes kubectl',
    long_description=open('README.rst').read(),
    author='Greg Taylor',
    author_email='greg@gctaylor.com',
    license='BSD',
    url='http://kubeconfig-python.readthedocs.io',
    version='1.1.2',
    packages=find_packages(),
    install_requires=[
        'PyYAML>=5.2',
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
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
    ],
)
