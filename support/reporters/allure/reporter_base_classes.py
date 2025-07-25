from abc import ABC
from typing import Protocol

from support.reporters.allure.reporter_metaclasses import (
    MetaclassABCMetaWithMethodReporting,
    MetaclassProtocolMetaWithMethodReporting,
    MetaclassWithMethodReporting,
)

# class ClassWithStepLoggingAndReporting(metaclass=MetaclassWithStepLoggingAndReporting):
#     logger: LoggerProtocol


class ClassWithMethodReporting(metaclass=MetaclassWithMethodReporting):
    pass


class ABCWithMethodReporting(ABC, metaclass=MetaclassABCMetaWithMethodReporting):
    pass


class ProtocolWithInstanceMethodReporting(Protocol, metaclass=MetaclassProtocolMetaWithMethodReporting):
    pass
