from collections import defaultdict
from typing import Dict, List, Any
from abc import ABC, abstractmethod


class ContextException(Exception):
    """Exception raised when an error related to a Context operation occurs.
    """


class Context:
    """Defines a context for code generation.

    A Context is basically a dictionary of stacks. In other words, it defines
    a `stack_name -> stack` mapping. Each `stack` has is semantically defined by its
    `stack_name`.


    Example:
        >>> context = Context()
        >>> context.put_value('current_value', '100')
        >>> context.put_value('current_value', '200')
        >>> context.get_value('current_value')  # 200
        >>> context.pop_value('current_value')
        >>> context.get_value('current_value')  # 100

    """

    def __init__(self) -> None:
        self.context: Dict[str, List[str]] = defaultdict(list)

    def put_value(self, name: str, value: str) -> None:
        """Pushes the value `value` to a stack named `name`.
        """
        self.context[name].append(value)

    def get_value(self, name: str) -> str:
        """Gets the front value of the stack named `name`.
        """
        try:
            return self.context[name][-1]
        except IndexError:
            raise ContextException(f"Name {name} does not exist in the context.")

    def pop_value(self, name: str) -> None:
        """Pops the front value of the stack named `name`.
        """
        try:
            self.context[name].pop()
        except IndexError:
            raise ContextException(f"Name {name} does not exist in the context.")

    def clear_values(self, name: str) -> None:
        """Clears the stack named `name`.
        """
        self.context[name].clear()


class ContextDelegate(ABC):
    """Delegate class for getting the generated code template file and its kwargs for a
    given expression.

    Also defines the context state changes when the corresponding expression node is visited
    and exited.

    Attributes:
        context (:class:`Context`): Context instance.
    """

    def __init__(self, context: Context):
        self.context = context
        self.child = ""

    @abstractmethod
    def get_template_file(self) -> str:
        """Returns the template file containing the generated code for the expression.
        """
        raise NotImplementedError

    @abstractmethod
    def template_kwargs(self) -> Dict[str, Any]:
        """Returns the arguments (a dictionary) that will be passed to the template.
        """
        raise NotImplementedError

    @abstractmethod
    def context_enter(self) -> None:
        """Modifies the context state. Called when the expression node is visited.

        Use this method to prepare the context for expressions that will be visited
        afterwards. It is preferable to keep most `context.put_value` calls in this method.
        """
        raise NotImplementedError

    @abstractmethod
    def context_exit(self) -> None:
        """Modifies the context state. Called when the expression node is exited.

        Use this method to clear values from the context and prepare it for the
        expression nodes that were visited before. It is preferable to keep most
        `context.pop_value` calls in this method.
        """
        raise NotImplementedError
