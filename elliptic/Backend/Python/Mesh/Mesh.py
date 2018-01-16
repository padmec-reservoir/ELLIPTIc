from types import ModuleType

from .PythonTemplateManager import PythonTemplateManager


class Grid:

    def __init__(self, nx, ny, nz, dx, dy, dz):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def get_coord(self, i, j, k):
        return [i * self.dx, j * self.dy, k * self.dz]


class MeshBuilder:

    def grid(self, nx, ny, nz, dx, dy, dz):
        return Grid(nx, ny, nz, dx, dy, dz)


class MeshBackend:

    def __init__(self, output_formats, report_format, fields):
        self.template_manager = PythonTemplateManager()

    def mesh_builder(self):
        return MeshBuilder()

    def get_template_manager(self) -> PythonTemplateManager:
        return self.template_manager

    def get_backend_builder(self) -> ModuleType:
        from . import build_functions
        return build_functions
