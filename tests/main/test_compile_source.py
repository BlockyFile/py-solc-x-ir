#!/usr/bin/python3

import json
from pathlib import Path

import pytest

import solcxir
from solcxir.exceptions import ContractsNotFound

# these values should work for all compatible solc versions
combined_json_values = (
    "abi",
    "asm",
    "ast",
    "bin",
    "bin-runtime",
    "devdoc",
    "metadata",
    "opcodes",
    "srcmap",
    "srcmap-runtime",
    "userdoc",
)


@pytest.fixture(autouse=True)
def setup(all_versions):
    pass


def test_compile_source(foo_source):
    output = solcxir.compile_source(foo_source)
    assert "<stdin>:Foo" in output
    for value in combined_json_values:
        assert value in output["<stdin>:Foo"]


def test_compile_source_with_optimization(foo_source):
    output = solcxir.compile_source(foo_source, optimize=True, optimize_runs=10000)
    assert "<stdin>:Foo" in output
    for value in combined_json_values:
        assert value in output["<stdin>:Foo"]


def test_compile_source_empty():
    with pytest.raises(ContractsNotFound):
        solcxir.compile_source("  ")


def test_compile_source_allow_empty():
    assert solcxir.compile_source("  ", allow_empty=True) == {}


def test_compile_source_output_dir(tmp_path, foo_source):
    solcxir.compile_source(foo_source, output_dir=tmp_path)
    output_path = tmp_path.joinpath("combined.json")

    with output_path.open() as fp:
        output = json.load(fp)["contracts"]
    assert "<stdin>:Foo" in output


def test_compile_source_overwrite(tmp_path, foo_source):
    output_path = tmp_path.joinpath("combined.json")
    with output_path.open("w") as fp:
        fp.write("foobar")

    with pytest.raises(FileExistsError):
        solcxir.compile_source(foo_source, output_dir=tmp_path)
    with pytest.raises(FileExistsError):
        solcxir.compile_source(foo_source, output_dir=tmp_path.joinpath("combined.json"))

    solcxir.compile_source(foo_source, output_dir=tmp_path, overwrite=True)

    with output_path.open() as fp:
        output = json.load(fp)["contracts"]
    assert "<stdin>:Foo" in output


@pytest.mark.parametrize("key", combined_json_values)
def test_compile_source_output_types(foo_source, key):
    output = solcxir.compile_source(foo_source, output_values=[key])
    assert list(output["<stdin>:Foo"]) == [key]


def test_compile_source_import_remapping(foo_path, bar_path, baz_source):
    import_remappings = {"contracts": foo_path.parent, "other": bar_path.parent}
    output = solcxir.compile_source(baz_source, import_remappings=import_remappings)

    assert set(output) == {
        f"{foo_path.as_posix()}:Foo",
        f"{bar_path.as_posix()}:Bar",
        "<stdin>:Baz",
    }


def test_solc_binary(wrapper_mock, foo_source):
    wrapper_mock.expect(solc_binary=Path("path/to/solc"))
    solcxir.compile_source(foo_source, ["abi"], solc_binary=Path("path/to/solc"), allow_empty=True)


def test_solc_version(wrapper_mock, all_versions, foo_source):
    solc_binary = solcxir.install.get_executable(all_versions)
    wrapper_mock.expect(solc_binary=solc_binary)
    solcxir.compile_source(foo_source, ["abi"], solc_version=all_versions, allow_empty=True)
