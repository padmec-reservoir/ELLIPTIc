from .Problem import ProblemBase
from PyTrilinos import Epetra, AztecOO


class LinearProblem(object):
    """Defines a linear problem abstraction for use with the AztecOO linear
    solver, to solve problems of the format Ax = b. This class needs the names
    for the A matrix and b vector, to be colected from the MatrixManager
    class.

    """
    def __init__(self, mesh, lhs_kernel, rhs_kernel, solution_name):
        self.mesh = mesh
        self.solution_name = solution_name

        self.lhs_kernel = lhs_kernel
        self.rhs_kernel = rhs_kernel

    def run_problem(self):
        self.mesh.run_kernel_recur(self.rhs_kernel)
        self.mesh.run_kernel_recur(self.lhs_kernel)

        self.solve_linear_problem()

        self.set_solution()

    def set_solution(self):
        solution_handle = self.mesh.create_field(self.solution_name)
        self.mesh.set_field_value(
            solution_handle, self.rhs_kernel.get_elements(), self.x)

    def solve_linear_problem(self):
        LHS = self.mesh.matrix_manager.get_matrix(self.lhs_kernel.array_name)
        LHS.FillComplete()

        rhs_field_handle = self.mesh.get_field(self.rhs_kernel.field_name)
        rhs_field = self.mesh.get_field_value(
            rhs_field_handle, self.rhs_kernel.get_elements())

        self.x = Epetra.Vector(
            self.mesh.matrix_manager.std_map[self.lhs_kernel.solution_dim])

        linearProblem = Epetra.LinearProblem(LHS, self.x, rhs_field)
        solver = AztecOO.AztecOO(linearProblem)
        solver.SetAztecOption(AztecOO.AZ_output, AztecOO.AZ_last)

        solver.Iterate(10000, 1e-9)

    def solve(self):
        self.solver.Iterate(10000, 1e-9)

        field = self.mesh.get_field(self.solution_name)
        ents = self.mesh.dimension_entities(self.solution_dim)
        self.mesh.set_field_value(field, ents, self.x)

    def export_solution(self, file_name):
        self.mesh.moab.write_file(file_name)
