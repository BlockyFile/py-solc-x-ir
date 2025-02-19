#!/usr/bin/python3

import functools

import pytest
from semantic_version import Version

import solcxir
from solcxir.exceptions import SolcNotInstalled, UnsupportedVersionError


def test_set_solc_version_pragma(pragmapatch):
    set_pragma = functools.partial(solcxir.set_solc_version_pragma, check_new=True)
    assert set_pragma("pragma solidity 0.4.11;") == Version("0.4.11")
    assert set_pragma("pragma solidity ^0.4.11;") == Version("0.4.25")
    assert set_pragma("pragma solidity >=0.4.0<0.4.25;") == Version("0.4.11")
    assert set_pragma("pragma solidity >=0.4.2;") == Version("1.2.3")
    assert set_pragma("pragma solidity >=0.4.2<0.5.5;") == Version("0.5.4")
    assert set_pragma("pragma solidity ^0.4.2 || 0.5.5;") == Version("0.4.25")
    assert set_pragma("pragma solidity ^0.4.2 || >=0.5.4<0.7.0;") == Version("0.5.7")
    with pytest.raises(SolcNotInstalled):
        set_pragma("pragma solidity ^0.7.1;")


def test_install_solc_version_pragma(pragmapatch):
    install_pragma = functools.partial(solcxir.install_solc_pragma, install=False)
    assert install_pragma("pragma solidity ^0.4.11;") == Version("0.4.26")
    assert install_pragma("pragma solidity >=0.4.0<0.4.25;") == Version("0.4.24")
    assert install_pragma("pragma solidity >=0.4.2;") == Version("0.6.0")
    assert install_pragma("pragma solidity >=0.4.2<0.5.5;") == Version("0.5.3")
    assert install_pragma("pragma solidity ^0.4.2 || 0.5.5;") == Version("0.4.26")
    assert install_pragma("pragma solidity ^0.4.2 || >=0.5.4<0.7.0;") == Version("0.6.0")
    with pytest.raises(UnsupportedVersionError):
        install_pragma("pragma solidity ^0.7.1;")


def test_get_solc_version():
    version = solcxir.get_solc_version()
    version_with_hash = solcxir.get_solc_version(with_commit_hash=True)

    assert version != version_with_hash
    assert version == version_with_hash.truncate()
