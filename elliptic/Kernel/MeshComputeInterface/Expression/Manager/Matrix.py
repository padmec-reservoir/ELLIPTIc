from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilder
from .Manager import Manager


class Matrix(Manager):

    def __init__(self):
        super().__init__()


class Create(Matrix):

    def __init__(self, field_name):
        super().__init__()

        self.field_name = field_name

        self.name = "Create Matrix"

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.create_matrix_delegate(context=context, field_name=self.field_name)


class FillColumns(Matrix):

    def __init__(self, matrix):
        super().__init__()

        self.matrix_id = matrix.unique_id

        self.name = "Fill Columns"

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.fill_columns_delegate(context=context, matrix=self.matrix_id)


class FillDiag(Matrix):

    def __init__(self, matrix):
        super().__init__()

        self.matrix_id = matrix.unique_id

        self.name = "Fill Diagonal"

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.fill_diag_delegate(context=context, matrix=self.matrix_id)


class Solve(Matrix):

    def __init__(self):
        super().__init__()

        self.name = "Solve"

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.solve_delegate(context=context)
