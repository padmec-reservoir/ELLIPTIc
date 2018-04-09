from abc import ABC, abstractmethod

from .Context import ContextDelegate


class DSLContract(ABC):
    """Defines the abstract contract of the DSL.

    The DSL abstract contract is the set of operations that the DSL supports, plus a base member.
    Each member should return an instance of a concrete implementation of the ContextDelegate class.
    """

    @abstractmethod
    def base_delegate(self, context) -> ContextDelegate:
        """Returns the context delegate for the DSL base context handling.

        The base context delegate could be used, for example, to declare variables and initialize
        dependencies for the generated code.
        """
        raise NotImplementedError