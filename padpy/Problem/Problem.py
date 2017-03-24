
class ProblemBase(object):

    def __init__(self, mesh, pipeline, solution_dim):
        self.mesh = mesh
        self.pipeline = pipeline
        self.solution_dim = solution_dim

    def run_pipeline(self):
        for kernel in self.pipeline:
            self.mesh.run_kernel(kernel)

    def fill_matrices(self):
        for matrix in self.mesh.matrix_manager.get_matrices():
            matrix.FillComplete()
