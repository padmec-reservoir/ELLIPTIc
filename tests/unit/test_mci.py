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
    import os
    mesh_filename = os.path.join(os.path.dirname(__file__), 'cube_small.h5m')
    mesh_ = elliptic_.mesh_builder().read_file(mesh_filename)

    elliptic_.set_mesh(mesh_)

    return mesh_


class TestExpression:

    def test_IR_build(self, mci, mesh, elliptic_):

        with mci.root() as root:
            internal_ents = root(Selector.Dilute.ByEnt, dim=3)(Selector.Filter.Where, is_boundary=False)

            scalar = internal_ents(Computer.Map.PutScalar,
                                   value=5.0)
            scalar(Manager.PutField, field_name="PRES")

            field = internal_ents(Computer.Map.GetField,
                                  field_name="TEST_FIELD")
            field(Manager.PutField, field_name="SAT")

            internal_ents.export_tree('res1.png')

        elliptic_.run_kernel(mci)

        #elliptic_.export('test.h5m')
