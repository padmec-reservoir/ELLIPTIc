import pytest


from elliptic.Kernel.MeshComputeInterface import MeshComputeInterface as mci
from elliptic.Kernel.MeshComputeInterface.Selector import EntitySelector


class TestMeshComputeInterface:
    pass


class TestSelector:

    @pytest.fixture()
    def mci_inst(self):
        return mci()

    def test_EntitySelector(self, mci_inst):
        mci_inst.selector(EntitySelector).by_dim(3)

        mci_inst._build_context()
