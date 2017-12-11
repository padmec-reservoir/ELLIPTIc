
class Elliptic:

    def __init__(self, mesh_backend, solver_backend):
        self.mesh_backend = mesh_backend
        self.solver_backend = solver_backend

        self._mesh = None

    def mesh_factory(self):
        return self.mesh_backend.mesh_factory()

    def set_mesh(self, mesh):
        self._mesh = mesh
