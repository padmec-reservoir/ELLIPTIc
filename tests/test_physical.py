import pytest
import numpy

from elliptic.Physical import PhysicalMap
from elliptic import Physical


class TestPhysical:

    def test_PhysicalBase(self):
        phys = Physical.PhysicalBase()
        with pytest.raises(NotImplementedError):
            phys.value = 1
        with pytest.raises(NotImplementedError):
            phys.value


class TestPhysicalMap:

    def setup(self):
        self.map = PhysicalMap()

    def test_add_physical(self):
        self.map[101] = Physical.PhysicalBase()

        assert 101 in self.map

    def test_add_non_physical_raises_ValueError(self):
        with pytest.raises(ValueError):
            self.map[101] = 5.0
