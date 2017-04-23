import pytest

from elliptic.Mesh import MeshFactory
from elliptic.Physical import PhysicalMap, PhysicalBase


class TestMesh:
    def setup(self):
        self.physical = PhysicalMap()
        self.physical[101] = PhysicalBase()
        self.physical[102] = PhysicalBase()
        self.physical[103] = PhysicalBase()
        self.physical[50] = PhysicalBase()

        self.meshfile = 'tests/cube_small.h5m'

        self.mf = MeshFactory()

    def test_load_mesh(self):
        self.mf.load_mesh(self.meshfile, self.physical)

    def test_load_mesh_with_wrong_physical_raises_ValueError(self):
        physical_wrong = PhysicalMap()
        with pytest.raises(ValueError):
            self.mf.load_mesh(self.meshfile, physical_wrong)
