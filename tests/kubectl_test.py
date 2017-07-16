import os

import pytest

from kubeconfig import kubectl


def test_find_kubectl():
    """Make sure we can find and run kubectl"""

    kubectl.run()
