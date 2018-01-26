
class Elliptic:

    def __init__(self, mesh_backend, solver_backend):
        self.mesh_backend = mesh_backend
        self.solver_backend = solver_backend

        self._mesh = None

    def run_kernel(self, mci):
        kernel_module = mci.get_built_module()
        import pdb; pdb.set_trace()
        self.mesh_backend.run_kernel(kernel_module, self._mesh)

    def get_mesh_template_manager(self):
        return self.mesh_backend.get_template_manager()

    def get_mesh_backend_builder(self):
        return self.mesh_backend.get_backend_builder()

    def get_mesh_template_libs(self):
        return self.mesh_backend.get_libraries()

    def get_mesh_backend_include_dirs(self):
        return self.mesh_backend.get_include_dirs()

    def mesh_builder(self):
        return self.mesh_backend.mesh_builder()

    def set_mesh(self, mesh):
        self._mesh = mesh

    def tree_preprocess(self, root):
        self.mesh_backend.tree_preprocess(root)

    def export(self, filename):
        self.mesh_backend.export(self._mesh, filename)