from .Expression import Computer, Manager, Selector
from .Expression.Expression import ExpressionBuilder


class ExprContext:

    def __init__(self, expr_type, mci):
        self._type = expr_type
        self._mci = mci

    def __enter__(self):
        return ExpressionBuilder()

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class MCI:

    def selection(self):
        return ExprContext(Selector, self)

    def computation(self):
        return ExprContext(Computer, self)

    def management(self):
        return ExprContext(Manager, self)
