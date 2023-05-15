#!/usr/bin/python3


import pytest

import solcxir
from solcxir.exceptions import SolcNotInstalled, UnsupportedVersionError


def test_get_executable():
    assert solcxir.install.get_executable() == solcxir.install._default_solc_binary


def test_no_default_set(nosolc):
    with pytest.raises(SolcNotInstalled):
        solcxir.install.get_executable()


def test_unsupported_version():
    with pytest.raises(UnsupportedVersionError):
        solcxir.install.get_executable("0.4.0")


def test_version_not_installed():
    with pytest.raises(SolcNotInstalled):
        solcxir.install.get_executable("999.999.999")
