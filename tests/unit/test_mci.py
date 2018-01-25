import pytest

from elliptic.Kernel.MeshComputeInterface import MCI
from elliptic.Kernel.MeshComputeInterface.Expression import (Selector,
                                                             Computer, Manager)


@pytest.fixture()
def mci(request, elliptic_) -> MCI:
    mci_ = MCI(elliptic_)

    return mci_


@pytest.fixture()
def mesh(request, elliptic_):
    mesh_ = elliptic_.mesh_builder().read_file('tests/cube_small.h5m')

    return mesh_


class TestExpression:

    class DummyFilter(Selector.Filter.Filter):
        name = "Filter"

        def __init__(self, val3, val4):
            super().__init__()

    class DummyMap(Computer.Map.Map):
        name = "Map"

        def __init__(self, val1):
            super().__init__()

    class DummyReduce(Computer.Reduce.Reduce):
        name = "Reduce"

        def __init__(self, val3, val4):
            super().__init__()

    def test_IR_build(self, mci, mesh, elliptic_):

        with mci.root() as root:
            res1 = root(Selector.Dilute.ByEnt,
                        dim=3)(self.DummyFilter,
                                val3=3,
                                val4=4)
            res2 = res1(self.DummyMap,
                        val1=2)(self.DummyReduce,
                                val3=3,
                                val4=4)
            res3 = res1(self.DummyReduce,
                        val3=3,
                        val4=4)(self.DummyMap,
                                val1=2)

        elliptic_.run_kernel(mci, mesh)
