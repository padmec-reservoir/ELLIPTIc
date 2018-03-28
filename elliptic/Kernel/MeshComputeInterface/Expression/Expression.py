from contextlib import contextmanager

from anytree import NodeMixin
from typing import Type, TypeVar, Iterable, Iterator

from ..BackendBuilder import BackendBuilder, ContextDelegate, ContextType


class EllipticNode(NodeMixin):

    last_id: int = 0

    def __init__(self) -> None:
        super().__init__()

        self.children: Iterable = tuple()
        self.name: str = ''

        self.unique_id = EllipticNode.last_id
        EllipticNode.last_id += 1

    def _name_func(self) -> str:
        return str(self.unique_id) + '\n' + self.name

    def _shape(self) -> str:
        return "shape=box"

    def export_tree(self, filename: str) -> None:
        from anytree.exporter import DotExporter

        exporter = DotExporter(self.root,
                               nodenamefunc=lambda node: node._name_func(),
                               nodeattrfunc=lambda node: node._shape())

        exporter.to_picture(filename)


ExpressionSubClass = TypeVar('ExpressionSubClass', bound='ExpressionBase')


class ExpressionBase(EllipticNode):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self,
                 expr_type: Type[ExpressionSubClass],
                 **kwargs) -> ExpressionSubClass:
        expr = expr_type(**kwargs)

        self.children += (expr,)

        return expr

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        raise NotImplementedError

    def render(self,
               template_manager,
               child: str,
               context_delegate: ContextDelegate,
               context: ContextType) -> str:

        template_file = context_delegate.get_template_file()
        template = template_manager.get_template(template_file)

        kwargs = context_delegate.template_kwargs(context)
        rendered_template = template.render(child=child, **kwargs)

        return rendered_template

    @contextmanager
    def visit(self, backend_builder: BackendBuilder, context: ContextType) -> Iterator[ContextDelegate]:
        context_delegate = self.get_context_delegate(context, backend_builder)

        # ContextDelegate does not implement a context manager so that it can be a simpler protocol
        context_delegate.context_enter(context)
        yield context_delegate
        context_delegate.context_exit(context)


class StatementRoot(ExpressionBase):

    def __init__(self) -> None:
        super(StatementRoot, self).__init__()
        self.name = "stmt_root"

    def _shape(self) -> str:
        return "shape=doubleoctagon"

    def get_context_delegate(self, context, backend_builder) -> ContextDelegate:
        return backend_builder.base_delegate(context=context)
