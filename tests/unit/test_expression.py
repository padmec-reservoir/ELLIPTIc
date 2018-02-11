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

    def test_render(self, mocker):
        backend_delegate = mocker.Mock(spec=BackendDelegate)
        backend_delegate.get_template_file.return_value = mocker.sentinel.template_file
        backend_delegate.template_kwargs.return_value = {}

        class ExpressionStub(ExpressionBase):
            def get_delegate_obj(self, _):
                return backend_delegate

        expression = ExpressionStub()

        context = mocker.sentinel.context

        backend_builder = mocker.sentinel.backend_builder

        template = mocker.Mock()
        template.render.return_value = mocker.sentinel.rendered_template

        template_manager = mocker.Mock()
        template_manager.get_template.return_value = template

        child = mocker.sentinel.child

        rendered_template = expression.render(template_manager=template_manager,
                                              child=child,
                                              backend_builder=backend_builder,
                                              context=context)

        assert rendered_template is mocker.sentinel.rendered_template

        backend_delegate.update_context.assert_called_once_with(backend_builder,
                                                                mocker.sentinel.context)
        backend_delegate.get_template_file.assert_called_once_with(backend_builder)
        backend_delegate.template_kwargs.assert_called_once_with(backend_builder,
                                                                 mocker.sentinel.context)
