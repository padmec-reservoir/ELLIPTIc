import pytest
import numpy

from Padmec.Mesh.Mesh import Mesh
from Padmec.Mesh.MoabMeshFactory import MoabMeshFactory
from Padmec.Physical.PhysicalMap import PhysicalMap
from Padmec.Physical import Physical


class TestMesh:
    def setup(self):
        self.mesh = Mesh(None)

    def test_mesh_check_physical_constraint_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            self.mesh.check_physical_constraint(None)

    def test_mesh_get_adj_elems_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            self.mesh.get_adj_elems(None, None, None)


class TestMoabMesh:
    def setup(self):
        self.physical = PhysicalMap()
        self.physical[101] = Physical.Dirichlet(1.0)
        self.physical[102] = Physical.Dirichlet(-1.0)
        self.physical[103] = Physical.Symmetric()
        self.physical[50] = Physical.Permeability(numpy.eye(3))

        self.meshfile = 'tests/cube_small_1part.msh'

        self.mf = MoabMeshFactory()

    def test_load_mesh(self):
        self.mf.load_mesh(self.meshfile, self.physical)

    def test_load_mesh_with_wrong_physical_raises_ValueError(self):
        physical_wrong = PhysicalMap()
        with pytest.raises(ValueError):
            self.mf.load_mesh(self.meshfile, physical_wrong)

    def test_check_physical_constraint(self):
        my_mesh = self.mf.load_mesh(self.meshfile, self.physical)

        # TODO: Finish me!
