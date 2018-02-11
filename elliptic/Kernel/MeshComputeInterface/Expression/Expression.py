from anytree import NodeMixin
from typing import Type, TypeVar, Iterable, Dict, List, Union

from ..BackendBuilder import BackendBuilderSubClass, BackendDelegate, ContextType


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

    def get_delegate_obj(self, backend_builder: BackendBuilderSubClass) -> BackendDelegate:
        raise NotImplementedError

    def render(self,
               template_manager,
               child: str,
               backend_builder: BackendBuilderSubClass,
               context: ContextType) -> str:
        delegate_obj = self.get_delegate_obj(backend_builder)

        delegate_obj.update_context(backend_builder, context)
        template_file = delegate_obj.get_template_file(backend_builder)
        template = template_manager.get_template(template_file)

        kwargs = delegate_obj.template_kwargs(backend_builder, context)
        rendered_template = template.render(child=child, **kwargs)

        return rendered_template


class StatementRoot(ExpressionBase):

    def __init__(self) -> None:
        super(StatementRoot, self).__init__()
        self.name = "stmt_root"

    def _shape(self) -> str:
        return "shape=doubleoctagon"

    def get_delegate_obj(self, backend_builder):
        return backend_builder.base_delegate()
