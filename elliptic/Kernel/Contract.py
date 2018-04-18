from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.Expression import Expression


class DSLImplementation(ABC):
    """Abstract class that defines a DSL Implementation. Should be used to connect the
    corresponding :class:`Context Delegates <elliptic.Kernel.Context.ContextDelegate>`.
    """

    @abstractmethod
    def base_delegate(self) -> Type[ContextDelegate]:
        """Returns the context delegate for the DSL base context handling.

        The base context delegate could be used, for example, to declare variables and initialize
        dependencies for the generated code.
        """
        raise NotImplementedError


DSLImplementationSubclass = TypeVar('DSLImplementationSubclass', bound=DSLImplementation)
DSLContractSubclass = TypeVar('DSLContractSubclass', bound='DSLContract')


class DSLContract(Generic[DSLImplementationSubclass]):
    """Defines the contract of the DSL.

    The DSL contract is the set of operations that the DSL supports, plus a base operation.
    Each operation should create an `Expression` instance and call `append_tree` with the created expression.

    Parameters:
        dsl_impl: DSL Implementation object.
        expr: Current DSL operation. If set to None, will be set to the next operation done
            when calling `append_tree`.

    Attributes:
        dsl_impl: DSL Implementation object.
        expr: Current DSL operation.
    """

    def __init__(self, dsl_impl: DSLImplementationSubclass, expr: Expression=None):
        self.dsl_impl: DSLImplementationSubclass = dsl_impl
        self.expr: Expression = expr

    def append_tree(self: DSLContractSubclass, expr: Expression) -> DSLContractSubclass:
        """Inserts the given expression to the expression tree and returns a new DSLContract
        bounded to the given expression.
        """
        if not self.expr:
            self.expr = expr
            return self
        else:
            self.expr.add_child(expr)
            return self.__class__(self.dsl_impl, expr)

    def Base(self: DSLContractSubclass) -> DSLContractSubclass:
        """Base operation. Called by default from ELLIPTIc before any other operation.
        """
        expr = Expression(self.dsl_impl.base_delegate(), "Base")
        expr.shape = "shape=doubleoctagon"

        return self.append_tree(expr)
