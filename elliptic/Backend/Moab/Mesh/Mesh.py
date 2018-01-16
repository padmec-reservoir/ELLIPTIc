from types import ModuleType

from .MoabTemplateManager import MoabTemplateManager


class MeshBuilder:
    pass
    #def load_file(self, filename: str) -> Mesh:
    #    pass


class MeshBackend:

    def __init__(self, output_formats, report_format, fields):
        self.template_manager = MoabTemplateManager()

    def run_kernel(self, tree) -> None:
        pass

    def get_template_manager(self) -> MoabTemplateManager:
        return self.template_manager

    def get_build_functions(self) -> ModuleType:
        from . import build_functions
        return build_functions
