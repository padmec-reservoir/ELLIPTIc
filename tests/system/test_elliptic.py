import pytest

from elliptic.Mesh.MeshFactory import MOABMeshFactory
from elliptic.Kernel import KernelBase


class TestingKernel(KernelBase):

    def compute(self, mci):
        from elliptic.Kernel.MeshComputeInterface.Selector import (
                EntitySelector)

        mci.selector(EntitySelector).by_dim(3)


class TestElliptic(object):

    @pytest.fixture(params=["1"])
    def mesh(self, request):
        # TODO: In the near future, modify this here to a .h5m filename
        # Possibly also make it so that the test would generate the final
        # preprocessed file automatically from the msh file.
        filename = f"tests/system/case_{request.param[0]}.msh"
        mf = MOABMeshFactory()
        mesh_obj = mf.load_mesh(filename)

        return mesh_obj

    def test_elliptic(self, mesh):
        kernel = TestingKernel()
        mesh.run_kernel(kernel)
