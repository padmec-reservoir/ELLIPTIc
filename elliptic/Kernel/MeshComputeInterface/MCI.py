from .Expression import Computer, Manager, Selector, Expression
from .Expression.Expression import ExpressionBuilder
from typing import Type


class ExprContext:

    def __init__(self,
                 expr_type: Type[Expression.ExpressionBase],
                 mci: 'MCI') -> None:
        self._type = expr_type
        self._mci = mci

    def __enter__(self) -> ExpressionBuilder:
        return ExpressionBuilder()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass


class MCI:

    def selection(self) -> ExprContext:
        return ExprContext(Selector.Selector, self)

    def computation(self) -> ExprContext:
        return ExprContext(Computer.Computer, self)

    def management(self) -> ExprContext:
        return ExprContext(Manager.Manager, self)
