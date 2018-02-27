import pytest

from elliptic.Kernel.MeshComputeInterface import MCI
from elliptic.Kernel.MeshComputeInterface.Expression import (Selector,
                                                             Computer, Manager)
from elliptic.Kernel.MeshComputeInterface.MCI import MCIBuildError


class TestMCI:

    def test_root(self, mci, mocker):
        mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')
        assert not mci.building
        assert not mci.built

        with mci.root() as root:
            assert mci.building
            assert not mci.built

        assert not mci.building
        assert mci.built

    def test_root_raises_MCIBuildError(self, mci, mocker):
        mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')

        with mci.root() as root:
            with pytest.raises(MCIBuildError):
                with mci.root() as root2:
                    pass

    def test_get_built_module(self, mci, mocker):
        tree_build = mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')
        tree_build.return_value = mocker.sentinel.built_module

        with mci.root() as root:
            pass

        assert mci.get_built_module() is mocker.sentinel.built_module

    def test_get_built_module_raises_MCIBuildError(self, mci, mocker):
        mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')

        with pytest.raises(MCIBuildError):
            mci.get_built_module()

    def test_build(self, mci, elliptic, mocker):
        tree_build = mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')

        with mci.root() as root:
            pass

        tree_build.assert_called_once()


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



