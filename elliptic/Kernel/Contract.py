from typing import TypeVar, Generic

from elliptic.Kernel.Expression import Expression


DSLImplementation = TypeVar('DSLImplementation')


class DSLContract(Generic[DSLImplementation]):
    """Defines the abstract contract of the DSL.

    The DSL abstract contract is the set of operations that the DSL supports, plus a base member.
    Each member should return an instance of a concrete implementation of the ContextDelegate class.

    Parameters:
        dsl_impl: DSL Implementation object.
        expr: Current DSL operation. If set to None, will be set to the next operation done
            when calling `append_tree`.

    Attributes:
        dsl_impl: DSL Implementation object.
        expr: Current DSL operation.
    """

    def __init__(self, dsl_impl: DSLImplementation, expr: Expression=None):
        self.dsl_impl: DSLImplementation = dsl_impl
        self.expr: Expression = expr

    def append_tree(self, expr: Expression):
        """Inserts the given expression to the expression tree and returns a new DSLContract
        bounded to the given expression.
        """
        if not self.expr:
            self.expr = expr
            return self
        else:
            self.expr.add_child(expr)
            return self.__class__(self.dsl_impl, expr)

    def Base(self):
        """Returns the context delegate for the DSL base context handling.

        The base context delegate could be used, for example, to declare variables and initialize
        dependencies for the generated code.
        """
        expr = Expression(self.dsl_impl.base_delegate(), "Base")
        expr.shape = "shape=doubleoctagon"

        return self.append_tree(expr)
