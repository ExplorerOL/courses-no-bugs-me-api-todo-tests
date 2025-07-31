from pytest_check.check_raises import raises as check_raises
from pytest_check.context_manager import CheckContextManager


class NoneError(Exception):
    pass


class AssertSoft(CheckContextManager):
    """Класс мягкого (неблокирующего) ассерта

    Пример использования:
        assert_soft = AssertSoft()
        with assert_soft:
            assert False
    """

    def __enter__(self, msg: str = ''):
        check_raises(NoneError)


assert_soft = AssertSoft()
