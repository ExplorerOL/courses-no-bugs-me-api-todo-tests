import inspect
from abc import ABCMeta
from typing import _ProtocolMeta

from config.config_general import config_general


class MetaclassWithMethodReporting(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            # config_core.logger.deep_trace(f'Атрибут {attr_name} имеет тип {type(attr_value)}')
            if callable(attr_value) and not inspect.isclass(attr_value):
                if isinstance(attr_value, staticmethod):
                    # config_core.logger.deep_trace('Декорирование статического метода')
                    attrs[attr_name] = config_general.reporter.static_step_decorator(attrs[attr_name])
                else:
                    # config_core.logger.deep_trace('Декорирование метода объекта')
                    attrs[attr_name] = config_general.reporter.step_decorator(attrs[attr_name])
        return super().__new__(cls, name, bases, attrs)


class MetaclassABCMetaWithMethodReporting(ABCMeta, MetaclassWithMethodReporting):
    pass


class MetaclassProtocolMetaWithMethodReporting(_ProtocolMeta, MetaclassWithMethodReporting):
    pass
