from functools import wraps
from pathlib import Path

import allure

from support.reporters.allure.reporter_protocol import ReporterProtocol


class ASSERTContext:
    _ASSERT_STATUS = True
    _TRACES_PATH = Path('traces')
    aut_info_for_report_dict: dict = {}

    def __enter__(self):
        allure.step('Verify:')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, Exception):
            self._ASSERT_STATUS = False


class ReporterAllure(ReporterProtocol):
    __IS_CURRENT_STAGE_PASSED = True

    def __enter__(self, msg: str = ''):
        self.is_current_stage_passed = True
        self._curr_step_obj = allure.step(f'ASSERT: {msg}')
        self._curr_step_obj.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and not self.__IS_CURRENT_STAGE_PASSED:
            exc_type = type(AssertionError)
            exc_val = AssertionError('SoftAssertionError inside stage')
        self._curr_step_obj.__exit__(exc_type, exc_val, exc_tb)

    @property
    def report_all_methods(self) -> bool:
        return self.__report_all_methods

    @report_all_methods.setter
    def report_all_methods(self, new_value: bool) -> None:
        self.__report_all_methods = new_value

    def ARRANGE(self, msg: str):
        return allure.step(f'ARRANGE: {msg}')

    def ACT(self, msg: str):
        return allure.step(f'ACT: {msg}')

    def ASSERT(self, msg: str):
        return allure.step(f'ASSERT: {msg}')

    def step(self, name: str):
        return allure.step(f'Step: {name}')

    def attach_text(self, text: str):
        return allure.attach(text, name='Info', attachment_type=allure.attachment_type.TEXT)

    def attach_image(self, source, name):
        return allure.attach(source, name=name, attachment_type=allure.attachment_type.PNG)

    def attach_zip(self, source, name):
        return allure.attach(source, name=name, extension='zip')

    def attach_link(self, name: str, url: str):
        return allure.attach(url, name=name, attachment_type=allure.attachment_type.URI_LIST)

    def step_decorator(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            first_line_from_docstring = str(func.__doc__).split('\n')[0] if func.__doc__ else ''
            if isinstance(func, staticmethod):
                with allure.step(
                    f'Step: {first_line_from_docstring} | {func.__module__} -> {func.__class__.__name__} -> {func.__name__}: {kwargs}'
                ):
                    return func(*args, **kwargs)
            else:
                step_self = args[0]
                with allure.step(
                    f'Step: {first_line_from_docstring} | {step_self.__module__} -> {step_self.__class__.__name__} -> {func.__name__}: {kwargs}'
                ):
                    return func(*args, **kwargs)

        return wrapper

    def set_parent_suite(self, parent_suite_name: str):
        return allure.dynamic.parent_suite(parent_suite_name=parent_suite_name)

    def set_suite(self, suite_name: str):
        return allure.dynamic.suite(suite_name=suite_name)

    def set_sub_suite(self, sub_suite_name: str):
        return allure.dynamic.sub_suite(sub_suite_name=sub_suite_name)
