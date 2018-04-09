from collections import defaultdict
from typing import Dict, List
from abc import ABC, abstractmethod


class ContextException(Exception):
    """Exception raised when an error related to a Context operation occurs.
    """


class Context:

    def __init__(self):
        self.context: Dict[str, List[str]] = defaultdict(list)

    def put_value(self, name: str, value: str):
        self.context[name].append(value)

    def get_value(self, name: str):
        try:
            return self.context[name][-1]
        except IndexError:
            raise ContextException(f"Name {name} does not exist in the context.")

    def pop_value(self, name: str):
        try:
            self.context[name].pop()
        except IndexError:
            raise ContextException(f"Name {name} does not exist in the context.")

    def clear_values(self, name: str):
        self.context[name].clear()


class ContextDelegate(ABC):

    def __init__(self, context: Context):
        self.context = context
        self.child = ""

    @abstractmethod
    def get_template_file(self):
        raise NotImplementedError

    @abstractmethod
    def template_kwargs(self):
        raise NotImplementedError

    @abstractmethod
    def context_enter(self):
        raise NotImplementedError

    @abstractmethod
    def context_exit(self):
        raise NotImplementedError
