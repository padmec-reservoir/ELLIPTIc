from collections import defaultdict
from contextlib import contextmanager

import pytest

from elliptic.Kernel.Context import Context, ContextException
from elliptic.Kernel.Expression import EllipticNode, ExpressionBase, StatementRoot


class TestEllipticNode:

    def test_unique_id(self):
        first_node = EllipticNode()
        second_node = EllipticNode()

        assert first_node.unique_id != second_node.unique_id

    def test_name_func(self):
        node = EllipticNode()
        node.name = "test"

        assert node._name_func() == f'{node.unique_id}\ntest'

    def test_shape(self):
        node = EllipticNode()

        assert node._shape() == "shape=box"

    def test_export_tree(self, mocker):
        node = EllipticNode()

        exporter = mocker.patch('anytree.exporter.DotExporter')
        exporter_obj = mocker.Mock()
        exporter.return_value = exporter_obj

        node.export_tree('filename.png')

        exporter_obj.to_picture.assert_called_once_with('filename.png')


class TestStatementRoot:
    def test_shape(self):
        root: StatementRoot = StatementRoot()

        assert root._shape() == "shape=doubleoctagon"


class TestExpressionBase:

    def test_call(self):
        class ExpressionStub(ExpressionBase):
            def __init__(self, arg):
                super().__init__()
                self.arg = arg

        expression: ExpressionBase = ExpressionBase()

        expr = expression(ExpressionStub, arg=5)

        assert isinstance(expr, ExpressionStub)
        assert expr.arg == 5
        assert expression.children[0] is expr
        assert len(expression.children) == 1

    def test_visit(self, mocker, delegate_stub):
        context = Context()
        backend_builder = mocker.sentinel.backend_builder

        class ExpressionStub(ExpressionBase):
            def get_context_delegate(self, context, backend_builder):
                return delegate_stub(context)

        expression = ExpressionStub()

        with expression.visit(backend_builder, context) as context_delegate:
            assert context.get_value('a') == '10'

        with pytest.raises(ContextException):
            context.get_value('a')

    def test_get_context_delegate_raises_NotImplementedError(self):
        expression: ExpressionBase = ExpressionBase()

        with pytest.raises(NotImplementedError):
            expression.get_context_delegate(None, None)

    def test_render(self, mocker):
        child = "child"
        kwargs = {"arg1": 1, "arg2": 2}

        template = mocker.Mock()
        template.render.return_value = mocker.sentinel.rendered_template

        template_manager = mocker.Mock()
        template_manager.get_template.return_value = template

        context_delegate = mocker.Mock()
        context_delegate.get_template_file.return_value = mocker.sentinel.template_file
        context_delegate.template_kwargs.return_value = kwargs

        expression: ExpressionBase = ExpressionBase()

        rendered_template = expression.render(template_manager, child, context_delegate)

        assert rendered_template is mocker.sentinel.rendered_template

        context_delegate.get_template_file.assert_called_once()
        template_manager.get_template.assert_called_once_with(mocker.sentinel.template_file)
        context_delegate.template_kwargs.assert_called_once()
        template.render.assert_called_once_with(child=child, **kwargs)
