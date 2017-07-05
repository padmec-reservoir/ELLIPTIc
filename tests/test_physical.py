import pytest

from elliptic.Physical import PhysicalMap
from elliptic import Physical


class TestPhysical:

    def test_PhysicalBase(self):
        phys = Physical.PhysicalBase()
        with pytest.raises(NotImplementedError):
            phys.value = 1
        with pytest.raises(NotImplementedError):
            phys.value  # pylint: disable=W0104


class TestPhysicalMap:

    def setup(self):
        self.map = PhysicalMap()

    def test_add_physical(self):
        pb = Physical.PhysicalBase()
        self.map[101] = pb

        assert 101 in self.map
        assert self.map[101] is pb

    def test_add_non_physical_raises_ValueError(self):
        with pytest.raises(ValueError):
            self.map[101] = 5.0
