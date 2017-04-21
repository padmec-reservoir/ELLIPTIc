"""Basically lots of integration tests with some unit tests."""
import pytest

from elliptic.Kernel import (KernelBase, DimensionEntityKernel, TPFA,
                             fill_vector, fill_matrix)
from elliptic.Mesh.MeshFactory import MeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Physical import Physical
from elliptic.Solver import MatrixManager


class TestKernelBase:

    def test_run_raises_NotImplementedError(self):
        k = KernelBase
        with pytest.raises(NotImplementedError):
            k.run(None, None, None)

    def test_get_elements_raises_NotImplementedError(self):
        k = KernelBase
        with pytest.raises(NotImplementedError):
            k.get_elements()

    def test_test_kernel(self):
        k = KernelBase
        assert not k.check_kernel()

    def test_fill_vector_kernel_with_name(self):
        @fill_vector('my_name')
        class FillVectorKernel(KernelBase):
            pass

        assert FillVectorKernel.name == 'my_name'

    def test_fill_vector_kernel_without_name(self):
        @fill_vector('')
        class FillVectorKernel(KernelBase):
            pass

        assert FillVectorKernel.name == 'FillVectorKernel'

    def test_fill_matrix_kernel_with_name(self):
        @fill_matrix('my_name')
        class FillMatrixKernel(KernelBase):
            pass

        assert FillMatrixKernel.name == 'my_name'

    def test_fill_matrix_kernel_without_name(self):
        @fill_matrix()
        class FillMatrixKernel(KernelBase):
            pass

        assert FillMatrixKernel.name == 'FillMatrixKernel'

    def test_fill_matrix_kernel_with_same_names_raises_KeyError(self):
        matrix_manager = MatrixManager()
        matrix_manager.create_map(0, 0)

        @fill_matrix()
        class FillMatrixKernel(KernelBase):
            solution_dim = 0

        @fill_matrix('FillMatrixKernel')
        class FillMatrixKernel2(KernelBase):
            solution_dim = 0

        FillMatrixKernel.create_array(matrix_manager)

        with pytest.raises(KeyError):
            FillMatrixKernel2.create_array(matrix_manager)

    def test_fill_vector_kernel_with_same_names_raises_KeyError(self):
        matrix_manager = MatrixManager()
        matrix_manager.create_map(0, 0)

        @fill_vector()
        class FillVectorKernel(KernelBase):
            solution_dim = 0

        @fill_vector('FillVectorKernel')
        class FillVectorKernel2(KernelBase):
            solution_dim = 0

        FillVectorKernel.create_array(matrix_manager)

        with pytest.raises(KeyError):
            FillVectorKernel2.create_array(matrix_manager)


class TestDimensionEntityKernel:

    def setup(self):
        self.physical = PhysicalMap()
        self.physical[101] = Physical.Dirichlet(1.0)
        self.physical[102] = Physical.Dirichlet(-1.0)
        self.physical[103] = Physical.Symmetric()
        self.physical[50] = TPFA.TPFAPermeability(1.0)

        meshfile = 'tests/cube_small.h5m'
        mf = MeshFactory()
        self.m = mf.load_mesh(meshfile, self.physical)

    def test_check_kernel_raises_ValueError(self):
        k = DimensionEntityKernel
        with pytest.raises(ValueError):
            k.check_kernel()

    def test_subclass_not_raises_ValueError(self):
        class DimensionEntityKernel_subclass(DimensionEntityKernel):
            entity_dim = 1

        k = DimensionEntityKernel_subclass
        k.check_kernel()

    def test_get_elements(self):
        class DimensionEntityKernel_dim1(DimensionEntityKernel):
            entity_dim = 1

        class DimensionEntityKernel_dim2(DimensionEntityKernel):
            entity_dim = 2

        class DimensionEntityKernel_dim3(DimensionEntityKernel):
            entity_dim = 3

        assert len(DimensionEntityKernel_dim1.get_elements(self.m)) == 191
        assert len(DimensionEntityKernel_dim2.get_elements(self.m)) == 255
        assert len(DimensionEntityKernel_dim3.get_elements(self.m)) == 107


class TestTPFA:

    def setup(self):
        self.physical = PhysicalMap()
        self.physical[101] = Physical.Dirichlet(1.0)
        self.physical[102] = Physical.Dirichlet(-1.0)
        self.physical[103] = Physical.Symmetric()
        self.physical[50] = TPFA.TPFAPermeability(1.0)

        meshfile = 'tests/cube_small.h5m'
        mf = MeshFactory()
        self.m = mf.load_mesh(meshfile, self.physical)

        self.tpfa = TPFA.TPFAKernel

    def test_tpfa(self):
        self.m.run_kernel(self.tpfa)
