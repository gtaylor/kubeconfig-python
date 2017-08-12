Quickstart
==========

After :doc:`installation`, you are ready to start working with your configs.

Reading your Config
-------------------

We'll start by reading your current configs, with the result being returned
as a dict:

.. code-block:: py

    from kubeconfig import KubeConfig

    conf = KubeConfig()
    print(conf.view())

Since we're just calling ``kubectl`` under the covers, your ``KUBECONFIG``
environment variable will be referenced, and all kubeconfig merging rules
will apply.

If you want to read a specific kubeconfig, you can pass that in as well:

.. code-block:: py

    conf = KubeConfig('path-to-your-config')

Creating or modifying credentials
---------------------------------

Use
:py:meth:`KubeConfig.set_credentials <kubeconfig.KubeConfig.set_credentials>`
to create or modify credentials:

.. code-block:: py

    from kubeconfig import KubeConfig

    conf = KubeConfig()
    kc.set_credentials(name='my-user, token='super-secret-token')

Creating or modifying a cluster
-------------------------------

Use
:py:meth:`KubeConfig.set_cluster <kubeconfig.KubeConfig.set_cluster>`
to create or modify clusters:

.. code-block:: py

    from kubeconfig import KubeConfig

    conf = KubeConfig()
    kc.set_cluster(
        name='my-cluster,
        server='https://my-k8s-api-server.xxx/'
        certificate_authority='/path/to/ca.crt',
    )

Creating or modifying a context
-------------------------------

Use
:py:meth:`KubeConfig.set_cluster <kubeconfig.KubeConfig.set_cluster>`
to create or modify contexts:

.. code-block:: py

    from kubeconfig import KubeConfig

    conf = KubeConfig()
    kc.set_context(
        name='my-context,
        cluster='my-cluster'
        user='my-user',
    )


Changing your current context
-----------------------------

If you'd like to switch to another context in your config file, this is
done via :py:meth:`KubeConfig.use_context <kubeconfig.KubeConfig.use_context>`:

.. code-block:: py

    from kubeconfig import KubeConfig

    conf = KubeConfig()
    conf_doc = conf.view()
    print('Current context:', conf_doc['current-context'])
    conf.use_context('new-context')
    # Re-read the config.
    conf_doc = conf.view()
    print('Current context:', conf_doc['current-context'])
