from functions import __package_name__
from functions import __version__


def test_version():
    assert type(__version__) is str


def test_something_else():
    assert __package_name__ == "functions-cli"
