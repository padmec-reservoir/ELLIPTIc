from PyTrilinos import Epetra

comm = Epetra.PyComm()


class MatrixManager(object):
    def __init__(self):
        self.std_map = {}

        self.matrix = {}
        self.vector = {}

    def create_map(self, dim, len_elems):
        self.std_map[dim] = Epetra.Map(len_elems, 0, comm)

    def create_matrix(self, dim, name):
        if name not in self.matrix:
            # The last argument suppose that our meshes will be
            # mostly tetrahedral
            self.matrix[name] = Epetra.CrsMatrix(
                Epetra.Copy, self.std_map[dim], 5)
        else:
            raise KeyError("Matrix name already defined")

    def create_vector(self, dim, name):
        if name not in self.vector:
            self.vector[name] = Epetra.Vector(self.std_map[dim])
        else:
            raise KeyError("Vector name already defined")

    def get_matrix(self, name):
        return self.matrix[name]

    def get_vector(self, name):
        return self.vector[name]

    def fill_vector(self, name, row, value):
        self.vector[name][row] = value

    def fill_matrix(self, name, row, cols, values):
        self.matrix[name].InsertGlobalValues(row, values, cols)

    def sum_into_matrix(self, name, row, cols, values):
        self.vector[name].SumIntoGlobalValues(row, values, cols)
