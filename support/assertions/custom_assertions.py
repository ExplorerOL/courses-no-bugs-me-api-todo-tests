from contextlib import nullcontext
from typing import Any

from support.assertions.assert_soft import assert_soft


class CustomAssertions:
    @staticmethod
    def verify_is_equal(actual_value: Any, expected_value: Any, soft: bool = True, msg: str = '') -> None:
        """Проверка на равенство фактического и ожидаемого значений."""
        with assert_soft if soft else nullcontext():
            assert actual_value == expected_value, (
                f'Фактическое значение {actual_value!r} не равно ожидаемому {expected_value!r}!'
            )
