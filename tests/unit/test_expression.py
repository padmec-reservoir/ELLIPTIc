from contextlib import contextmanager

import pytest

from elliptic.Kernel.MeshComputeInterface.Expression import EllipticNode, ExpressionBase
from elliptic.Kernel.MeshComputeInterface.Expression.Selector.Dilute import ByEnt, ByAdj
from elliptic.Kernel.MeshComputeInterface.Expression.Selector.Filter import Where


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
