import pytest
import numpy

from Padmec.Mesh import MeshFactory
from Padmec.Physical import PhysicalMap
from Padmec import Physical


class TestMesh:
    def setup(self):
        self.physical = PhysicalMap()
        self.physical[101] = Physical.Dirichlet(1.0)
        self.physical[102] = Physical.Dirichlet(-1.0)
        self.physical[103] = Physical.Symmetric()
        self.physical[50] = Physical.Permeability(numpy.eye(3))

        self.meshfile = 'tests/cube_small.h5m'

        self.mf = MeshFactory()

    def test_load_mesh(self):
        self.mf.load_mesh(self.meshfile, self.physical)

    def test_load_mesh_with_wrong_physical_raises_ValueError(self):
        physical_wrong = PhysicalMap()
        with pytest.raises(ValueError):
            self.mf.load_mesh(self.meshfile, physical_wrong)
