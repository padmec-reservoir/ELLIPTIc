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
        with mci.selection() as s:
            res1 = s(self.DummyDilute,
                     val1=1,
                     val2=2)(self.DummyFilter,
                             val3=3,
                             val4=4)

        with mci.selection() as s:
            res2 = s(self.DummyDilute, val1=1, val2=2)
            res2 = res2(self.DummyFilter, val3=3, val4=4)

        res1.export_tree("res1.png")
        res2.export_tree("res2.png")

        assert res1.root.descendants == res2.root.descendants

        with mci.computation() as c:
            res3 = c(self.DummyMap,
                     grouping=res1,
                     val1=2)(self.DummyReduce,
                             val3=3,
                             val4=4)

            res4 = c(self.DummyMap, grouping=res2, val2=2)
            res4 = res4(self.DummyReduce, val3=3, val4=4)

            assert res3 == res4

        with mci.management() as m:
            pass
