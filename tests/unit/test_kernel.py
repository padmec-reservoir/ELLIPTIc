from collections import defaultdict
import pytest


from elliptic.Kernel import (KernelBase, EntityKernelMixins, AdjKernelMixin,
                             FieldKernelMixin, ArrayKernelMixins)


class TestKernelBase(object):

    @pytest.fixture()
    def instance(self, mesh):
        def get_instance(deps=None, deps_kwargs=None):
            class TestKernel(KernelBase):
                depends = deps

            return TestKernel(mesh, deps_kwargs)

        return get_instance

    def test_init(self, mocker, instance):
        k = instance()
        assert isinstance(k.deps_kwargs, defaultdict)

        k = instance([], mocker.sentinel.deps_kwargs)
        assert k.deps_kwargs is mocker.sentinel.deps_kwargs

    def test_build_dependencies(self, mocker, faker, instance):
        depends = [mocker.Mock()]
        deps_kwargs = {depends[0]: faker.pydict()}
        k = instance(depends, deps_kwargs)

        depends[0].return_value = mocker.Mock()

        k.build_dependencies()

        depends[0].assert_called_once_with(k.mesh, **deps_kwargs[depends[0]])
        depends[0].return_value.build_dependencies.assert_called_once_with()

        assert len(k.depends_instances) == 1
        assert k.depends_instances[0] is depends[0].return_value

    def test_get_elements_raises_NotImplementedError(self, instance):
        k = instance()
        with pytest.raises(NotImplementedError):
            k.get_elements()

    def test_run_raises_NotImplementedError(self, instance):
        k = instance()
        with pytest.raises(NotImplementedError):
            k.run(None)

    def test_get_physical(self, mocker, faker, instance, physical_map,
                          physical_type):
        elems = faker.pylist(10, True, int)
        elems_phys_val = faker.pylist(len(elems), False, int)
        group = faker.pystr()
        physical = physical_type(1)[0]

        k = instance()

        phys_tag_entities = mocker.patch(
            'elliptic.Mesh.MOABMesh.phys_tag_entities')
        phys_tag_entities.return_value = elems
        physical_map.register(physical)
        physical_map[group] = physical

        elem_values = dict(zip(elems, elems_phys_val))
        tag_get_data = mocker.patch(
            'elliptic.Mesh.MOABMesh.get_field_value')
        tag_get_data.side_effect = (
            lambda _, elems, flat: [elem_values[elem] for elem in elems])

        k.mesh.resolve(physical_map)

        phys = k.get_physical(physical, elems)
        for elem_val in phys:
            assert elem_val[1] == elem_values[elem_val[0]]

        phys = k.get_physical(physical, [])
        assert phys == []


class TestDimensionEntityKernelMixin(object):

    @pytest.fixture(params=[0, 1, 2, 3])
    def instance(self, request, faker, mesh):
        class TestKernel(EntityKernelMixins.DimensionEntityKernelMixin):
            entity_dim = request.param

        return TestKernel(mesh)

    def test_get_elements(self, mocker, instance):
        k = instance

        get_entities_by_dimension = mocker.patch(
            'elliptic.Mesh.MOABMesh.dimension_entities')
        get_entities_by_dimension.return_value = mocker.sentinel.elems

        r = k.get_elements()

        get_entities_by_dimension.assert_called_once_with(k.entity_dim)
        assert r is mocker.sentinel.elems


class TestAdjKernelMixin(object):

    @pytest.fixture(params=[0, 1, 2, 3])
    def instance(self, request, faker, mesh):
        class TestKernel(AdjKernelMixin):
            pass

        return TestKernel(mesh)

    def test_class_adj_str(self, mocker, faker, instance):
        k = instance

        bridge_dim, target_dim, depth = (
            faker.pyint() % 4, faker.pyint() % 4, faker.pyint() % 4)

        tag_name = "_adj_tag_{0}{1}{2}".format(
            bridge_dim, target_dim, depth)

        assert k.adj_str[(bridge_dim, target_dim, depth)] == tag_name

    def test_get_adj(self, mocker, faker, instance):
        k = instance

        elem = faker.pyint()

        bridge_dim, target_dim, depth = (
            faker.pyint() % 4, faker.pyint() % 4, faker.pyint() % 4)

        get_adj = mocker.patch(
            'elliptic.Mesh.MOABMesh.get_adj')

        k.get_adj(elem, bridge_dim, target_dim, depth)

        get_adj.assert_called_once_with(
            elem, k.adj_str[(bridge_dim, target_dim, depth)])


class TestPropertyKernelMixin(object):

    @pytest.fixture(params=["Name", ""])
    def instance(self, request, faker, mesh):
        class TestKernel(FieldKernelMixin):
            dimension = faker.pyint() % 4
            field_name = request.param

        return TestKernel(mesh)

    def test_set_property_value(self, mocker, faker, instance):
        k = instance

        elem = mocker.sentinel.elem
        value = mocker.sentinel.value

        set_field_value = mocker.patch(
            'elliptic.Mesh.MOABMesh.set_field_value')
        k.set_field_value([(elem, value)])

        set_field_value.assert_called_once_with(
            k.mesh.get_field(k.field_name), [elem], [value])
