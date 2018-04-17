from abc import ABC, abstractmethod
from typing import List, Type

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.Contract import DSLContract, DSLImplementation
from elliptic.Kernel.DSL import DSLMeta
from elliptic.Kernel.Expression import Expression
from elliptic.Kernel.TemplateManager import TemplateManagerBase


class VectorTemplateManager(TemplateManagerBase):

    def __init__(self) -> None:
        super().__init__(__package__, 'Templates')


class VectorMeta(DSLMeta):

    def include_dirs(self) -> List[str]:
        return []

    def libs(self) -> List[str]:
        return []


class VectorImplementationBase(DSLImplementation):

    @abstractmethod
    def range_delegate(self, start, count) -> Type[ContextDelegate]:
        raise NotImplementedError


class VectorContract(DSLContract[VectorImplementationBase]):

    def Range(self, start: int, count: int) -> 'VectorContract':
        return self.append_tree(Expression(self.dsl_impl.range_delegate(start, count), "Range"))
