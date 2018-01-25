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

    def test_IR_build(self, mci, mesh, elliptic_):

        with mci.root() as root:
            res1 = root(Selector.Dilute.ByEnt,
                        dim=3)(Selector.Filter.Where,
                               is_boundary=False)
            res2 = res1(Computer.Map,
                        function="get_centroid",
                        arg1="arg1",
                        arg2="arg2")

            res1.export_tree('res1.png')

        elliptic_.run_kernel(mci, mesh)
