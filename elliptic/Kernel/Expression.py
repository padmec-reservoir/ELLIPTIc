from contextlib import contextmanager

from anytree import NodeMixin
from typing import Type, TypeVar, Iterable, Iterator

from .Contract import DSLContract
from .Context import ContextDelegate, Context


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

    def get_context_delegate(self, context: Context, dsl_contract: DSLContract) -> ContextDelegate:
        raise NotImplementedError

    def render(self,
               template_manager,
               child: str,
               context_delegate: ContextDelegate) -> str:

        template_file = context_delegate.get_template_file()
        template = template_manager.get_template(template_file)

        kwargs = context_delegate.template_kwargs()
        rendered_template = template.render(child=child, **kwargs)

        return rendered_template

    @contextmanager
    def visit(self, dsl_contract: DSLContract, context: Context) -> Iterator[ContextDelegate]:
        context_delegate = self.get_context_delegate(context, dsl_contract)

        # ContextDelegate does not implement a context manager so that it can be a simpler protocol
        context_delegate.context_enter()
        yield context_delegate
        context_delegate.context_exit()


class StatementRoot(ExpressionBase):

    def __init__(self) -> None:
        super(StatementRoot, self).__init__()
        self.name = "stmt_root"

    def _shape(self) -> str:
        return "shape=doubleoctagon"

    def get_context_delegate(self, context: Context, dsl_contract: DSLContract) -> ContextDelegate:
        return dsl_contract.base_delegate(context=context)
