from abc import ABC
from typing import Protocol

from support.reporters.allure.reporter_metaclasses import (
    ClassABCMetaWithMethodReporting,
    ClassProtocolMetaWithMethodReporting,
    MetaclassWithMethodReporting,
)


class ClassWithMethodReporting(metaclass=MetaclassWithMethodReporting):
    pass


class ABCWithMethodReporting(ABC, metaclass=ClassABCMetaWithMethodReporting):
    pass


class ProtocolWithInstanceMethodReporting(Protocol, metaclass=ClassProtocolMetaWithMethodReporting):
    pass
