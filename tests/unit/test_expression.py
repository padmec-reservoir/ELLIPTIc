import pytest

from elliptic.Kernel.MeshComputeInterface.Expression import EllipticNode, ExpressionBase, StatementRoot


class TestEllipticNode:

    def test_unique_id(self):
        first_node = EllipticNode()
        second_node = EllipticNode()

        assert first_node.unique_id == 0
        assert second_node.unique_id == 1

    def test_render_returns_child(self, mocker):
        node = EllipticNode()

        with pytest.raises(NotImplementedError):
            node.render(template_manager=None, child='', backend_builder=None)


class TestExpressionBase:

    def test_call(self, mocker):
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


class TestStatementRoot:

    def test_render(self, mocker):
        statement_root = StatementRoot()

        backend_builder = mocker.Mock()
        backend_builder.base.return_value = mocker.sentinel.template_file

        template = mocker.Mock()
        template.render.return_value = mocker.sentinel.rendered_template

        template_manager = mocker.Mock()
        template_manager.get_template.return_value = template

        child = mocker.sentinel.child

        rendered_template = statement_root.render(template_manager=template_manager,
                                                  child=child,
                                                  backend_builder=backend_builder)

        assert rendered_template is mocker.sentinel.rendered_template



