import solcxir
import solcxir.main


def test_get_combined_json_outputs_defaults(mocker, foo_source):
    # verify we get the correct combined json outputs for different
    # compiler versions
    spy = mocker.spy(solcxir.main, "_get_combined_json_outputs")

    solcxir.compile_source(foo_source, solc_version="0.4.12")
    assert "function-debug" not in spy.spy_return

    solcxir.compile_source(foo_source, solc_version="0.8.9")
    assert "function-debug" in spy.spy_return
