import os
import tempfile

from jinja2 import Environment, PackageLoader

from .DynamicCompiler.utils import (build_extension, elliptic_cythonize,
                                    import_extension)


class TemplatedInterface:

    def __init__(self):
        pass

    def render(self, **kwargs):
        self.template.render(**kwargs)


class Context:

    build_dir_prefix = 'elliptic__'

    def __init__(self):
        self.built_module = None

        self.jinja2_env = Environment(
            loader=PackageLoader(__package__, 'Templates'))

    def get_template(self, template_file):
        return self.jinja2_env.get_template(template_file)

    def compile_tree(self):
        cython_dir = tempfile.mkdtemp(prefix=self.build_dir_prefix)
        module_fd, module_path = tempfile.mkstemp(
            suffix='.pyx', dir=cython_dir)

        module_name = module_path.split('/')[-1].strip('.pyx')

        full_rendered_template = self.build_template()

        with os.fdopen(module_fd, 'w') as f:
            f.write(full_rendered_template)

        extensions = elliptic_cythonize(module_name, module_path)

        built_ext = build_extension(extensions[0], cython_dir)
        ext_path = built_ext.get_ext_fullpath(module_name)

        self.built_module = import_extension(module_name, ext_path)

    def build_template(self):
        # TODO: Iterate on tree and create a single full template
        pass


class MeshComputeInterface:

    def __init__(self, context=None):
        if not context:
            self.context = Context()
        else:
            self.context = context

    def selector(self, selector_class):
        pass
