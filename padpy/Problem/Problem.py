
class ProblemBase(object):
    """Defines a type of problem. A problem can expose many set-up methods
    or optional steps associated with solving the given kind of problem. A
    Runner should be associated with the finite steps of interest.

    A problem should be loosely coupled with the Pipeline class, in the sense
    that it must not depend on what kernels are present on the pipeline.

    A problem might need to be tightly coupled with the MatrixManager class, or
    with the Trilinos library.

    Parameters
    ----------
    mesh: padpy.Mesh.Mesh.Mesh
        Mesh to be used in this problem.
    pipeline: padpy.Problem.Pipeline.Pipeline
        Pipeline to be used in this problem.
    solution_dim: unsigned int
        Dimension of the target solution.

    """
    def __init__(self, mesh, pipeline, solution_dim):
        self.mesh = mesh
        self.pipeline = pipeline
        self.solution_dim = solution_dim

    def run_pipeline(self):
        """Runs this problem's pipeline.

        """
        for kernel in self.pipeline:
            self.mesh.run_kernel(kernel)

    def fill_matrices(self):
        """Fill all the matrices associated with this problem.

        """
        for matrix in self.mesh.matrix_manager.get_matrices():
            matrix.FillComplete()
