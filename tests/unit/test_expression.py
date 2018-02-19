from contextlib import contextmanager

import pytest

from elliptic.Kernel.MeshComputeInterface.Expression import EllipticNode, ExpressionBase
from elliptic.Kernel.MeshComputeInterface.Expression.Manager import PutField
from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction
from elliptic.Kernel.MeshComputeInterface.Expression.Computer.Map import Map
from elliptic.Kernel.MeshComputeInterface.Expression.Manager.Matrix import Create, FillColumns, FillDiag, Solve
from elliptic.Kernel.MeshComputeInterface.Expression.Selector import Interface
from elliptic.Kernel.MeshComputeInterface.Expression.Selector.Dilute import ByEnt, ByAdj
from elliptic.Kernel.MeshComputeInterface.Expression.Selector.Filter import Where
from elliptic.Kernel.MeshComputeInterface.Expression.Selector.Selector import Selector


class TestEllipticNode:

    def test_unique_id(self):
        first_node = EllipticNode()
        second_node = EllipticNode()

        assert first_node.unique_id == 0
        assert second_node.unique_id == 1


@pytest.fixture()
def delegate_stub():
    class DelegateStub:
        def get_template_file(self):
            pass

        def template_kwargs(self, _):
            pass

        def context_enter(self, context):
            context[5] = 10

        def context_exit(self, context):
            context[5] = 5

    return DelegateStub


class TestExpressionBase:

    def test_call(self):
        class ExpressionStub(ExpressionBase):
            def __init__(self, arg):
                super().__init__()
                self.arg = arg

        expression = ExpressionBase()

        expr = expression(ExpressionStub, arg=5)

        assert isinstance(expr, ExpressionStub)
        assert expr.arg == 5
        assert expression.children[0] is expr
        assert len(expression.children) == 1

    def test_visit(self, mocker, delegate_stub):
        context = {}
        backend_builder = mocker.sentinel.backend_builder

        class ExpressionStub(ExpressionBase):
            def get_context_delegate(self, backend_builder):
                return delegate_stub()

        expression = ExpressionStub()

        with expression.visit(backend_builder, context) as context_delegate:
            assert context[5] == 10

        assert context[5] == 5


@contextmanager
def _test_expression(mocker, delegate_stub_, delegate_fun, test_cls, **cls_kwargs):
    inst = test_cls(**cls_kwargs)
    backend_builder = mocker.Mock()
    getattr(backend_builder, delegate_fun).return_value = delegate_stub_()
    context = {}

    with inst.visit(backend_builder, context) as context_delegate:
        assert context[5] == 10
        yield {'backend_builder': backend_builder,
               'expression': inst}

    assert context[5] == 5


class TestDilute:

    def test_by_ent(self, mocker, delegate_stub):
        with _test_expression(mocker, delegate_stub, 'by_ent_delegate', ByEnt, dim=3) as ret:
            ret['backend_builder'].by_ent_delegate.assert_called_once_with(dim=3)

    def test_by_adj(self, mocker, delegate_stub):
        with _test_expression(mocker, delegate_stub, 'by_adj_delegate', ByAdj, bridge_dim=2, to_dim=3) as ret:
            ret['backend_builder'].by_adj_delegate.assert_called_once_with(bridge_dim=2, to_dim=3)


class TestFilter:

    def test_where(self, mocker, delegate_stub):
        args = {'a': 1, 'b': 2}
        with _test_expression(mocker, delegate_stub, 'where_delegate', Where, **args) as ret:
            ret['backend_builder'].where_delegate.assert_called_once_with(conditions=args.items())


class TestInterface:

    def test_interface(self, mocker, delegate_stub):
        to_ent = mocker.Mock(spec=Selector)
        to_ent.unique_id = 5

        with _test_expression(mocker, delegate_stub, 'interface_delegate', Interface, to_ent=to_ent) as ret:
            ret['backend_builder'].interface_delegate.assert_called_once_with(to_ent=5)


class TestMap:

    def test_map(self, mocker, delegate_stub):
        args = {'a': 1, 'b': 2}
        mapping_function = mocker.Mock()
        mapping_function.name = "test"
        mapping_function.process_fun_args.return_value = args
        mapping_function.kwargs = args

        with _test_expression(mocker, delegate_stub, 'map_delegate', Map, mapping_function=mapping_function) as ret:
            ret['backend_builder'].map_delegate.assert_called_once_with(mapping_function=mapping_function,
                                                                        fargs=args.items())


class TestMapFunctions:

    def test_map_functions(self, mocker, delegate_stub):
        from inspect import getmembers, isclass
        from elliptic.Kernel.MeshComputeInterface.Expression.Computer import MapFunctions

        functions_list = [getattr(MapFunctions, o[0]) for o in getmembers(MapFunctions) if isclass(o[1])]

        for fun in functions_list:
            assert issubclass(fun, EllipticFunction)


class TestManager:

    def test_put_field(self, mocker, delegate_stub):
        with _test_expression(mocker, delegate_stub, 'put_field_delegate', PutField, field_name='test') as ret:
            ret['backend_builder'].put_field_delegate.assert_called_once_with(field_name='test')


class TestMatrix:

    def test_create(self, mocker, delegate_stub):
        with _test_expression(mocker, delegate_stub, 'create_matrix_delegate', Create, field_name='test') as ret:
            ret['backend_builder'].create_matrix_delegate.assert_called_once_with(field_name='test')

    def test_fill_columns(self, mocker, delegate_stub):
        matrix = mocker.sentinel.matrix
        with _test_expression(mocker, delegate_stub, 'fill_columns_delegate', FillColumns, matrix=matrix) as ret:
            ret['backend_builder'].fill_columns_delegate.assert_called_once_with(matrix=matrix)

    def test_fill_diag(self, mocker, delegate_stub):
        matrix = mocker.sentinel.matrix
        with _test_expression(mocker, delegate_stub, 'fill_diag_delegate', FillDiag, matrix=matrix) as ret:
            ret['backend_builder'].fill_diag_delegate.assert_called_once_with(matrix=matrix)

    def test_solve(self, mocker, delegate_stub):
        with _test_expression(mocker, delegate_stub, 'solve_delegate', Solve) as ret:
            ret['backend_builder'].solve_delegate.assert_called_once()
