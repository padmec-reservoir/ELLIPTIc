
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


class MeshFactory:

    def grid(self, nx, ny, nz, dx, dy, dz):
        return Grid(nx, ny, nz, dx, dy, dz)


class Mesh:

    def __init__(self, output_formats, report_format, fields):
        pass

    def mesh_factory(self):
        return MeshFactory()
