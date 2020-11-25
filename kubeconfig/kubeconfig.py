"""View or manipulate your kubeconfig file.

For example:

.. code-block:: py

    import kubeconfig

    # We'll use kubectl's default kubeconfig resolution heuristics.
    conf = kubeconfig.KubeConfig()
    # See the full, merged contents of your effective kubeconfig.
    print(conf.view())
    # Change your default context.
    conf.use_context('another-context')
    # Check to see our changes.
    print(conf.view())
"""
import yaml


from . import kubectl


class KubeConfig(object):
    """
    This is the top-level class for manipulating your kubeconfig file.
    You may view or make changes using the exposed methods. Changes take
    effect immediately.

    .. note:: All values read from your config file(s) will be decoded to
        Python strings. This happens as a result of our parsing the YAML.

    :param str path: If you'd like to work against a specific kubeconfig
        file instead of using your currently configured (or default),
        pass the full path in.
    """

    def __init__(self, path=None):
        self.path = path

    def _bool_to_cli_str(self, bool_arg):
        """
        :param bool bool_arg: A boolean value.
        :rtype: str
        :return: The CLI form of the boolean. IE: 'false', 'true'.
        """
        if not isinstance(bool_arg, bool):
            raise ValueError("Not a bool: %s", bool_arg)
        return repr(bool_arg).lower()

    def _run_kubectl_config(self, *args):
        """
        This convenience method is for invoking kubectl sub-commands and
        retrieving the resulting stdout/stderr.

        :raise: :py:exc:`KubectlCommandError <kubeconfig.exceptions.KubectlCommandError>`
            when kubectl exits with an error.
        :rtype: str
        :return: A combination of stdout+stderr for the given kubectl command.
        """
        subcmd_args = ['config'] + list(args)
        return kubectl.run(kubeconfig=self.path, subcmd_args=subcmd_args)

    def current_context(self):
        """
        :rtype: str or None
        :return: Your config's currently selected context (``current-context``),
            or ``None`` if not set.
        """
        current_context = self.view().get('current-context')
        return current_context if current_context else None

    def delete_cluster(self, name):
        """
        Deletes a cluster entry from your config.

        :param str name: The name of the cluster to delete from your config.
        :raise: :py:exc:`KubectlCommandError <kubeconfig.exceptions.KubectlCommandError>`
            when an invalid cluster name is specified.
        """
        self._run_kubectl_config('delete-cluster', name)

    def delete_context(self, name):
        """
        Deletes a context entry from your config.

        :param str name: The name of the context to delete from your config.
        :raise: :py:exc:`KubectlCommandError <kubeconfig.exceptions.KubectlCommandError>` 
            when an invalid context name is specified.
        """
        self._run_kubectl_config('delete-context', name)

    def rename_context(self, old_name, new_name):
        """
        Changes the name of a context in your config.

        :param str old_name: The name of the context to rename.
        :param str new_name: The desired new name for the context.
        :raise: :py:exc:`KubectlCommandError <kubeconfig.exceptions.KubectlCommandError>`
            when an invalid context name is specified for old or new.
        """
        self._run_kubectl_config('rename-context', old_name, new_name)

    def set(self, name, value):
        """
        Sets an individual value in your config.

        :param str name: The dot delimited name of the key to set.
        :param value: The value to set on the key.
        :raise: :py:exc:`KubectlCommandError <kubeconfig.exceptions.KubectlCommandError>`
            when an invalid name is specified.
        """
        self._run_kubectl_config('set', name, value)

    def set_cluster(self, name, certificate_authority=None, embed_certs=None,
                    insecure_skip_tls_verify=None, server=None):
        """
        Creates or updates a cluster entry in your config. In the case where
        you are updating an existing cluster, only the optional keyword args
        that you pass in will be updated on the entry.

        :param str name: The name of the cluster to modify.
        :param str certificate_authority: Path to a certificate authority
            file for verifying the certs on the cluster's API server.
        :param bool embed_certs: Combined with ``certificate_authority``,
            setting this to ``True`` will cause the CA cert to be embedded
            directly in the written config. If ``False`` or unspecified,
            the path to the CA cert will be used instead.
        :param bool insecure_skip_tls_verify: If ``True``, we won't do
            cert validation against the cluster's API server.
        :param str server: Full URI to the cluster's API server.
        """
        flags = []
        if certificate_authority is not None:
            flags += ['--certificate-authority=%s' % certificate_authority]
        if embed_certs is not None:
            flags += ['--embed-certs=%s' % self._bool_to_cli_str(embed_certs)]
        if insecure_skip_tls_verify is not None:
            flags += ['--insecure-skip-tls-verify=%s' %
                      self._bool_to_cli_str(insecure_skip_tls_verify)]
        if server is not None:
            flags += ['--server=%s' % server]
        self._run_kubectl_config('set-cluster', name, *flags)

    def set_context(self, name, cluster=None, namespace=None, user=None):
        """
        Creates or updates a context entry in your config. In the case where
        you are updating an existing context, only the optional keyword args
        that you pass in will be updated on the entry.

        :param str name: The name of the context to modify.
        :param str cluster: Determines the context's cluster.
        :param str namespace: Sets the default namespace for the context.
        :param str user: The user to authenticate as for the context.
        """
        flags = []
        if cluster is not None:
            flags += ['--cluster=%s' % cluster]
        if namespace is not None:
            flags += ['--namespace=%s' % namespace]
        if user is not None:
            flags += ['--user=%s' % user]
        self._run_kubectl_config('set-context', name, *flags)

    def set_credentials(self, name, auth_provider=None, auth_provider_args=None,
                        client_certificate=None, client_key=None,
                        embed_certs=None, password=None, token=None,
                        username=None):
        """
        Creates or updates a ``user`` entry under the ``users`` entry.
        In the case where you are updating an existing user, only the optional
        keyword args that you pass in will be updated on the entry.

        :param str name: The name of the user to add or update.
        :param str auth_provider: The auth provider name to use. For example,
            ``oidc``, ``gcp``, etc.
        :param dict auth_provider_args: Some providers support extra config
            params, which can be passed in as a flat dict.
        :param str client_certificate: Path to your X.509 client cert (if
            using cert auth).
        :param str client_key: Path to your cert's private key (if using
            cert auth).
        :param bool embed_certs: Combined with ``client_certificate``,
            setting this to ``True`` will cause the cert to be embedded
            directly in the written config. If ``False`` or unspecified,
            the path to the cert will be used instead.
        :param str username: Your username (if using basic auth).
        :param str password: Your user's password (if using basic auth).
        :param str token: Your private token (if using token auth).
        """
        flags = []
        if auth_provider is not None:
            flags += ['--auth-provider=%s' % auth_provider]
        if auth_provider_args is not None:
            arg_pairs = ["%s=%s" % (k, v) for k, v in auth_provider_args.items()]
            for arg_pair in arg_pairs:
                flags += ['--auth-provider-arg=%s' % arg_pair]
        if client_certificate is not None:
            flags += ['--client-certificate=%s' % client_certificate]
        if client_key is not None:
            flags += ['--client-key=%s' % client_key]
        if embed_certs is not None:
            flags += ['--embed-certs=%s' % self._bool_to_cli_str(embed_certs)]
        if password is not None:
            flags += ['--password=%s' % password]
        if token is not None:
            flags += ['--token=%s' % token]
        if username is not None:
            flags += ['--username=%s' % username]
        self._run_kubectl_config('set-credentials', name, *flags)

    def unset(self, name):
        """
        Unsets an individual value in your kubeconfig file.

        :param str name: The dot delimited name of the key to unset.
        :raise: :py:exc:`KubectlCommandError <kubeconfig.exceptions.KubectlCommandError>`
            when an invalid name is specified.
        """
        self._run_kubectl_config('unset', name)

    def use_context(self, name):
        """
        Changes your default/active context.

        :param str name: The context to set as current.
        :raise: :py:exc:`KubectlCommandError <kubeconfig.exceptions.KubectlCommandError>`
            when an invalid context name is specified.
        """
        self._run_kubectl_config('use-context', name)

    def view(self):
        """
        :rtype: dict
        :return: A dict representing your full kubeconfig file, after all
            merging has been done.
        """
        conf_doc_str = self._run_kubectl_config('view', '--raw')
        return yaml.safe_load(conf_doc_str)
