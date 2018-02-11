from typing import TypeVar, Dict, Union, List
from typing_extensions import Protocol


class BackendBuilder:
    pass


BackendBuilderSubClass = TypeVar('BackendBuilderSubClass', bound=BackendBuilder)
ContextType = Dict[str, Union[str, List[str]]]


class BackendDelegate(Protocol):

    def update_context(self, backend_builder: BackendBuilderSubClass, context: ContextType):
        ...

    def get_template_file(self, backend_builder: BackendBuilderSubClass):
        ...

    def template_kwargs(self, backend_builder: BackendBuilderSubClass, context: ContextType):
        ...
