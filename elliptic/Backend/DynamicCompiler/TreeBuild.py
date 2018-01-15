import os
import tempfile
from types import ModuleType
from typing import List

from jinja2 import Environment, PackageLoader, Template

from .utils import (build_extension, elliptic_cythonize,
                    import_extension)
from elliptic.Kernel.MeshComputeInterface.Expression import (StatementRoot,
                                                             ExpressionBase,
                                                             EllipticNode)


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

    def __init__(self, template_manager: TemplateManagerBase) -> None:
        self.template_manager = template_manager

    def build(self, root: StatementRoot) -> ModuleType:
        cython_dir = tempfile.mkdtemp(prefix=self.build_dir_prefix)
        module_fd, module_path = tempfile.mkstemp(
            suffix='.pyx', dir=cython_dir)

        module_name = module_path.split('/')[-1].strip('.pyx')

        full_rendered_template = self._render_tree(root)

        with os.fdopen(module_fd, 'w') as f:
            f.write(full_rendered_template)

        extensions = elliptic_cythonize(module_name, module_path)

        built_ext = build_extension(extensions[0], cython_dir)
        ext_path = built_ext.get_ext_fullpath(module_name)

        self.built_module = import_extension(module_name, ext_path)

        return self.built_module

    def _render_tree(self, node: EllipticNode) -> str:
        child: ExpressionBase
        node_templates: List[str] = []

        for child in node.children:
            built_node: str = self._render_tree(child)
            node_templates.append(built_node)

        return node.render(self.template_manager, node_templates)
