from .Problem import ProblemBase


class ExplicitProblem(ProblemBase):
    def __init__(self, mesh, kernel, solution_dim):
        super(ExplicitProblem, self).__init__(mesh, kernel, solution_dim)
        self.mesh = mesh
        self.kernel = kernel
        self.solution_dim = solution_dim

    def clear_mesh_ran_kernel(self):
        self.mesh.remove_ran_kernel(self.kernel)

    # TODO:
    #def export_solution(self, file_name):
    #    for kernel in self.pipeline:
    #        self.mesh.create_double_solution_tag(kernel.array_name)
    #        array = self.mesh.matrix_manager.get_vector(kernel.array_name)
    #        self.mesh.set_solution(
    #            kernel.array_name, kernel.solution_dim, array)
    #    self.mesh.moab.write_file(file_name)
