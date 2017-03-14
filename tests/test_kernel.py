import numpy
import pytest

from Padmec.Kernel import (KernelBase, TPFA, check_kernel, preprocess,
                           fill_matrix)
from Padmec.Mesh.MeshFactory import MeshFactory
from Padmec.Physical.PhysicalMap import PhysicalMap
from Padmec.Physical import Physical


class TestKernel:
    def test_KernelBase_attributes_minus_one(self):
        k = KernelBase
        assert k.elem_dim == -1
        assert k.bridge_dim == -1
        assert k.target_dim == -1
        assert k.depth == -1

    def test_KernelBase_call_raises_NotImplementedError(self):
        k = KernelBase
        with pytest.raises(NotImplementedError):
            k.run_kernel(None)

    def test_check_kernel_raises_ValueError_when_elem_dim_not_set(self):
        class BadKernel(KernelBase):
            bridge_dim = 1
            target_dim = 1
            depth = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

    def test_check_kernel_raises_ValueError_when_bridge_dim_not_set(self):
        class BadKernel(KernelBase):
            elem_dim = 1
            target_dim = 1
            depth = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

    def test_check_kernel_raises_ValueError_when_target_dim_not_set(self):
        class BadKernel(KernelBase):
            elem_dim = 1
            bridge_dim = 1
            depth = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)

    def test_check_kernel_raises_ValueError_when_depth_not_set(self):
        class BadKernel(KernelBase):
            elem_dim = 1
            bridge_dim = 1
            target_dim = 1

        with pytest.raises(ValueError):
            check_kernel(BadKernel)


class TestTPFA:
    """This is basically an integration test."""

    def setup(self):
        self.physical = PhysicalMap()
        self.physical[101] = Physical.Dirichlet(1.0)
        self.physical[102] = Physical.Dirichlet(-1.0)
        self.physical[103] = Physical.Symmetric()
        self.physical[50] = Physical.Permeability(numpy.eye(3))

        meshfile = 'tests/cube_small.h5m'
        mf = MeshFactory()
        self.m = mf.load_mesh(meshfile, self.physical)

        self.tpfa = TPFA

    def _test_run_kernel(self):
        self.m.run_kernel(self.tpfa)
