"""Basically lots of integration tests with some unit tests."""
import numpy as np
import pytest

from Padmec.Kernel import (KernelBase, TPFA, check_kernel, fill_vector,
                           fill_matrix)
from Padmec.Mesh.MeshFactory import MeshFactory
from Padmec.Physical.PhysicalMap import PhysicalMap
from Padmec.Physical import Physical
from Padmec.Solver import MatrixManager


class TestKernel:
    def test_KernelBase_attributes_minus_one(self):
        k = KernelBase
        assert k.elem_dim == -1
        assert k.bridge_dim == -1
        assert k.target_dim == -1
        assert k.depth == -1

    def test_KernelBase_run_raises_NotImplementedError(self):
        k = KernelBase
        with pytest.raises(NotImplementedError):
            k.run(None, None, None)

    def test_check_kernel_raises_ValueError_when_elem_dim_not_set(self):
        class BadKernel(KernelBase):
            bridge_dim = 1
            target_dim = 1
            depth = 1
            solution_dim = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

    def test_check_kernel_raises_ValueError_when_bridge_dim_not_set(self):
        class BadKernel(KernelBase):
            elem_dim = 1
            target_dim = 1
            depth = 1
            solution_dim = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

    def test_check_kernel_raises_ValueError_when_target_dim_not_set(self):
        class BadKernel(KernelBase):
            elem_dim = 1
            bridge_dim = 1
            depth = 1
            solution_dim = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

    def test_check_kernel_raises_ValueError_when_depth_not_set(self):
        class BadKernel(KernelBase):
            elem_dim = 1
            bridge_dim = 1
            target_dim = 1
            solution_dim = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

    def test_check_kernel_raises_ValueError_when_solution_dim_not_set(self):
        class BadKernel(KernelBase):
            elem_dim = 1
            bridge_dim = 1
            target_dim = 1
            depth = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

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

    def test_run_kernel(self):
        self.m.run_kernel(self.tpfa)
