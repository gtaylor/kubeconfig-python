kubeconfig
==========

``kubeconfig`` is a simple Python module for manipulating Kubernetes kubeconfig
files.

.. code-block:: py

    import kubeconfig

    conf = kubeconfig.KubeConfig()
    conf.set_context('new-context', cluster='other-cluster', user='my-user')
    conf.use_context('new-context')
    print(conf.view())

Example usage cases
-------------------

* Generating configs for users
* Tooling that manages switching between multiple clusters or users
* Cycling credentials out in a config
* Updating CA cert entries in your config

How it works
------------

Rather than re-implement and maintain the kubeconfig detection, selection, and
merging logic found in kubectl_, this module calls on ``kubectl`` to do the
config reading and writing.

This does make ``kubectl`` a hard dependency for this module, but also ensures
behavior that is consistent with what you'd expect by using ``kubectl``
directly.

.. _kubectl: https://kubernetes.io/docs/user-guide/kubectl-overview/

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api
