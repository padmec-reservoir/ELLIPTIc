from anytree import NodeMixin
from typing import Dict, Any, Type


class EllipticNodeMixin(NodeMixin):

    last_id: int = 0

    def __init__(self) -> None:
        super(EllipticNodeMixin, self).__init__()

        self.name: str

        self.unique_id = EllipticNodeMixin.last_id
        EllipticNodeMixin.last_id += 1

    def _name_func(self) -> str:
        return self.name + '_' + str(self.unique_id)

    def _shape(self) -> str:
        return "shape=box"

    def export_tree(self, filename: str) -> None:
        from anytree.exporter import DotExporter

        exporter = DotExporter(self.root,
                               nodenamefunc=lambda node: node._name_func(),
                               nodeattrfunc=lambda node: node._shape())

        exporter.to_picture(filename)


class ExpressionBase(EllipticNodeMixin):

    def __init__(self,
                 args: Dict[str, int],
                 expr_bldr: 'ExpressionBuilder') -> None:
        super(ExpressionBase, self).__init__()

        self.children = (args, expr_bldr)


class Argument(EllipticNodeMixin):

    def __init__(self, name: str, val: Any) -> None:
        super(Argument, self).__init__()

        self.name = name
        self.val = val


class Arguments(EllipticNodeMixin):

    def _shape(self) -> str:
        return "shape=ellipse"

    def __init__(self, **kwargs) -> None:
        super(Arguments, self).__init__()

        self.name = "Args"

        children = []
        for k, v in kwargs.items():
            children.append(Argument(name=k, val=v))
        self.children = children


class StatementRoot(EllipticNodeMixin):

    def _shape(self) -> str:
        return "shape=doubleoctagon"

    def __init__(self) -> None:
        super(StatementRoot, self).__init__()
        self.name = "stmt_root"


class ExpressionBuilder(StatementRoot):

    def __call__(self,
                 expr_type: Type[ExpressionBase],
                 **kwargs) -> 'ExpressionBuilder':
        new_expr_bldr = ExpressionBuilder()
        args = Arguments(**kwargs)
        expr = expr_type(args, new_expr_bldr)

        self.children += (expr,)

        return new_expr_bldr
