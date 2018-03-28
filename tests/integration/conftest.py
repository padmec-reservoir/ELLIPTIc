"""
These delegates are arbitrarily defined just for testing,
and have no relation with the expected MCI behavior.
"""
import pytest

from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, ContextType, BackendBuilder
from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction, EllipticReduce
from elliptic.Kernel.TreeBuilder import TemplateManagerBase


class SimpleBackendBuilder(BackendBuilder):

    def base_delegate(self, context) -> ContextDelegate:
        class Delegate(ContextDelegate):

            def get_template_file(self):
                return 'base.etp'

            def template_kwargs(self, context: ContextType):
                return {'a': self.get_value('a'),
                        'b': self.get_value('b')}

            def context_enter(self, context: ContextType):
                self.put_value('a', 'x')
                self.put_value('b', 'a')
                self.put_value('cur_var', 'base_str')

            def context_exit(self, context: ContextType):
                self.pop_value('a')
                self.pop_value('b')
                self.pop_value('cur_var')

        return Delegate(context)

    def interface_delegate(self, context, to_ent: int) -> ContextDelegate:
        raise NotImplementedError

    def by_ent_delegate(self, context, dim: int) -> ContextDelegate:
        class Delegate(ContextDelegate):

            def get_template_file(self):
                return 'by_ent.etp'

            def template_kwargs(self, context: ContextType):
                return {'append_var': self.get_value('cur_var'),
                        'append_val': self.get_value('a')}

            def context_enter(self, context: ContextType):
                self.put_value('a', str(dim))

            def context_exit(self, context: ContextType):
                self.pop_value('a')

        return Delegate(context)

    def by_adj_delegate(self, context, bridge_dim: int, to_dim: int) -> ContextDelegate:
        raise NotImplementedError

    def where_delegate(self, context, conditions) -> ContextDelegate:
        raise NotImplementedError

    def map_delegate(self, context, mapping_function: EllipticFunction, fargs) -> ContextDelegate:
        raise NotImplementedError

    def reduce_delegate(self, context, reducing_function: EllipticReduce, fargs) -> ContextDelegate:
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


@pytest.fixture()
def template_manager():
    template_manager_ = TemplateManagerBase('res', 'templates')

    return template_manager_


@pytest.fixture()
def simple_backend_builder():
    backend_builder = SimpleBackendBuilder()

    return backend_builder
