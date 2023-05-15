#!/usr/bin/python3

import sys

import pytest
from semantic_version import Version

import solcxir
from solcxir.exceptions import SolcInstallationError, UnexpectedVersionError, UnexpectedVersionWarning


def test_validate_installation_wrong_version(monkeypatch, install_mock, install_path):
    monkeypatch.setattr("solcxir.wrapper._get_solc_version", lambda k: Version("0.0.0"))

    with pytest.raises(UnexpectedVersionError):
        solcxir.install_solc()

    assert not install_path.exists()


def test_validate_installation_nightly(monkeypatch, install_mock, solc_binary, install_path):
    version = solcxir.wrapper._get_solc_version(solc_binary)
    monkeypatch.setattr("solcxir.wrapper._get_solc_version", lambda k: Version(f"{version}-nightly"))

    with pytest.warns(UnexpectedVersionWarning):
        solcxir.install_solc()

    assert install_path.exists()


def test_validate_installation_fails(monkeypatch, solc_binary, install_path):
    def _mock(*args, **kwargs):
        if sys.platform == "win32":
            install_path.mkdir()
            with install_path.joinpath("solc.exe").open("w") as fp:
                fp.write("blahblah")
        else:
            with install_path.open("w") as fp:
                fp.write("blahblah")

    monkeypatch.setattr("solcxir.install._install_solc_unix", _mock)
    monkeypatch.setattr("solcxir.install._install_solc_windows", _mock)

    with pytest.raises(SolcInstallationError):
        solcxir.install_solc()

    assert not install_path.exists()
