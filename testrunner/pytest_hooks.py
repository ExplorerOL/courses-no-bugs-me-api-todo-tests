from config.config_general import config_general


def pytest_configure(config):
    config_general.base_url = config.option.base_url
