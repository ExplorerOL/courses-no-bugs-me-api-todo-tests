from config.config_general import config_general
from support.assertions.assert_soft import assert_soft
from support.assertions.custom_assertions import CustomAssertions


class BaseTest:
    assert_soft = assert_soft
    assertions = CustomAssertions

    def __enter__(self) -> None:
        # with ReporterAllureScada.step(name=f'ACT:'):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def ARRANGE(self, msg: str = ''):
        return config_general.reporter.ARRANGE(msg=msg)

    def ACT(self, msg: str = ''):
        return config_general.reporter.ACT(msg=msg)
        # with reporter.step(name=f'ACT: {msg}'):
        # return self

    def ASSERT(self, msg: str = ''):
        return config_general.reporter.ASSERT(msg=msg)
