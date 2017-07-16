Installing kubeconfig
=====================

Prerequesites
-------------

.. warning:: This module currently requires Python 3.5 or greater. While
    we will likely make changes to knock this back to 3.4, there is no desire
    to add or maintain Python 2 compatibility.

* Python 3.5+
* kubectl_

Installation
------------

The recommended installation method is through pip::

    pip install kubeconfig

If you'd like to install directly from source::

    git clone git@github.com:gtaylor/kubeconfig-python.git
    cd kubeconfig-python
    python setup.py install


Once you are set up, see the :doc:`quickstart` for first steps.

.. _kubectl: https://kubernetes.io/docs/user-guide/kubectl-overview/
