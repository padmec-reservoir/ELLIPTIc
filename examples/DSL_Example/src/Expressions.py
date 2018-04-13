from elliptic.Kernel import Context
from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.Expression import ExpressionBase

from .DSL import VectorContract


class Range(ExpressionBase):

    def __init__(self, start, count):
        super().__init__()

        self.start = start
        self.count = count
        self.name = f"Range({start}, {count})"

    def get_context_delegate(self, context: Context, dsl_contract: VectorContract) -> ContextDelegate:
        return dsl_contract.range_delegate(context=context, start=self.start, count=self.count)
