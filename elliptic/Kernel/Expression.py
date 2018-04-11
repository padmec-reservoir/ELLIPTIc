from contextlib import contextmanager

from anytree import NodeMixin
from typing import Type, TypeVar, Iterable, Iterator

from .Contract import DSLContract
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

    def _name_func(self) -> str:
        return str(self.unique_id) + '\n' + self.name

    def _shape(self) -> str:
        return "shape=box"

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


ExpressionSubClass = TypeVar('ExpressionSubClass', bound='ExpressionBase')


class ExpressionBase(EllipticNode):
    """Base class for building DSL expressions.
    """

    def __init__(self) -> None:
        super().__init__()

    def __call__(self,
                 expr_type: Type[ExpressionSubClass],
                 **kwargs) -> ExpressionSubClass:
        """Inserts a new node in the DSL tree.

        Parameters:
            expr_type: A expression type. A new node will be created with this type.
            kwargs: The keyword arguments to be passed when creating the new node
                (i.e. to the `expr_type` constructor).
        """
        expr = expr_type(**kwargs)

        self.children += (expr,)

        return expr

    def get_context_delegate(self, context: Context, dsl_contract: DSLContract) -> ContextDelegate:
        """Returns the context delegate for this expression.

        Parameters:
            context: A context object.
            dsl_contract: The DSL contract.
        """
        raise NotImplementedError

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
    def visit(self, context: Context, dsl_contract: DSLContract) -> Iterator[ContextDelegate]:
        """Context manager used when an expression node is visited in the DSL tree.

        Calls the :class:`context delegate <elliptic.Kernel.Context.ContextDelegate>`
        :meth:`~elliptic.Kernel.Context.ContextDelegate.context_enter`
        and :meth:`~elliptic.Kernel.Context.ContextDelegate.context_exit` methods.

        Parameters:
            dsl_contract: The DSL contract.
            context: A context object.
        """
        context_delegate = self.get_context_delegate(context, dsl_contract)

        # ContextDelegate does not implement a context manager so that it can be a simpler protocol
        context_delegate.context_enter()
        yield context_delegate
        context_delegate.context_exit()


class StatementRoot(ExpressionBase):
    """Represents the root of the DSL statement.
    """

    def __init__(self) -> None:
        super(StatementRoot, self).__init__()
        self.name = "stmt_root"

    def _shape(self) -> str:
        return "shape=doubleoctagon"

    def get_context_delegate(self, context: Context, dsl_contract: DSLContract) -> ContextDelegate:
        """Returns the base delegate from the given :class:`~elliptic.Kernel.Contract.DSLContract` instance.

        Parameters:
            context: A context object.
            dsl_contract: The DSL contract.
        """
        return dsl_contract.base_delegate(context=context)
