from anytree import NodeMixin, AnyNode, RenderTree


class EllipticNodeMixin(NodeMixin):

    last_id = 0

    def __init__(self):
        super(EllipticNodeMixin, self).__init__()

        print(self.last_id)
        print("\n\n\n\n\n\n\n\n")

        self.unique_id = self.__class__.last_id
        self.__class__.last_id += 1

    def _name_func(self):
        return self.name + '_' + str(self.unique_id)

    def _shape(self):
        return "shape=box"

    def export_tree(self, filename):
        from anytree.exporter import DotExporter

        exporter = DotExporter(self.root,
                               nodenamefunc=lambda node: node._name_func(),
                               nodeattrfunc=lambda node: node._shape())

        exporter.to_picture(filename)


class ExpressionBase(EllipticNodeMixin):

    def __init__(self, args, expr_bldr):
        super(ExpressionBase, self).__init__()

        self.children = (args, expr_bldr)


class StatementRoot(EllipticNodeMixin):

    def _shape(self):
        return "shape=doubleoctagon"

    def __init__(self):
        super(StatementRoot, self).__init__()
        self.name = "stmt_root"


class Argument(EllipticNodeMixin):

    def __init__(self, name, val):
        super(Argument, self).__init__()

        self.name = name
        self.val = val


class Arguments(EllipticNodeMixin):

    def _shape(self):
        return "shape=ellipse"

    def __init__(self, **kwargs):
        super(Arguments, self).__init__()

        self.name = "Args"

        children = []
        for k, v in kwargs.items():
            children.append(Argument(name=k, val=v))
        self.children = children


class ExpressionBuilder(StatementRoot):

    def __call__(self, expr_type, **kwargs):
        new_expr_bldr = ExpressionBuilder()
        args = Arguments(**kwargs)
        expr = expr_type(args, new_expr_bldr)

        self.children += (expr,)

        return new_expr_bldr
