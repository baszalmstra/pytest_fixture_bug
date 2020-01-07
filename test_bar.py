import pytest


@pytest.fixture(scope="session", params=["bar1"])
def parameterized_fixture(request):
    print("Calling parameterized_fixture with: {}".format(request.param))
    return request.param


def test_bar(recursive_fixture):
    print("Calling test_foo with: {}".format(recursive_fixture))
    assert("bar" in recursive_fixture)
