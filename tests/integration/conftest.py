"""
These delegates are arbitrarily defined just for testing,
and have no relation with the expected MCI behavior.
"""
import pytest

from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, ContextType
from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction, EllipticReduce
from elliptic.Kernel.TreeBuilder import TemplateManagerBase


class SimpleBackendBuilder:

    def base_delegate(self) -> ContextDelegate:
        class Delegate:

            def get_template_file(self):
                return 'base.etp'

            def template_kwargs(self, context: ContextType):
                return {'a': context['a'][-1], 'b': context['b'][-1]}

            def context_enter(self, context: ContextType):
                context['a'].append('x')
                context['b'].append('a')
                context['cur_var'].append('base_str')

            def context_exit(self, context: ContextType):
                context['a'].pop()
                context['b'].pop()
                context['cur_var'].pop()

        return Delegate()

    def interface_delegate(self, to_ent: int) -> ContextDelegate:
        raise NotImplementedError

    def by_ent_delegate(self, dim: int) -> ContextDelegate:
        class Delegate:

            def get_template_file(self):
                return 'by_ent.etp'

            def template_kwargs(self, context: ContextType):
                return {'append_var': context['cur_var'][-1],
                        'append_val': context['a'][-1]}

            def context_enter(self, context: ContextType):
                context['a'].append(str(dim))

            def context_exit(self, context: ContextType):
                context['a'].pop()

        return Delegate()

    def by_adj_delegate(self, bridge_dim: int, to_dim: int) -> ContextDelegate:
        raise NotImplementedError

    def where_delegate(self, conditions) -> ContextDelegate:
        raise NotImplementedError

    def map_delegate(self, mapping_function: EllipticFunction, fargs) -> ContextDelegate:
        raise NotImplementedError

    def reduce_delegate(self, reducing_function: EllipticReduce, fargs) -> ContextDelegate:
        raise NotImplementedError

    def put_field_delegate(self, field_name: str) -> ContextDelegate:
        raise NotImplementedError

    def create_matrix_delegate(self, field_name: str) -> ContextDelegate:
        raise NotImplementedError

    def fill_columns_delegate(self, matrix: int) -> ContextDelegate:
        raise NotImplementedError

    def fill_diag_delegate(self, matrix: int) -> ContextDelegate:
        raise NotImplementedError

    def solve_delegate(self) -> ContextDelegate:
        raise NotImplementedError


@pytest.fixture()
def template_manager():
    template_manager_ = TemplateManagerBase('res', 'templates')

    return template_manager_


@pytest.fixture()
def simple_backend_builder():
    backend_builder = SimpleBackendBuilder()

    return backend_builder
