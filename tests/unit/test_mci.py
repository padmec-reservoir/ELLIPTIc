import pytest

from elliptic.Kernel.MeshComputeInterface import MCI
from elliptic.Kernel.MeshComputeInterface.Expression import (Selector,
                                                             Computer, Manager)


@pytest.fixture()
def mci(request, elliptic_) -> MCI:
    mci_ = MCI(elliptic_)

    return mci_


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

    def test_IR_build(self, mci):

        with mci.root() as root:
            res1 = root(Selector.Dilute.ByEnt,
                        dim=1)(self.DummyFilter,
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

        res1.export_tree("res1.png")
