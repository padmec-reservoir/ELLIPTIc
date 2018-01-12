from .Expression import Computer, Manager, Selector, Expression
from .Expression.Expression import ExpressionBuilder


class ExprContext:

    def __init__(self,
                 mci: 'MCI') -> None:
        self._mci = mci

    def __enter__(self) -> ExpressionBuilder:
        return ExpressionBuilder()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass


class MCI:

    def root(self) -> ExprContext:
        return ExprContext(self)
