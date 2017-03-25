from PyTrilinos import Epetra

comm = Epetra.PyComm()


class ReadOnlyMatrix(object):
    """Matrix wrapper. Defines a read-only matrix. Also abstracts the usage
    of the id_map for accessing the matrix.

    """
    # TODO: Test me

    def __init__(self, matobj, id_map):
        self.mat = matobj
        self.id_map = id_map

    def __getitem__(self, key):
        return self.mat[self.id_map[key]]

    def __str__(self):
        return str(self.mat)


class MatrixManager(object):
    """Class responsible for managing matrices and vectors.

    Note
    ----
    This class is tightly coupled with the entire system. If you
    wish to extend it, you may need to replicate behavior from the Trilinos
    library.

    """
    def __init__(self):
        self.std_map = {}

        self.matrix = {}
        self.vector = {}

    def create_map(self, dim, len_elems):
        self.std_map[dim] = Epetra.Map(len_elems, 0, comm)

    def create_matrix(self, dim, name, share=False):
        if name not in self.matrix:
            # The last argument suppose that our meshes will be
            # mostly tetrahedral
            self.matrix[name] = Epetra.CrsMatrix(
                Epetra.Copy, self.std_map[dim], 5)
        elif not share:
            raise KeyError("Matrix name already defined and share "
                           "is set to False")

    def create_vector(self, dim, name, share=False):
        if name not in self.vector:
            self.vector[name] = Epetra.Vector(self.std_map[dim])
        elif not share:
            raise KeyError("Vector name already defined and share "
                           "is set to False")

    def get_matrix(self, name):
        return self.matrix[name]

    def get_matrices(self):
        return self.matrix.values()

    def get_vector(self, name):
        return self.vector[name]

    def fill_vector(self, name, row, value):
        self.vector[name][row] = value

    def fill_matrix(self, name, row, cols, values):
        self.matrix[name].InsertGlobalValues(row, values, cols)

    def sum_into_matrix(self, name, row, cols, values):
        self.matrix[name].SumIntoGlobalValues(row, values, cols)
