from types import ModuleType
from typing import List

from cypyler import TMPCypyler
from jinja2 import Template

from .TemplateManager import TemplateManagerBase
from .Context import Context
from .Expression import Expression

NODEGROUP_TEMPLATE = ("{% for node in node_templates %}"
                      "{{ node }}"
                      "{% endfor %}")


class TreeBuild:
    """Class responsible for processing a DSL tree and consolidating the generated Cython code.

    Parameters:
        template_manager: A template manager object.
        dsl_contract: A dsl contract object.
        libraries: A list containing any libraries that should be statically linked.
        include_dirs: A list containing extra include directories.
            `Cypyler` adds numpy includes by default.
    """
    build_dir_prefix = 'elliptic__'

    def __init__(self,
                 template_manager: TemplateManagerBase,
                 libraries: List[str]=None,
                 include_dirs: List[str]=None) -> None:
        self.template_manager = template_manager
        self.libraries = libraries
        self.include_dirs = include_dirs
        self.built_module: ModuleType = None

    def build(self, root: Expression) -> ModuleType:
        """Processes the DSL tree and returns the built Cython module.

        Parameters:
            root: The DSL tree root.
        """
        full_rendered_template = self._render_tree(node=root, context=Context())

        cp = TMPCypyler(self.build_dir_prefix, self.libraries, self.include_dirs)

        self.built_module = cp.build(full_rendered_template)

        return self.built_module

    def _render_tree(self, node: Expression, context: Context) -> str:
        children_rendered_templates: List[str] = []

        with node.visit(context) as context_delegate:
            child: Expression
            for child in node.children:
                built_node: str = self._render_tree(child, context)
                children_rendered_templates.append(built_node)

            group_template = Template(NODEGROUP_TEMPLATE)
            rendered_group = group_template.render(node_templates=children_rendered_templates)

            rendered_node = node.render(self.template_manager,
                                        rendered_group,
                                        context_delegate)
            context_delegate.child = rendered_group

        return rendered_node
