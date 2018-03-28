from typing import Dict, Union, List, TYPE_CHECKING

from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction, EllipticReduce


ContextType = Dict[str, List[str]]


class ContextDelegate(ABC):

    def __init__(self, context):
        self.context = context

    def put_value(self, name, value):
        self.context[name].append(value)

    def get_value(self, name):
        return self.context[name][-1]

    def pop_value(self, name):
        self.context[name].pop()

    @abstractmethod
    def get_template_file(self):
        pass

    @abstractmethod
    def template_kwargs(self, context: ContextType):
        pass

    @abstractmethod
    def context_enter(self, context: ContextType):
        pass

    @abstractmethod
    def context_exit(self, context: ContextType):
        pass


class BackendBuilder:

    def base_delegate(self, context) -> ContextDelegate:
        raise NotImplementedError

    def interface_delegate(self, context, to_ent: int) -> ContextDelegate:
        raise NotImplementedError

    def by_ent_delegate(self, context, dim: int) -> ContextDelegate:
        raise NotImplementedError

    def by_adj_delegate(self, context, bridge_dim: int, to_dim: int) -> ContextDelegate:
        raise NotImplementedError

    def where_delegate(self, context, conditions) -> ContextDelegate:
        raise NotImplementedError

    def map_delegate(self, context, mapping_function: 'EllipticFunction', fargs) -> ContextDelegate:
        raise NotImplementedError

    def reduce_delegate(self, context, reducing_function: 'EllipticReduce', fargs) -> ContextDelegate:
        raise NotImplementedError

    def put_field_delegate(self, context, field_name: str) -> ContextDelegate:
        raise NotImplementedError

    def create_matrix_delegate(self, context, field_name: str) -> ContextDelegate:
        raise NotImplementedError

    def fill_columns_delegate(self, context, matrix: int) -> ContextDelegate:
        raise NotImplementedError

    def fill_diag_delegate(self, context, matrix: int) -> ContextDelegate:
        raise NotImplementedError

    def solve_delegate(self, context) -> ContextDelegate:
        raise NotImplementedError

