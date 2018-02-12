import pytest

from elliptic.Kernel.MeshComputeInterface.Expression import EllipticNode, ExpressionBase
from elliptic.Kernel.MeshComputeInterface.BackendBuilder import BackendDelegate


class TestEllipticNode:

    def test_unique_id(self):
        first_node = EllipticNode()
        second_node = EllipticNode()

        assert first_node.unique_id == 0
        assert second_node.unique_id == 1


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

    def test_visit(self, mocker):
        context = {}
        backend_builder = mocker.sentinel.backend_builder

        class DelegateStub:
            def get_template_file(self):
                pass
            def template_kwargs(self, _):
                pass
            def context_enter(self, context):
                context[5] = 10
            def context_exit(self, context):
                context[5] = 5

        class ExpressionStub(ExpressionBase):
            def get_delegate_obj(self, _):
                return DelegateStub()

        expression = ExpressionStub()

        with expression.visit(backend_builder, context) as delegate_obj:
            assert context[5] == 10

        assert context[5] == 5
