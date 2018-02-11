from elliptic.Kernel.MeshComputeInterface.Expression.Expression import StatementRoot
from elliptic.Kernel.MeshComputeInterface.Expression.Manager import PutField
from elliptic.Kernel.MeshComputeInterface.Expression.Computer.Map import GetScalarField
from .Expression import DeclareVariable, CreateField, DeclareExistingField


class TreePreprocessor:

    def __init__(self, root):
        self.root = root

    def run(self):
        self._preprocess_subtree(self.root)

        self.root.export_tree("preprocessed.png")

    def _preprocess_subtree(self, node):
        self._preprocess_node(node)

        for child in node.children:
            self._preprocess_subtree(child)

    def _preprocess_node(self, node):
        if isinstance(node, PutField):
            self._preprocess_field(node, CreateField)
        elif isinstance(node, GetScalarField):
            self._preprocess_field(node, DeclareExistingField)

    def _add_declare_node(self, node, var_name, var_type="double"):
        # Declaration nodes can be in any order
        # Here we put them just after the statement root, therefore they are always guaranteed to be
        # on top of every other node.
        # This is similar to variable hoisting.
        stmt_root = self._find_node_above(node, StatementRoot)
        declare_node = DeclareVariable(var_name=var_name,
                                       var_type=var_type)

        declare_node.children = stmt_root.children
        declare_node.parent = stmt_root

        return declare_node

    def _preprocess_field(self, node, field_type):
        field_node = field_type(name=node.field_name)

        field_handle_node = self._add_declare_node(node,
                                                   var_name=field_node.var_name(),
                                                   var_type="Tag")

        # Search for the last declaration node and initialize our field variable there
        last_declare_node = self._find_last_node_below(field_handle_node, DeclareVariable)
        field_node.children = last_declare_node.children
        field_node.parent = last_declare_node

    def _find_last_node_below(self, node, last_node_type):
        child = node.children[0]

        if not isinstance(child, last_node_type):
            return node
        else:
            return self._find_last_node_below(child, last_node_type)

    def _find_node_above(self, node, above_node_type):
        parent = node.parent
        if isinstance(parent, above_node_type):
            return parent
        else:
            return self._find_node_above(parent, above_node_type)
