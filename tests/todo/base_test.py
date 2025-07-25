from support.assertions.assert_soft import assert_soft
from support.assertions.custom_assertions import CustomAssertions


class BaseTest:
    assert_soft = assert_soft
    assertions = CustomAssertions
