from collections import defaultdict
import numpy
import pytest


from elliptic.Kernel import (KernelBase, EntityKernelMixins, AdjKernelMixin,
                             PropertyKernelMixin, ArrayKernelMixins)


class TestKernelBase(object):

    def get_instance_no_deps_kwargs(self, mocker):
        class TestKernel(KernelBase):
            pass

        return TestKernel(mocker.Mock())

    def get_instance_with_deps_kwargs(self, mocker, deps, deps_kwargs):
        class TestKernel(KernelBase):
            depends = deps

        return TestKernel(mocker.Mock(), deps_kwargs)

    def test_init(self, mocker, faker):
        k = self.get_instance_no_deps_kwargs(mocker)
        assert isinstance(k.deps_kwargs, defaultdict)

        k = self.get_instance_with_deps_kwargs(
            mocker, mocker.Mock(), mocker.sentinel.deps_kwargs)
        assert k.deps_kwargs is mocker.sentinel.deps_kwargs

    def test_build_dependencies(self, mocker, faker):
        depends = [mocker.Mock()]
        deps_kwargs = {depends[0]: faker.pydict()}
        k = self.get_instance_with_deps_kwargs(
            mocker, depends, deps_kwargs)

        depends[0].return_value = mocker.Mock()

        k.build_dependencies()

        depends[0].assert_called_once_with(k.mesh, **deps_kwargs[depends[0]])
        depends[0].return_value.build_dependencies.assert_called_once_with()

        assert len(k.depends_instances) == 1
        assert k.depends_instances[0] is depends[0].return_value

    def test_get_elements_raises_NotImplementedError(self, mocker):
        k = self.get_instance_no_deps_kwargs(mocker)
        with pytest.raises(NotImplementedError):
            k.get_elements()

    def test_run_raises_NotImplementedError(self, mocker):
        k = self.get_instance_no_deps_kwargs(mocker)
        with pytest.raises(NotImplementedError):
            k.run(None)

    def test_get_physical(self, mocker, faker):
        elems = faker.pylist(10, True, int)
        elems_phys_val = faker.pylist(len(elems), False, int)

        k = self.get_instance_no_deps_kwargs(mocker)

        k.mesh.physical.query.return_value = [[elems, None]]
        k.mesh.moab.tag_get_data.return_value = elems_phys_val

        phys = k.get_physical(mocker.sentinel.phys_type, elems)
        check_vals = zip(set(elems), elems_phys_val)
        for elem_val in phys:
            assert elem_val in check_vals

        k.mesh.physical.query.assert_called_once_with(
            mocker.sentinel.phys_type)

        phys = k.get_physical(mocker.sentinel.phys_type, [])
        k.mesh.physical.query.assert_called_with(
            mocker.sentinel.phys_type)
        assert phys == []

    def test_get_average_position(self, mocker, faker):
        elem = faker.pyint()
        k = self.get_instance_no_deps_kwargs(mocker)

        mocker.patch('numpy.array')
        numpy.array.return_value = mocker.sentinel.elem_array
        k.get_average_position(elem)
        k.mesh.mesh_topo_util.get_average_position.assert_called_once_with(
            mocker.sentinel.elem_array)
        numpy.array.assert_called_once_with([elem])


class TestDimensionEntityKernelMixin(object):

    def get_instance(self, mocker, faker):
        class TestKernel(EntityKernelMixins.DimensionEntityKernelMixin):
            entity_dim = faker.pyint() % 4

        return TestKernel(mocker.Mock())

    def test_get_elements(self, mocker, faker):
        k = self.get_instance(mocker, faker)

        k.mesh.get_entities_by_meshset.return_value = mocker.sentinel.elems
        r = k.get_elements()

        k.mesh.get_entities_by_meshset.assert_called_once_with(
            'ROOT', k.entity_dim)
        assert r is mocker.sentinel.elems


class TestMeshSetEntityKernelMixin(object):

    def get_instance(self, mocker, faker):
        class TestKernel(EntityKernelMixins.MeshSetEntityKernelMixin):
            entity_dim = faker.pyint() % 4
            meshset_tag_name = faker.pystr()

        return TestKernel(mocker.Mock())

    def test_get_elements(self, mocker, faker):
        k = self.get_instance(mocker, faker)

        k.mesh.get_entities_by_meshset.return_value = mocker.sentinel.elems
        r = k.get_elements()

        k.mesh.get_entities_by_meshset.assert_called_once_with(
            k.meshset_tag_name, k.entity_dim)
        assert r is mocker.sentinel.elems


