#!/usr/bin/python3

import solcxir


def test_import_solc(monkeypatch, solc_binary, nosolc):
    version = solcxir.wrapper._get_solc_version(solc_binary)

    monkeypatch.setattr("solcxir.install._get_which_solc", lambda: solc_binary)
    assert solcxir.import_installed_solc() == [version]

    assert nosolc.joinpath(f"solc-v{version}").exists()


def test_import_solc_fails_after_importing(monkeypatch, solc_binary, nosolc):
    count = 0
    version = solcxir.wrapper._get_solc_version(solc_binary)

    def version_mock(*args):
        # the first version call succeeds, the second attempt fails
        # this mocks a solc binary that no longer works after being copied
        nonlocal count
        if not count:
            count += 1
            return version
        raise Exception

    monkeypatch.setattr("solcxir.install._get_which_solc", lambda: solc_binary)
    monkeypatch.setattr("solcxir.wrapper._get_solc_version", version_mock)

    assert solcxir.import_installed_solc() == []
    assert not nosolc.joinpath(solc_binary.name).exists()
