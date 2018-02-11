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

    def _test_IR_build(self, mci, elliptic_):

        with mci.root() as root:
            # Diluting
            internal_ents = root(Selector.Dilute.ByEnt, dim=3)
            internal_ents_centers = internal_ents(Computer.Map.GetCentroid)
            internal_ents_diff = internal_ents(Computer.Map.GetScalarField, field_name="DIFF")

            vols_adj_ents = internal_ents(Selector.Dilute.ByAdj, bridge_dim=2, to_dim=3)
            adj_vols_centers = vols_adj_ents(Computer.Map.GetCentroid)
            adj_vols_diff = vols_adj_ents(Computer.Map.GetScalarField, field_name="DIFF")

            ent_adj_vol_interfaces = vols_adj_ents(Selector.Interface, to_ent=internal_ents)
            interface_centers = ent_adj_vol_interfaces(Computer.Map.GetCentroid)

            internal_ents_dx = interface_centers(Computer.Map.NormDist, other=internal_ents_centers)
            adj_vols_dx = interface_centers(Computer.Map.NormDist, other=adj_vols_centers)

            # Computing
            two = internal_ents(Computer.Map.PutScalar, value=2.0)
            diff_eq_numerator = two(Computer.Map.ScalarProd,
                                    other=adj_vols_dx)(Computer.Map.ScalarProd,
                                                       other=internal_ents_dx)
            diff_eq_denominator_1 = internal_ents_dx(Computer.Map.ScalarProd,
                                                     other=internal_ents_diff)
            diff_eq_denominator_2 = adj_vols_dx(Computer.Map.ScalarProd,
                                                other=adj_vols_diff)
            diff_eq_denominator = diff_eq_denominator_1(Computer.Map.ScalarSum, other=diff_eq_denominator_2)

            adj_diff_eq = diff_eq_numerator(Computer.Map.ScalarDiv, other=diff_eq_denominator)

            ent_diff_flow_sum = adj_diff_eq(Computer.Reduce.Sum)

            # Managing
            matrix = internal_ents(Manager.Matrix.Create, field_name="DENS")

            adj_diff_eq(Manager.Matrix.FillColumns, matrix=matrix)
            ent_diff_flow_sum(Manager.Matrix.FillDiag, matrix=matrix)

            matrix(Manager.Matrix.Solve)

            internal_ents.export_tree('res1.png')

        elliptic_.run_kernel(mci)

        elliptic_.export('test.h5m')