class TestAdjKernelMixin(object):

    def get_instance(self, mocker):
        class TestKernel(AdjKernelMixin):
            pass

        return TestKernel(mocker.Mock())

    def test_class_adj_str(self, mocker, faker):
        k = self.get_instance(mocker)

        bridge_dim, target_dim, depth = (
            faker.pyint() % 4, faker.pyint() % 4, faker.pyint() % 4)

        tag_name = "_adj_tag_{0}{1}{2}".format(
            bridge_dim, target_dim, depth)

        assert k.adj_str[(bridge_dim, target_dim, depth)] == tag_name

    def test_get_adj(self, mocker, faker):
        k = self.get_instance(mocker)

        elem = faker.pyint()

        bridge_dim, target_dim, depth = (
            faker.pyint() % 4, faker.pyint() % 4, faker.pyint() % 4)

        k.mesh.moab.tag_get_handle.return_value = mocker.sentinel.adj_tag
        k.mesh.moab.tag_get_data.return_value = mocker.sentinel.adj_set
        k.mesh.moab.get_entities_by_handle.return_value = mocker.sentinel.adj

        adj = k.get_adj(elem, bridge_dim, target_dim, depth)

        k.mesh.moab.tag_get_data.assert_called_once_with(
            mocker.sentinel.adj_tag, elem, flat=True)

        k.mesh.moab.get_entities_by_handle.assert_called_once_with(
            mocker.sentinel.adj_set)

        assert adj is mocker.sentinel.adj


class TestPropertyKernelMixin(object):

    def get_instance_with_property_name(self, mocker, faker):
        class TestKernel(PropertyKernelMixin):
            num_values = faker.pyint()
            property_name = faker.pystr()

        return TestKernel(mocker.Mock())

    def get_instance_empty_property_name(self, mocker, faker):
        class TestKernel(PropertyKernelMixin):
            num_values = faker.pyint()

        return TestKernel(mocker.Mock())

    def test_init(self, mocker, faker):
        k = self.get_instance_with_property_name(mocker, faker)

        k.mesh.create_double_tag.assert_called_once_with(
            k.property_name, k.num_values)

        k = self.get_instance_empty_property_name(mocker, faker)

        assert k.property_name == 'TestKernel'

    def test_set_property_value(self, mocker, faker):
        k = self.get_instance_with_property_name(mocker, faker)

        elem = mocker.sentinel.elem
        value = mocker.sentinel.value

        k.set_property_value([(elem, value)])

        k.mesh.set_tag_value.assert_called_once_with(
            k.property_name, [elem], [value])


