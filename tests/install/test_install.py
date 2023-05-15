#!/usr/bin/python3

import pytest

import solcxir
from solcxir.exceptions import SolcInstallationError


@pytest.mark.skipif("'--no-install' in sys.argv")
def test_install_latest():
    version = solcxir.get_installable_solc_versions()[0]
    assert solcxir.install_solc("latest") == version


def test_unknown_platform(monkeypatch):
    monkeypatch.setattr("sys.platform", "potatoOS")
    with pytest.raises(OSError):
        solcxir.install_solc()


def test_install_unknown_version():
    with pytest.raises(SolcInstallationError):
        solcxir.install_solc("0.4.99")


@pytest.mark.skipif("'--no-install' in sys.argv")
def test_progress_bar(nosolc):
    solcxir.install_solc("0.6.9", show_progress=True)


def test_environment_var_path(monkeypatch, tmp_path):
    install_folder = solcxir.get_solcx_install_folder()
    monkeypatch.setenv("solcxir_BINARY_PATH", tmp_path.as_posix())
    assert solcxir.get_solcx_install_folder() != install_folder

    monkeypatch.undo()
    assert solcxir.get_solcx_install_folder() == install_folder


def test_environment_var_versions(monkeypatch, tmp_path):
    versions = solcxir.get_installed_solc_versions()
    monkeypatch.setenv("solcxir_BINARY_PATH", tmp_path.as_posix())
    assert solcxir.get_installed_solc_versions() != versions

    monkeypatch.undo()
    assert solcxir.get_installed_solc_versions() == versions


@pytest.mark.skipif("'--no-install' in sys.argv")
def test_environment_var_install(monkeypatch, tmp_path):
    assert not tmp_path.joinpath("solc-v0.6.9").exists()

    monkeypatch.setenv("solcxir_BINARY_PATH", tmp_path.as_posix())

    solcxir.install_solc("0.6.9")
    assert tmp_path.joinpath("solc-v0.6.9").exists()
