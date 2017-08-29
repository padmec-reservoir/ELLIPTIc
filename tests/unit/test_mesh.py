
class TestMOABMesh(object):

    def test_phys_tag_entities(self, faker, mesh):
        phys_tag_name = faker.pystr()

        mesh.phys_tag_entities(phys_tag_name)

        mesh.moab.tag_get_handle.assert_called_once_with(
            phys_tag_name + "_elems")

    def test_resolve(self, mocker, mesh, physical_map):
        phys_tag_entities = mocker.patch(
            'elliptic.Mesh.MOABMesh.phys_tag_entities')
        phys_tag_entities.return_value = [1, 2, 3]

        mesh.resolve(physical_map)

        assert mesh.physical is physical_map

    def _create_field(self, mocker, mesh, field_name, dim):
        types = mocker.patch('elliptic.Mesh.Mesh.types')
        types.MB_TYPE_DOUBLE = mocker.sentinel.MB_TYPE_DOUBLE
        types.MB_TAG_SPARSE = mocker.sentinel.MB_TAG_SPARSE

        mesh.moab.tag_get_handle.return_value = mocker.sentinel.MB_TAG

        mesh.create_field(field_name, dim)

    def test_create_field(self, mocker, faker, mesh):
        field_name = faker.pystr()
        dim = faker.pyint() % 4

        self._create_field(mocker, mesh, field_name, dim)

        mesh.moab.tag_get_handle.assert_called_once_with(
            field_name, dim, mocker.sentinel.MB_TYPE_DOUBLE, True,
            mocker.sentinel.MB_TAG_SPARSE)

    def test_set_field_value(self, mocker, faker, mesh):
        field_name = faker.pystr()
        dim = faker.pyint() % 4

        self._create_field(mocker, mesh, field_name, dim)

        numpy = mocker.patch('elliptic.Mesh.Mesh.np')
        numpy.asarray.return_value = mocker.sentinel.ARRAY

        field_handle = mesh.get_field(field_name)

        mesh.set_field_value(field_handle, [1, 2, 3], [1, 2, 3])

        mesh.moab.tag_set_data.assert_called_once_with(
            mocker.sentinel.MB_TAG, [1, 2, 3], mocker.sentinel.ARRAY)
