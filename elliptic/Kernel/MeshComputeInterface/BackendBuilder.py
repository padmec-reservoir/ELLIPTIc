from typing import Dict, List, TYPE_CHECKING

from elliptic.Kernel.Context import ContextDelegate


if TYPE_CHECKING:
    from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction, EllipticReduce


ContextType = Dict[str, List[str]]



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

