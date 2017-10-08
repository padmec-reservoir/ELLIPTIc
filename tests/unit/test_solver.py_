import pytest

from elliptic.Solver import MatrixManager, ReadOnlyMatrix


class TestMatrixManager:

    def setup(self):
        self.matrix_manager = MatrixManager()
        self.matrix_manager.create_map(0, 10)

    def test_ReadOnlyMatrix(self):
        id_map = {
            0: 1,
            1: 2,
            2: 0
        }
        matobj = [100, 200, 300]

        A = ReadOnlyMatrix(matobj, id_map)

        assert A[0] == 200
        assert A[1] == 300
        assert A[2] == 100

        with pytest.raises(TypeError):
            A[0] = 5

        assert str(A) == str(matobj)

    def test_MatrixManager_create_matrix(self):
        self.matrix_manager.create_matrix(0, 'A', False)
        self.matrix_manager.create_matrix(0, 'B', True)

        with pytest.raises(KeyError):
            self.matrix_manager.create_matrix(0, 'A', False)

        with pytest.raises(KeyError):
            self.matrix_manager.create_matrix(0, 'B', False)

        with pytest.raises(KeyError):
            self.matrix_manager.create_matrix(0, 'A', True)

        self.matrix_manager.create_matrix(0, 'B', True)

    def test_MatrixManager_create_vector(self):
        self.matrix_manager.create_vector(0, 'A', False)
        self.matrix_manager.create_vector(0, 'B', True)

        with pytest.raises(KeyError):
            self.matrix_manager.create_vector(0, 'A', False)

        with pytest.raises(KeyError):
            self.matrix_manager.create_vector(0, 'B', False)

        with pytest.raises(KeyError):
            self.matrix_manager.create_vector(0, 'A', True)

        self.matrix_manager.create_vector(0, 'B', True)

    def test_MatrixManager_get_matrix(self):
        self.matrix_manager.create_matrix(0, 'A', False)
        self.matrix_manager.create_matrix(0, 'B', True)
        self.matrix_manager.create_matrix(0, 'B', True)

        self.matrix_manager.get_matrix('A')

        matrices = self.matrix_manager.get_matrices()
        assert len(matrices) == 2

        vectors = self.matrix_manager.get_vectors()
        assert len(vectors) == 0

    def test_MatrixManager_get_vector(self):
        self.matrix_manager.create_vector(0, 'A', False)
        self.matrix_manager.create_vector(0, 'B', True)
        self.matrix_manager.create_vector(0, 'B', True)

        self.matrix_manager.get_vector('A')

        vectors = self.matrix_manager.get_vectors()
        assert len(vectors) == 2

        matrices = self.matrix_manager.get_matrices()
        assert len(matrices) == 0

    def test_MatrixManager_fill_matrix(self):
        self.matrix_manager.create_matrix(0, 'A', False)
        self.matrix_manager.fill_matrix('A', 1, [1, 2], [100, 200])

        A = self.matrix_manager.get_matrix('A')
        A.FillComplete()
        assert A[1, 1] == 100
        assert A[1, 2] == 200

    def test_MatrixManager_sum_into_matrix(self):
        self.matrix_manager.create_matrix(0, 'A', False)
        self.matrix_manager.fill_matrix('A', 1, [1, 2], [100, 200])
        self.matrix_manager.sum_into_matrix('A', 1, [1, 2], [100, 200])

        A = self.matrix_manager.get_matrix('A')
        A.FillComplete()
        assert A[1, 1] == 200
        assert A[1, 2] == 400

    def test_MatrixManager_fill_vector(self):
        self.matrix_manager.create_vector(0, 'A', False)
        self.matrix_manager.fill_vector('A', 1, 200)
        self.matrix_manager.fill_vector('A', 2, 300)

        A = self.matrix_manager.get_vector('A')
        assert A[1] == 200
        assert A[2] == 300

    def swap_vector(self, vector1_name, vector2_name):
        vec1 = self.get_vector(vector1_name)
        vec2 = self.get_vector(vector2_name)
        self.vector[vector1_name] = vec2
        self.vector[vector2_name] = vec1

    def test_MatrixManager_swap_vector(self):
        self.matrix_manager.create_vector(0, 'A', False)
        self.matrix_manager.create_vector(0, 'B', False)

        vec1 = self.matrix_manager.get_vector('A')
        vec2 = self.matrix_manager.get_vector('B')

        self.matrix_manager.swap_vector('A', 'B')

        assert vec1 is self.matrix_manager.get_vector('B')
        assert vec2 is self.matrix_manager.get_vector('A')