class TestFillArrayKernelBase(object):

    def get_instance_with_array_name(self, mocker, faker):
        class TestKernel(ArrayKernelMixins.FillArrayKernelBase):
            array_name = faker.pystr()
            solution_dim = faker.pyint() % 4
            share = faker.pybool()

        return TestKernel(mocker.Mock())

    def get_instance_empty_array_name(self, mocker, faker):
        class TestKernel(ArrayKernelMixins.FillArrayKernelBase):
            solution_dim = faker.pyint() % 4
            share = faker.pybool()

        return TestKernel(mocker.Mock())

    def get_instance_with_depends(self, mocker, faker, depends_ar):
        class TestKernel(ArrayKernelMixins.FillArrayKernelBase):
            array_name = faker.pystr()
            solution_dim = faker.pyint() % 4
            share = faker.pybool()
            depends = depends_ar

        return TestKernel(mocker.Mock())

    def test_init(self, mocker, faker):
        k = self.get_instance_empty_array_name(mocker, faker)

        assert k.array_name == 'TestKernel'

    def test_create_array_raises_NotImplementedError(self, mocker, faker):
        k = self.get_instance_empty_array_name(mocker, faker)

        with pytest.raises(NotImplementedError):
            k.create_array()

    def test_fill_array_raises_NotImplementedError(self, mocker, faker):
        k = self.get_instance_empty_array_name(mocker, faker)

        with pytest.raises(NotImplementedError):
            k.fill_array(mocker.sentinel.DEFAULT)

    def test_get_array_raises_NotImplementedError(self, mocker, faker):
        k = self.get_instance_empty_array_name(mocker, faker)

        with pytest.raises(NotImplementedError):
            k.get_array()

    def test_set_dependency_vectors(self, mocker, faker):
        depends = [mocker.Mock()]
        depends[0].return_value = mocker.Mock(
            spec=ArrayKernelMixins.FillArrayKernelBase)
        dep = depends[0].return_value
        dep.get_array.return_value = mocker.sentinel.ar
        dep.array_name = faker.pystr()

        k = self.get_instance_with_depends(mocker, faker, depends)
        k.mesh.matrix_manager = mocker.sentinel.matrix_manager
        k.mesh.id_map = mocker.sentinel.id_map

        k.build_dependencies()

        ReadOnlyMatrix = mocker.patch(
            'elliptic.Kernel.ArrayKernelMixins.ReadOnlyMatrix')
        ReadOnlyMatrix.return_value = mocker.sentinel.readonly_ar

        k.set_dependency_vectors()

        dep.get_array.assert_called_once_with(mocker.sentinel.matrix_manager)
        ReadOnlyMatrix.assert_called_once_with(
            mocker.sentinel.ar, mocker.sentinel.id_map)
        assert getattr(
            k, dep.array_name + '_array') is mocker.sentinel.readonly_ar


class TestFillVectorKernelMixin(object):

    def get_instance_empty_solution_access(self, mocker, faker):
        class TestKernel(ArrayKernelMixins.FillVectorKernelMixin):
            array_name = faker.pystr()
            solution_dim = faker.pyint() % 4
            share = faker.pybool()

        return TestKernel(mocker.Mock())

    def get_instance_with_solution_access(self, mocker, faker, sol_access_ar):
        class TestKernel(ArrayKernelMixins.FillVectorKernelMixin):
            array_name = faker.pystr()
            solution_dim = faker.pyint() % 4
            share = faker.pybool()

        return TestKernel(mocker.Mock(), sol_access_ar)

    def test_create_array(self, mocker, faker):
        k = self.get_instance_empty_solution_access(mocker, faker)

        k.create_array()

        k.mesh.matrix_manager.create_vector.assert_called_once_with(
            k.solution_dim, k.array_name, k.share)

    def test_fill_array(self, mocker, faker):
        k = self.get_instance_empty_solution_access(mocker, faker)
        vals = [(faker.pyint(), faker.pyint())]

        k.mesh.id_map.__getitem__ = mocker.Mock(
            side_effect={vals[0][0]: faker.pyint()}.__getitem__)

        k.fill_array(vals)

        k.mesh.matrix_manager.fill_vector.assert_called_once_with(
            k.array_name, k.mesh.id_map[vals[0][0]], vals[0][1])

    def test_get_array(self, mocker, faker):
        k = self.get_instance_empty_solution_access(mocker, faker)

        k.get_array()

        k.mesh.matrix_manager.get_vector.assert_called_once_with(k.array_name)

    def test_set_dependency_vectors(self, mocker, faker):
        sol_access = [mocker.Mock(
            spec=ArrayKernelMixins.FillArrayKernelBase)]
        dep = sol_access[0]
        dep.get_array.return_value = mocker.sentinel.ar
        dep.array_name = faker.pystr()

        k = self.get_instance_with_solution_access(mocker, faker, sol_access)
        k.mesh.matrix_manager = mocker.sentinel.matrix_manager
        k.mesh.id_map = mocker.sentinel.id_map

        ReadOnlyMatrix = mocker.patch(
            'elliptic.Kernel.ArrayKernelMixins.ReadOnlyMatrix')
        ReadOnlyMatrix.return_value = mocker.sentinel.readonly_ar

        k.set_dependency_vectors()

        k.solution_access[0].get_array.assert_called_once_with(
            mocker.sentinel.matrix_manager)

        ReadOnlyMatrix.assert_called_once_with(
            mocker.sentinel.ar, mocker.sentinel.id_map)
        assert getattr(
            k, dep.array_name + '_array') is mocker.sentinel.readonly_ar
