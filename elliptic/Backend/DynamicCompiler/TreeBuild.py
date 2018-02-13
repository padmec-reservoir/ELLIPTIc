import os
import tempfile
from types import ModuleType
from typing import List

from jinja2 import Environment, PackageLoader, Template

from .utils import (build_extension, elliptic_cythonize,
                    import_extension)
from elliptic.Kernel.MeshComputeInterface.Expression import (StatementRoot,
                                                             ExpressionBase)


class TemplateManagerBase:

    def __init__(self, package: str, templates_folder: str) -> None:
        self.jinja2_env = Environment(
            loader=PackageLoader(package, templates_folder))

    def get_template(self, template_file: str) -> Template:
        return self.jinja2_env.get_template(template_file)

    def render(self, template_file: str, **kwargs: str) -> str:
        template = self.get_template(template_file)
        return template.render(**kwargs)


class EllipticTemplateManager:
    jinja2_env = Environment(loader=PackageLoader(__package__, 'Templates'))

    @classmethod
    def get_template(cls, template_file):
        return cls.jinja2_env.get_template(template_file)

    @classmethod
    def render(cls, template_file, **kwargs):
        template = cls.get_template(template_file)
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

    def build(self, root: StatementRoot) -> ModuleType:
        cython_dir = tempfile.mkdtemp(prefix=self.build_dir_prefix)
        module_fd, module_path = tempfile.mkstemp(
            suffix='.pyx', dir=cython_dir)

        module_name = module_path.split('/')[-1].strip('.pyx')

        full_rendered_template = self._render_tree(node=root, context={})

        with os.fdopen(module_fd, 'w') as f:
            f.write(full_rendered_template)

        extensions = elliptic_cythonize(module_name, module_path,
                                        include_dirs=self.include_dirs,
                                        libraries=self.libraries)

        built_ext = build_extension(extensions[0], cython_dir)
        ext_path = built_ext.get_ext_fullpath(module_name)

        self.built_module = import_extension(module_name, ext_path)

        return self.built_module

    def _render_tree(self, node: ExpressionBase, context) -> str:
        children_rendered_templates: List[str] = []

        with node.visit(self.backend_builder, context) as context_delegate:

            child: ExpressionBase
            for child in node.children:
                built_node: str = self._render_tree(child, context)
                children_rendered_templates.append(built_node)

            group_template = EllipticTemplateManager.get_template("nodegroup.etp")
            rendered_group = group_template.render(node_templates=children_rendered_templates)

            rendered_node = node.render(self.template_manager,
                                        rendered_group,
                                        context_delegate,
                                        context)

        return rendered_node
