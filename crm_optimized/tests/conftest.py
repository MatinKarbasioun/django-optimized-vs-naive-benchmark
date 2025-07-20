import pytest

from crm_optimized.bootstrap import Bootstrap


@pytest.fixture(scope="session", autouse=True)
def init():
    Bootstrap()