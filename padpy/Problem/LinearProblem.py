from Problem import ProblemBase
from PyTrilinos import Epetra, AztecOO


class LinearProblem(ProblemBase):

    def setup_linear_problem(self, A_name, b_name):
        self.A = self.mesh.matrix_manager.get_matrix(A_name)
        self.b = self.mesh.matrix_manager.get_vector(b_name)

        self.A.FillComplete()

        self.x = Epetra.Vector(
            self.mesh.matrix_manager.std_map[self.solution_dim])

        self.linearProblem = Epetra.LinearProblem(self.A, self.x, self.b)
        self.solver = AztecOO.AztecOO(self.linearProblem)

    def solve(self):
        self.solver.Iterate(10000, 1e-9)

    def export_solution(self, solution_name, file_name):
        self.mesh.create_double_solution_tag(solution_name)
        self.mesh.set_solution(solution_name, self.solution_dim, self.x)
        self.mesh.moab.write_file(file_name)
