from typing import List

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.Contract import DSLContract
from elliptic.Kernel.DSL import DSLMeta
from elliptic.Kernel.TemplateManager import TemplateManagerBase

from .Delegates import BaseDelegate, RangeDelegate


class VectorTemplateManager(TemplateManagerBase):

    def __init__(self) -> None:
        super().__init__(__package__, 'Templates')


class VectorMeta(DSLMeta):

    def include_dirs(self) -> List[str]:
        return []

    def libs(self) -> List[str]:
        return []


class VectorContract(DSLContract):

    def Base(self, context) -> ContextDelegate:
        return BaseDelegate(context)

    def Range(self, context, start, count) -> ContextDelegate:
        return RangeDelegate(context, start, count)
