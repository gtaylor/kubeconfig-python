import os
import shutil

import pytest

import kubeconfig

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
SAMPLES_PATH = os.path.join(THIS_PATH, 'samples')
TMP_FIXTURES_DIR = os.path.join(THIS_PATH, 'tmp_fixtures')


def _sample(sample_name):
    return os.path.join(SAMPLES_PATH, sample_name)


def _copy_sample(sample_name):
    src = _sample(sample_name)
    dest = os.path.join(TMP_FIXTURES_DIR, sample_name)
    shutil.copy(src, dest)
    return dest


@pytest.fixture()
def prep_fixture_dir():
    shutil.rmtree(TMP_FIXTURES_DIR, ignore_errors=True)
    os.makedirs(TMP_FIXTURES_DIR)

#
# current-context tests
#


def test_current_context():
    # Should be test-context
    kc = kubeconfig.KubeConfig(_sample('one-context.config'))
    assert kc.current_context() == 'test-context'


def test_current_context_minimal_config():
    # No context set. Should be None.
    kc = kubeconfig.KubeConfig(_sample('minimal.config'))
    assert kc.current_context() is None


def test_current_context_empty_config():
    # Non-existing kubeconfig, assumes default.
    kc = kubeconfig.KubeConfig('this-does-not-exist.config')
    assert kc.current_context() is None

#
# delete-cluster tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_delete_cluster_minimal_invalid_name():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    with pytest.raises(kubeconfig.exceptions.KubectlCommandError):
        kc.delete_cluster('invalid')


@pytest.mark.usefixtures('prep_fixture_dir')
def test_delete_cluster():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert len(kc.view()['clusters']) == 1
    kc.delete_cluster('test-cluster')
    assert len(kc.view()['clusters']) == 0


#
# delete-context tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_delete_context_minimal_invalid_name():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    with pytest.raises(kubeconfig.exceptions.KubectlCommandError):
        kc.delete_context('invalid')


@pytest.mark.usefixtures('prep_fixture_dir')
def test_delete_context():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert len(kc.view()['contexts']) == 1
    kc.delete_context('test-context')
    assert len(kc.view()['contexts']) == 0


#
# rename-context tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_rename_context_minimal_invalid_name():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    with pytest.raises(kubeconfig.exceptions.KubectlCommandError):
        kc.rename_context('invalid', 'invalid-too')


@pytest.mark.usefixtures('prep_fixture_dir')
def test_rename_context():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert len(kc.view()['contexts']) == 1
    assert kc.view()['contexts'][0]['name'] == 'test-context'
    kc.rename_context('test-context', 'test-context-new')
    assert len(kc.view()['contexts']) == 1
    assert kc.view()['contexts'][0]['name'] == 'test-context-new'


#
# set tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_minimal_invalid_key():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    with pytest.raises(kubeconfig.exceptions.KubectlCommandError):
        kc.set('invalid', 'blah')


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert kc.view()['current-context'] == 'test-context'
    kc.set('current-context', 'new-context')
    assert kc.view()['current-context'] == 'new-context'


#
# set-cluster tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_cluster_new():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    kc.set_cluster('new-cluster')
    clusters = kc.view()['clusters']
    assert len(clusters) == 1
    assert clusters[0]['name'] == 'new-cluster'


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_cluster_existing():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert kc.view()['clusters'][0]['cluster']['server'] == 'https://192.168.1.100'
    kc.set_cluster('test-cluster', server='https://yarr')
    assert kc.view()['clusters'][0]['cluster']['server'] == 'https://yarr'


#
# set-context tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_context_new():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    kc.set_context('new-context', cluster='new-cluster')
    assert kc.view()['contexts'][0]['context']['cluster'] == 'new-cluster'


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_context_existing():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert kc.view()['contexts'][0]['context']['cluster'] == 'test-cluster'
    kc.set_context('test-context', cluster='other-cluster')
    assert kc.view()['contexts'][0]['context']['cluster'] == 'other-cluster'

#
# set-credentials tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_credentials_new():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    kc.set_credentials('new-user', username='new-user')
    assert kc.view()['users'][0]['user']['username'] == 'new-user'


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_credentials_existing():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert kc.view()['users'][0]['user']['auth-provider']['name'] == 'gcp'
    kc.set_credentials('test-user', auth_provider='other')
    assert kc.view()['users'][0]['user']['auth-provider']['name'] == 'other'


@pytest.mark.usefixtures('prep_fixture_dir')
def test_set_credentials_auth_args():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    provider_args = {
        'token-key': 'test',
        'expiry-key': 'test',
    }
    kc.set_credentials('test-user', auth_provider_args=provider_args)
    auth_provider = kc.view()['users'][0]['user']['auth-provider']
    assert auth_provider['config']['token-key'] == 'test'
    assert auth_provider['config']['expiry-key'] == 'test'


#
# unset tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_unset_context_minimal_invalid_key():
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    with pytest.raises(kubeconfig.exceptions.KubectlCommandError):
        kc.unset('invalid')


@pytest.mark.usefixtures('prep_fixture_dir')
def test_unset():
    kc = kubeconfig.KubeConfig(_copy_sample('simple-complete.config'))
    assert kc.view()['current-context'] == 'test-context'
    kc.unset('current-context')
    assert kc.view()['current-context'] == ''


#
# use-context tests
#


@pytest.mark.usefixtures('prep_fixture_dir')
def test_use_context_minimal_invalid_name():
    # Trying to use an undefined context is a hard failure.
    kc = kubeconfig.KubeConfig(_copy_sample('minimal.config'))
    with pytest.raises(kubeconfig.exceptions.KubectlCommandError):
        kc.use_context('invalid')


@pytest.mark.usefixtures('prep_fixture_dir')
def test_use_context():
    # The normal case.
    kc = kubeconfig.KubeConfig(_copy_sample('one-context.config'))
    kc.use_context('test-context')
    assert kc.view()['current-context'] == 'test-context'


#
# view tests
#


def test_view():
    kc = kubeconfig.KubeConfig(_sample('simple-complete.config'))
    config = kc.view()

    assert config['clusters'][0]['name'] == 'test-cluster'
    assert config['contexts'][0]['name'] == 'test-context'
    assert config['current-context'] == 'test-context'
    assert config['users'][0]['name'] == 'test-user'


@pytest.mark.usefixtures('prep_fixture_dir')
def test_view_empty_config():
    # In absence of a kubeconfig, the default behavior is to assume an
    # empty config with a basic structure.
    kc = kubeconfig.KubeConfig('this-does-not-exist.config')
    config = kc.view()

    assert type(config) == dict
    # Quick sanity check to make sure we've got a minimal doc coming through.
    assert 'apiVersion' in config
