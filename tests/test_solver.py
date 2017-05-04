import pytest

from elliptic.Kernel import KernelBase
from elliptic.Solver import MatrixManager, ReadOnlyMatrix
from elliptic.Solver.Problem import LinearProblem, Pipeline, Problem, Runner


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


class TestRunner:

    def test_RunnerBase_run_raises_NotImplementedError(self):
        runner = Runner.RunnerBase('problem')

        assert runner.problem == 'problem'

        with pytest.raises(NotImplementedError):
            runner.run()

    def test_RunnerBase_run(self):
        class TestRunner(Runner.RunnerBase):

            def _run(self):
                pass

        runner = TestRunner('problem')

        runner.run()


class TestProblem:

    def test_run_pipeline(self):
        class DummyMesh:

            def run_kernel(self, kernel):
                kernel.ran = True

        class DummyKernel:

            def __init__(self):
                self.ran = False

        pipeline = [DummyKernel(), DummyKernel(), DummyKernel()]

        problem = Problem.ProblemBase(DummyMesh(), pipeline, None)

        problem.run_pipeline()

        assert all(kernel.ran for kernel in pipeline)

    def test_fill_matrices(self):
        class DummyMatrix:

            def __init__(self):
                self.filled = False

            def FillComplete(self):
                self.filled = True

        class DummyMatrixManager:

            def __init__(self):
                self.matrices = [DummyMatrix(), DummyMatrix(), DummyMatrix()]

            def get_matrices(self):
                return self.matrices

        class DummyMesh:

            def __init__(self):
                self.matrix_manager = DummyMatrixManager()

        mesh = DummyMesh()

        problem = Problem.ProblemBase(mesh, None, None)

        problem.fill_matrices()

        assert all(
            matrix.filled for matrix in mesh.matrix_manager.get_matrices())


class TestPipeline:

    def test_pipeline_or_pipeline(self):
        kernels1 = []
        for idx in range(5):

            class DummyKernel(KernelBase):
                c_id = idx

            kernels1.append(DummyKernel)

        kernels2 = []
        for idx in range(5, 10):

            class DummyKernel(KernelBase):
                c_id = idx

            kernels2.append(DummyKernel)

        pipeline1 = Pipeline(kernels1)
        pipeline2 = Pipeline(kernels2)
        pipeline = pipeline1 | pipeline2

        for idx, kernel in enumerate(pipeline):
            assert kernel.c_id == idx

    def test_pipeline_or_kernel(self):
        kernels = []
        for idx in range(5):

            class DummyKernel(KernelBase):
                c_id = idx

            kernels.append(DummyKernel)

        pipeline1 = Pipeline(kernels[0:4])
        pipeline = pipeline1 | kernels[4]

        for idx, kernel in enumerate(pipeline):
            assert kernel.c_id == idx

    def test_pipeline_raises_TypeError(self):
        class DummyClass:
            pass

        kernels = [DummyClass, DummyClass]

        with pytest.raises(TypeError):
            Pipeline(kernels)
