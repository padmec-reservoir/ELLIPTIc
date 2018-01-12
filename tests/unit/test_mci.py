import pytest

from elliptic.Kernel.MeshComputeInterface import MCI
from elliptic.Kernel.MeshComputeInterface.Expression import (Selector,
                                                             Computer, Manager)


@pytest.fixture()
def mci(request):
    mci_ = MCI()

    return mci_


class TestExpression:

    class DummyDilute(Selector.Dilute):
        name = "Dilute"
        pass

    class DummyFilter(Selector.Filter):
        name = "Filter"
        pass

    class DummyMap(Computer.Map):
        name = "Map"
        pass

    class DummyReduce(Computer.Reduce):
        name = "Reduce"
        pass

    def test_IR_build(self, mci):
        with mci.root() as root:
            res1 = root(self.DummyDilute,
                        val1=1,
                        val2=2)(self.DummyFilter,
                                val3=3,
                                val4=4)
            res2 = res1(self.DummyMap,
                        val1=2)(self.DummyReduce,
                                val3=3,
                                val4=4)
            res3 = res1(self.DummyMap,
                        val1=2)(self.DummyReduce,
                                val3=3,
                                val4=4)

        res1.export_tree("res1.png")
