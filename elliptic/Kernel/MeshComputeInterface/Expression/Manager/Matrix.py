from .Manager import Manager


class Matrix(Manager):

    def __init__(self):
        super().__init__()


class Create(Matrix):

    def __init__(self, field_name):
        super().__init__()

        self.field_name = field_name

        self.name = "Create Matrix"


class FillColumns(Matrix):

    def __init__(self, matrix):
        super().__init__()

        self.matrix = matrix

        self.name = "Fill Columns"


class FillDiag(Matrix):

    def __init__(self, matrix):
        super().__init__()

        self.matrix = matrix

        self.name = "Fill Diagonal"


class Solve(Matrix):

    def __init__(self):
        super().__init__()

        self.name = "Solve"
