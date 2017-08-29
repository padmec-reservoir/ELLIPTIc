import pytest

from elliptic.Physical import PhysicalMap
from elliptic import Physical


class TestPhysical:

    def test_add_tag(self, mocker, physical_type):
        phys_type = physical_type(1)[0]
        phys = phys_type()

        phys.add_tag(mocker.sentinel.phys_tag)

        assert phys.phys_tags == [mocker.sentinel.phys_tag]

    def test_iter(self, mocker, physical_type):
        phys_type = physical_type(1)[0]
        phys = phys_type()

        phys.add_tag(mocker.sentinel.phys_tag)

        for tag in phys:
            assert tag == mocker.sentinel.phys_tag


class TestPhysicalMap:

    def setup(self):
        self.physical_map = PhysicalMap()

    def test_resolve(self):
        assert self.physical_map.resolved is False

        self.physical_map.resolve()

        assert self.physical_map.resolved is True

    def test_resolve_raises_ValueError_if_resolved(self):
        self.physical_map.resolve()

        with pytest.raises(ValueError):
            self.physical_map.resolve()

    def test_register_and_query(self, physical_type):
        phys_type = physical_type(1)[0]

        self.physical_map.register(phys_type)

        assert isinstance(
            self.physical_map.query(phys_type), phys_type)

    def test_register_raises_ValueError_if_resolved(self):
        self.physical_map.resolve()

        with pytest.raises(ValueError):
            self.physical_map.register(None)

    def test_register_raises_ValueError_if_double_register(self,
                                                           physical_type):
        phys_type = physical_type(1)[0]

        self.physical_map.register(phys_type)

        with pytest.raises(ValueError):
            self.physical_map.register(phys_type)
