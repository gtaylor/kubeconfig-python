kubeconfig
==========

kubeconfig is a simple Python module for manipulating Kubernetes kubeconfig
files.

.. code-block:: py

    from kubeconfig import KubeConfig

    conf = KubeConfig()
    conf.set_context('new-context', cluster='other-cluster', user='my-user')
    conf.use_context('new-context')
    print(conf.view())

Installing
----------

.. code-block:: shell

    pip install kubeconfig

Example usage cases
-------------------

* Generating configs for users
* Tooling that manages switching between multiple clusters or users
* Cycling credentials out in a config
* Updating CA cert entries in your config

Documentation
-------------

See the documentation_ for more details on usage.

License
-------

kubeconfig is licensed under the BSD 3-Clause License.

.. _documentation: http://kubeconfig-python.readthedocs.io
