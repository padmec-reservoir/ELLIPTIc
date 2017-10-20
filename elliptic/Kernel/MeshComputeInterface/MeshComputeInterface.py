import os
import tempfile

from jinja2 import Environment, PackageLoader

from .DynamicCompiler.utils import (build_extension, elliptic_cythonize,
                                    import_extension)


class TemplateManager:

    jinja2_env = Environment(loader=PackageLoader(__package__, 'Templates'))

    def get_template(self, template_file):
        return self.jinja2_env.get_template(template_file)

    def render(self, template_file, **kwargs):
        template = self.get_template(template_file)
        return template.render(**kwargs)


class ContextNode:

    # Overwrite for extending with your own templates
    template_manager = TemplateManager()

    def __init__(self):
        self._template_file = ""
        self._template_args = {}
        self._child_rendered_template = ""

        self.child_node_group = None

    def set_template_file(self, template_file):
        self._template_file = template_file

    def set_options(self, **kwargs):
        self._template_args.update(kwargs)

    def set_child_node_group(self, child_node_group):
        # child_node_group is a NodeGroup instance
        self.child_node_group = child_node_group

    def _render(self):
        if self.child_node_group:
            self._child_rendered_template = self.child_node_group._render()

        kwargs = self._template_args

        return self.template_manager.render(
                template_file=self._template_file,
                child=self._child_rendered_template,
                **kwargs)


class NodeGroup:

    # Overwrite for extending with your own templates
    template_manager = TemplateManager()
    template_file = "nodegroup.pyx.etp"

    def __init__(self):
        self.nodes = []  # ContextNodes

    def add_node(self, context_node):
        self.nodes.append(context_node)

    def _render(self):
        node_templates = []  # Strings

        for node in self.nodes:
            node_templates.append(node._render())

        return self.template_manager.render(
                template_file=self.template_file,
                node_templates=node_templates)


class Context:

    build_dir_prefix = 'elliptic__'
    base_template = 'base.pyx.etp'
    context_root_class = NodeGroup
    template_manager = TemplateManager()

    def __init__(self):
        self.built_module = None
        self.root_node_group = self.context_root_class()

    def compile_tree(self):
        cython_dir = tempfile.mkdtemp(prefix=self.build_dir_prefix)
        module_fd, module_path = tempfile.mkstemp(
            suffix='.pyx', dir=cython_dir)

        module_name = module_path.split('/')[-1].strip('.pyx')

        full_rendered_template = self._render_tree()

        with os.fdopen(module_fd, 'w') as f:
            f.write(full_rendered_template)

        extensions = elliptic_cythonize(module_name, module_path)

        built_ext = build_extension(extensions[0], cython_dir)
        ext_path = built_ext.get_ext_fullpath(module_name)

        self.built_module = import_extension(module_name, ext_path)

        return self.built_module

    def _render_tree(self):
        rendered_tree = self.root_node_group._render()

        rendered_base = self.template_manager.render(self.base_template,
                                                     child=rendered_tree)

        return rendered_base


class MeshComputeInterface:

    context_class = Context

    def __init__(self):
            self.context = self.context_class()

    def selector(self, selector_class=None):
        if not selector_class:
            from .Selector import EntitySelector
            selector_class = EntitySelector

        selector_obj = selector_class(node_group=self.context.root_node_group)

        return selector_obj

    def _build_context(self):
        return self.context.compile_tree()


class ComputeBase:

    context_node_class = ContextNode
    node_group_class = NodeGroup

    def __init__(self, node_group):
        self.current_node_group = node_group

        self._called = False

    def set_template(self, context_node, template_file, options):
        context_node.set_template_file(template_file)
        context_node.set_options(**options)
