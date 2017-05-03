from Problem import ProblemBase
from PyTrilinos import Epetra, AztecOO


class LinearProblem(ProblemBase):
    """Defines a linear problem abstraction for use with the AztecOO linear
    solver, to solve problems of the format Ax = b. This class needs the names
    for the A matrix and b vector, to be colected from the MatrixManager
    class.

    """
    def setup_linear_problem(self, A_name, b_name):
        """Sets a linear problem. The `A_name` and `b_name` parameters are
        related to the matrix and vectors names to be used in a linear problem
        Ax = b.

        """
        self.A = self.mesh.matrix_manager.get_matrix(A_name)
        self.b = self.mesh.matrix_manager.get_vector(b_name)

        self.A.FillComplete()

        self.x = Epetra.Vector(
            self.mesh.matrix_manager.std_map[self.solution_dim])

        self.linearProblem = Epetra.LinearProblem(self.A, self.x, self.b)
        self.solver = AztecOO.AztecOO(self.linearProblem)
        self.solver.SetAztecOption(AztecOO.AZ_output, AztecOO.AZ_last)

    def solve(self):
        self.solver.Iterate(10000, 1e-9)

    def export_solution(self, solution_name, file_name):
        """Exports the problem solution using the MOAB exporter.

        Parameters
        ----------
        solution_name: string
            Name of the solution found when solving the linear problem.
        file_name: string
            Path to the output file to be created, which will hold the mesh
            and the solution.

        """
        self.mesh.create_double_solution_tag(solution_name)
        self.mesh.set_solution(solution_name, self.solution_dim, self.x)
        self.mesh.moab.write_file(file_name)
