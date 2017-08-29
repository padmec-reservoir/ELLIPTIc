import pytest

from elliptic.Mesh import MOABMesh
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Physical import PhysicalBase


@pytest.fixture()
def physical_type(request, faker):
    def create_physical_types(num_types):
        return [type(
            str(faker.pystr()), (PhysicalBase,), {}) for i in range(num_types)]

    return create_physical_types


@pytest.fixture(params=[
    (1, []),
    (1, ['GROUP1']),
    (2, ['GROUP1', 'GROUP2'])])
def physical_map(request, physical_type):
    physical = PhysicalMap()
    physical_types = physical_type(request.param[0])

    for phys_type in physical_types:
        physical.register(phys_type)

    for group, phys_type in zip(request.param[1], physical_types):
        physical[group] = phys_type

    return physical


@pytest.fixture(params=[[], [1], [1, 2, 3]])
def mesh(request, mocker):
    mocker.patch('elliptic.Mesh.Mesh.topo_util')
    mocker.patch('elliptic.Mesh.Mesh.types')

    moab = mocker.Mock()

    moab.get_entities_by_dimension.side_effect = lambda ms, dim: request.param

    mesh = MOABMesh(moab)

    return mesh
