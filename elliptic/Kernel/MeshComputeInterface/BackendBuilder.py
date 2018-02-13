from typing import TypeVar, Dict, Union, List
from typing_extensions import Protocol


class BackendBuilder:
    pass


BackendBuilderSubClass = TypeVar('BackendBuilderSubClass', bound=BackendBuilder)
ContextType = Dict[str, Union[str, List[str]]]


class ContextDelegate(Protocol):

    def get_template_file(self):
        ...

    def template_kwargs(self, context: ContextType):
        ...

    def context_enter(self, context: ContextType):
        ...

    def context_exit(self, context: ContextType):
        ...
