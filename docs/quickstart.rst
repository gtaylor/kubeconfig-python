Quickstart
==========

After :doc:`installation`, you are ready to start working with your configs.

Reading your Config
-------------------

We'll start by reading your current configs, with the result being returned
as a dict.

.. code-block:: py

    import kubeconfig

    conf = kubeconfig.KubeConfig()
    print(conf.view())

Since we're just calling ``kubectl`` under the covers, your ``KUBECONFIG``
environment variable will be referenced, and all kubeconfig merging rules
will apply.

If you want to read a specific kubeconfig, you can pass that in as well:

.. code-block:: py

    conf = kubeconfig.KubeConfig('path-to-your-config')

Changing your current context
-----------------------------

If you'd like to switch to another context in your config file, this is
done via :py:meth:`kubeconfig.KubeConfig.use_context`:

.. code-block:: py

    conf = kubeconfig.KubeConfig()
    conf_doc = conf.view()
    print('Current context:', conf_doc['current-context'])
    conf.use_context('new-context')
    # Re-read the config.
    conf_doc = conf.view()
    print('Current context:', conf_doc['current-context'])
