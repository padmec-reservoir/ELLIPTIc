from collections import defaultdict
from types import ModuleType
from typing import List, TYPE_CHECKING

from cypyler import TMPCypyler
from jinja2 import Environment, PackageLoader, Template

if TYPE_CHECKING:
    from elliptic.Kernel.MeshComputeInterface.Expression import (StatementRoot,
                                                                 ExpressionBase)

NODEGROUP_TEMPLATE = ("{% for node in node_templates %}"
                      "{{ node }}"
                      "{% endfor %}")


class TemplateManagerBase:

    def __init__(self, package: str, templates_folder: str) -> None:
        self.jinja2_env = Environment(
            loader=PackageLoader(package, templates_folder))

    def get_template(self, template_file: str) -> Template:
        return self.jinja2_env.get_template(template_file)

    def render(self, template_file: str, **kwargs: str) -> str:
        template = self.get_template(template_file)
        return template.render(**kwargs)


class TreeBuild:
    build_dir_prefix = 'elliptic__'

    def __init__(self,
                 template_manager: TemplateManagerBase,
                 backend_builder,
                 libraries=None,
                 include_dirs=None) -> None:
        self.template_manager = template_manager
        self.backend_builder = backend_builder
        self.libraries = libraries
        self.include_dirs = include_dirs
        self.built_module: ModuleType = None

    def build(self, root: 'StatementRoot') -> ModuleType:
        full_rendered_template = self._render_tree(node=root, context=defaultdict(list))

        cp = TMPCypyler(self.build_dir_prefix, self.libraries, self.include_dirs)

        self.built_module = cp.build(full_rendered_template)

        return self.built_module

    def _render_tree(self, node: 'ExpressionBase', context) -> str:
        children_rendered_templates: List[str] = []

        with node.visit(self.backend_builder, context) as context_delegate:
            child: 'ExpressionBase'
            for child in node.children:
                built_node: str = self._render_tree(child, context)
                children_rendered_templates.append(built_node)

            group_template = Template(NODEGROUP_TEMPLATE)
            rendered_group = group_template.render(node_templates=children_rendered_templates)

            rendered_node = node.render(self.template_manager,
                                        rendered_group,
                                        context_delegate,
                                        context)

        return rendered_node
