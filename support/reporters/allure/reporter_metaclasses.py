import inspect
from abc import ABCMeta
from typing import _ProtocolMeta

from config.config_general import config_general


class MetaclassWithMethodReporting(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not inspect.isclass(attr_value) and not attr_name.startswith('_'):
                attrs[attr_name] = config_general.reporter.step_decorator(attrs[attr_name])
        return super().__new__(cls, name, bases, attrs)


class MetaclassABCMetaWithMethodReporting(ABCMeta, MetaclassWithMethodReporting):
    pass


class MetaclassProtocolMetaWithMethodReporting(_ProtocolMeta, MetaclassWithMethodReporting):
    pass
