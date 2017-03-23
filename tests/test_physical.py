import pytest
import numpy

from padpy.Physical import PhysicalMap
from padpy import Physical


class TestPhysical:

    def test_PhysicalBase(self):
        phys = Physical.PhysicalBase()
        with pytest.raises(NotImplementedError):
            phys.value = 1
        with pytest.raises(NotImplementedError):
            phys.value

    def test_Dirichlet(self):
        with pytest.raises(ValueError):
            phys = Physical.Dirichlet(5)

        phys = Physical.Dirichlet(5.0)

        assert phys.value == pytest.approx(5.0)

    def test_Symmetric(self):
        phys = Physical.Symmetric()

        assert phys.value is Physical.Symmetric

        with pytest.raises(NotImplementedError):
            phys.value = 5.0

    def test_Permeability(self):
        with pytest.raises(ValueError):
            phys = Physical.Permeability(5)

        tensor = numpy.eye(3)
        phys = Physical.Permeability(tensor)

        assert phys.value is tensor


class TestPhysicalMap:

    def setup(self):
        self.map = PhysicalMap()

    def test_add_physical(self):
        self.map[101] = Physical.Dirichlet(5.0)

        assert 101 in self.map
        assert self.map[101].value == pytest.approx(5.0)

    def test_add_non_physical_raises_ValueError(self):
        with pytest.raises(ValueError):
            self.map[101] = 5.0
