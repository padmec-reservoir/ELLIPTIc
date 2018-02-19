from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilderSubClass
from .Manager import Manager


class Matrix(Manager):

    def __init__(self):
        super().__init__()


class Create(Matrix):

    def __init__(self, field_name):
        super().__init__()

        self.field_name = field_name

        self.name = "Create Matrix"

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        return backend_builder.create_matrix_delegate(field_name=self.field_name)


class FillColumns(Matrix):

    def __init__(self, matrix):
        super().__init__()

        self.matrix = matrix

        self.name = "Fill Columns"

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        return backend_builder.fill_columns_delegate(matrix=self.matrix)


class FillDiag(Matrix):

    def __init__(self, matrix):
        super().__init__()

        self.matrix = matrix

        self.name = "Fill Diagonal"

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        return backend_builder.fill_diag_delegate(matrix=self.matrix)


class Solve(Matrix):

    def __init__(self):
        super().__init__()

        self.name = "Solve"

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        return backend_builder.solve_delegate()
