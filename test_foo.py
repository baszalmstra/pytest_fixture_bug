import pytest


@pytest.fixture(scope="session", params=["foo1", "foo2"])
def parameterized_fixture(request):
    print("Calling parameterized_fixture with: {}".format(request.param))
    return request.param


def test_foo(recursive_fixture):
    print("Calling test_bar with: {}".format(recursive_fixture))
    assert("foo" in recursive_fixture)
