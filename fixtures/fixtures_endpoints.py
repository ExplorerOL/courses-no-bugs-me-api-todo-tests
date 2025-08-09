import pytest

from config.config_general import config_general
from config.endpoints import EndpointsVersions


@pytest.fixture(scope='function')
def set_endpoints_to_mobile():
    config_general.set_version(version=EndpointsVersions.MOBILE)
    yield
    config_general.set_version(version=EndpointsVersions.WEB)


@pytest.fixture(scope='function', autouse=True)
def check_test_markers(request):
    if request.node.get_closest_marker('mobile'):
        config_general.set_version(version=EndpointsVersions.MOBILE)
    yield
    config_general.set_version(version=EndpointsVersions.WEB)
