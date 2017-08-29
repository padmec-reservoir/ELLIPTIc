
class ProblemBase(object):
    def __init__(self, mesh, kernel, solution_dim):
        self.mesh = mesh
        self.kernel = kernel
        self.solution_dim = solution_dim

    def run_problem(self):
        """Runs this problem's pipeline.

        """
        self.mesh.run_kernel_recur(self.kernel)
