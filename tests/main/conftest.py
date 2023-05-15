import pytest


class WrapperMock:
    """
    Simple mock for solcxir.wrapper.solc_wrapper
    """

    def __call__(self, **kwargs):
        for key, value in self.kwargs.items():
            assert kwargs[key] == value
        return '{"contracts":{}}', "", [], 0

    def expect(self, **kwargs):
        self.kwargs = kwargs


@pytest.fixture
def wrapper_mock(monkeypatch):
    mock = WrapperMock()
    monkeypatch.setattr("solcxir.wrapper.solc_wrapper", mock)
    yield mock
