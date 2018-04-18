from contextlib import contextmanager

from anytree import NodeMixin
from typing import Iterable, Iterator, Type

from .Context import ContextDelegate, Context


class EllipticNode(NodeMixin):
    """Base class for representing a node in the DSL tree.
    """

    last_id: int = 0

    def __init__(self) -> None:
        super().__init__()

        self.children: Iterable = tuple()
        self.name: str = ''

        self.unique_id = EllipticNode.last_id
        EllipticNode.last_id += 1

        self.shape = "shape=box"

    def _name_func(self) -> str:
        return str(self.unique_id) + '\n' + self.name

    def _shape(self) -> str:
        return self.shape

    def export_tree(self, filename: str) -> None:
        """Exports a graphical representation of the DSL tree.

        This method can be called from any tree node. The tree root will always be used.

        Parameters:
            filename: Name for the exported image file.
        """
        from anytree.exporter import DotExporter

        exporter = DotExporter(self.root,
                               nodenamefunc=lambda node: node._name_func(),
                               nodeattrfunc=lambda node: node._shape())

        exporter.to_picture(filename)


class Expression(EllipticNode):
    """Base class for building DSL expressions.

    Parameters:
        context_delegate: A context delegate object responsible for generating some Cython code.
        display_name: The name that will be displayed when this Expression is rendered into a picture.
        display_args: The arguments that will be displayed below this Expression name in the rendered picture.
    """

    def __init__(self, context_delegate: Type[ContextDelegate], display_name="", display_args=None) -> None:
        super().__init__()

        if not display_args:
            display_args = {}

        args_str = ""
        for k, v in display_args.items():
            args_str = f"{args_str}\n{k}={v}"
        self.name = f"{display_name}{args_str}"

        self.context_delegate = context_delegate

    def add_child(self, expr: 'Expression'):
        self.children += (expr,)

    def render(self,
               template_manager,
               child: str,
               context_delegate: ContextDelegate) -> str:
        """Render the expression generated code.

        Parameters:
            template_manager: A `TemplateManagerBase` instance.
            child: The rendered template corresponding to this node's child.
            context_delegate: The context delegate for the DSL.
        """

        template_file = context_delegate.get_template_file()
        template = template_manager.get_template(template_file)

        kwargs = context_delegate.template_kwargs()
        rendered_template = template.render(child=child, **kwargs)

        return rendered_template

    @contextmanager
    def visit(self, context: Context) -> Iterator[ContextDelegate]:
        """Context manager used when an expression node is visited in the DSL tree.

        Calls the :class:`context delegate <elliptic.Kernel.Context.ContextDelegate>`
        :meth:`~elliptic.Kernel.Context.ContextDelegate.context_enter`
        and :meth:`~elliptic.Kernel.Context.ContextDelegate.context_exit` methods.

        Parameters:
            context: A context object.
        """
        context_delegate = self.context_delegate(context, self.unique_id)

        # ContextDelegate does not implement a context manager so that it can be a simpler protocol
        context_delegate.context_enter()
        yield context_delegate
        context_delegate.context_exit()
