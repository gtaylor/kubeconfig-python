from setuptools import setup, find_packages


setup(
    name='kubeconfig',
    description='A simple wrapper around Kubernetes kubectl',
    long_description=open('README.rst').read(),
    author='Greg Taylor',
    author_email='greg@gctaylor.com',
    license='BSD',
    url='http://kubeconfig-python.readthedocs.io',
    version='1.0.1',
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
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
    ],
)
