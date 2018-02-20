from typing import Dict, Union, List, TYPE_CHECKING
from typing_extensions import Protocol


if TYPE_CHECKING:
    from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction, EllipticReduce


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


class BackendBuilder(Protocol):

    def base_delegate(self) -> ContextDelegate:
        ...

    def interface_delegate(self, to_ent: int) -> ContextDelegate:
        ...

    def by_ent_delegate(self, dim: int) -> ContextDelegate:
        ...

    def by_adj_delegate(self, bridge_dim: int, to_dim: int) -> ContextDelegate:
        ...

    def where_delegate(self, conditions) -> ContextDelegate:
        ...

    def map_delegate(self, mapping_function: 'EllipticFunction', fargs) -> ContextDelegate:
        ...

    def reduce_delegate(self, reducing_function: 'EllipticReduce', fargs) -> ContextDelegate:
        ...

    def put_field_delegate(self, field_name: str) -> ContextDelegate:
        ...

    def create_matrix_delegate(self, field_name: str) -> ContextDelegate:
        ...

    def fill_columns_delegate(self, matrix: int) -> ContextDelegate:
        ...

    def fill_diag_delegate(self, matrix: int) -> ContextDelegate:
        ...

    def solve_delegate(self) -> ContextDelegate:
        ...

