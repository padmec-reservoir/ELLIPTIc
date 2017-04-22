"""Basically lots of integration tests with some unit tests."""
import pytest

from elliptic.Kernel import KernelBase, TPFA
from elliptic.Kernel.EntityKernelMixins import (DimensionEntityKernelMixin,
                                                MeshSetEntityKernelMixin)
from elliptic.Mesh.MeshFactory import MeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Physical import Physical
from elliptic.Solver import MatrixManager


class TestKernelBase:

    def test_run_raises_NotImplementedError(self):
        k = KernelBase
        with pytest.raises(NotImplementedError):
            k.run(None, None)

    def test_get_elements_raises_NotImplementedError(self):
        k = KernelBase
        with pytest.raises(NotImplementedError):
            k.get_elements(None)

    def test_test_kernel(self):
        k = KernelBase
        assert not k.check_kernel()


class TestDimensionEntityKernelMixin:

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
        k = DimensionEntityKernelMixin
        with pytest.raises(ValueError):
            k.check_kernel()

    def test_subclass_not_raises_ValueError(self):
        class DimensionEntityKernelMixin_subclass(DimensionEntityKernelMixin):
            entity_dim = 1

        k = DimensionEntityKernelMixin_subclass
        k.check_kernel()

    def test_get_elements(self):
        class DimensionEntityKernelMixin_dim1(DimensionEntityKernelMixin):
            entity_dim = 1

        class DimensionEntityKernelMixin_dim2(DimensionEntityKernelMixin):
            entity_dim = 2

        class DimensionEntityKernelMixin_dim3(DimensionEntityKernelMixin):
            entity_dim = 3

        assert len(DimensionEntityKernelMixin_dim1.get_elements(self.m)) == 191
        assert len(DimensionEntityKernelMixin_dim2.get_elements(self.m)) == 255
        assert len(DimensionEntityKernelMixin_dim3.get_elements(self.m)) == 107


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
