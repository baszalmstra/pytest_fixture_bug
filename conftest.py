import pytest


@pytest.fixture(scope="session")
def parameterized_fixture(request):
    return request.param


@pytest.fixture(scope="session")
def recursive_fixture(parameterized_fixture):
    print("Calling recursive_fixture with: {}".format(parameterized_fixture))
    return parameterized_fixture
