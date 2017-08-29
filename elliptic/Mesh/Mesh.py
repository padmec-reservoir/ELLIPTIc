import colorlog
import time

from pymoab import types
from pymoab import topo_util
import numpy as np

from elliptic.Solver import MatrixManager


class MOABMesh(object):

    LOG = colorlog.getLogger('elliptic.Mesh.Mesh')

    def __init__(self, mb):
        self.moab = mb
        self.mesh_topo_util = topo_util.MeshTopoUtil(mb)

        self.id_map = {}

        self.fields = {}

        self.matrix_manager = MatrixManager()

        self._create_matrix_maps()
        self._create_id_maps()

    def _create_matrix_maps(self):
        for dim in range(4):
            all_ents = self.dimension_entities(dim)
            self.matrix_manager.create_map(dim, len(all_ents))

    def _create_id_maps(self):
        for dim in range(4):
            all_ents = self.dimension_entities(dim)
            idx = 0
            for ent in all_ents:
                self.id_map[ent] = idx
                idx += 1

    def resolve(self, physical):
        physical.resolve()

        for physical_name, physical_type in physical:
            phys_tag = self.moab.tag_get_handle(physical_name)
            phys_elems = self.phys_tag_entities(physical_name)
            physical_type.add_tag((set(phys_elems), phys_tag))

        self.physical = physical

    def phys_tag_entities(self, phys_tag_name):
        root_set = self.moab.get_root_set()
        phys_tag_elems = self.moab.tag_get_handle(phys_tag_name + "_elems")

        try:
            phys_elems_set = self.moab.tag_get_data(phys_tag_elems, root_set)
        except RuntimeError as e:
            if e.args[0] == types.MB_TAG_NOT_FOUND:
                print "Tag not found: {0}".format(phys_tag_name + "_elems")
            else:
                print "Unknown error."
            exit()
        phys_elems = self.moab.get_entities_by_handle(phys_elems_set)

        return phys_elems

    def dimension_entities(self, dim):
        if dim < 0 or dim > 3:
            raise ValueError("Dimension must be between 0 and 3.")

        ents = self.moab.get_entities_by_dimension(
            self.moab.get_root_set(), dim)
        return ents

    def create_field(self, field_name, dim=1):
        """Creates a field of double type with the name `field_name`.

        Parameters
        ----------
        field_name: string
            Name of the field.
        dim: int
            Dimension (number of values per entity) of the field.
        """
        field_handle = self.moab.tag_get_handle(
            field_name, dim, types.MB_TYPE_DOUBLE, True, types.MB_TAG_SPARSE)
        self.fields[field_name] = field_handle

        return field_handle

    def register_field(self, field_name, dim=1):
        """Registers a field that already exists with the name `field_name`.

        Parameters
        ----------
        field_name: string
            Name of the field.
        """
        self.fields[field_name] = self.moab.tag_get_handle(field_name)

    def get_field(self, field_name):
        return self.fields[field_name]

    def set_field_value(self, field_handle, elems, values):
        self.moab.tag_set_data(field_handle, elems, np.asarray(values))

    def get_field_value(self, field_handle, elems, flat=True):
        return self.moab.tag_get_data(field_handle, elems, flat=flat)

    def get_adj(self, elem, adj_tag_name):
        adj_tag = self.moab.tag_get_handle(adj_tag_name)
        adj_set = self.moab.tag_get_data(adj_tag, elem, flat=True)
        adj = self.moab.get_entities_by_handle(adj_set)
        return adj

    def run_kernel_recur(self, kernel):
        """Excecutes a `kernel` in the mesh. Its dependencies are run
        recursively.

        Parameters
        ----------
        kernel: elliptic.Kernel.Kernel.Kernel
            Kernel to be run.

        """
        #kernel.create_array()

        elems = kernel.get_elements()

        kernel.build_dependencies()
        if kernel.depends_instances:
            for dep in kernel.depends_instances:
                self.run_kernel_recur(dep)

        #if issubclass(kernel, TransientExplicitKernelMixin):
        #    if kernel.solution_init:
        #        for kernel_init in kernel.solution_init:
        #            self.run_kernel_recur(kernel_init)

        kernel.set_dependencies()

        self.LOG.info("Running kernel {0}".format(kernel.__class__.__name__))
        t0 = time.time()
        count = 0
        percent = 0
        for elem in elems:
            count += 1
            if count == (len(elems) // 100):
                percent += 1
                self.LOG.debug('{0}%'.format(percent))
                count = 0

            kernel.run(elem)

        self.LOG.info("\ntook {0} seconds... Ran over {1} elems\n".format(
            time.time() - t0, len(elems)))


#class __MOABMesh(object):
#    """Defines mesh behavior using MOAB as library.
#    A Mesh should only be associated with one problem at a time.
#
#    Note
#    ----
#    This class is tightly coupled with the entire system. If you
#    wish to extend it, you may need to replicate behavior from the MOAB
#    library.
#
#    """
#
#    LOG = colorlog.getLogger('elliptic.Mesh.Mesh')
#
#    def __init__(self, mb):
#        #self.moab = mb
#        #self.id_map = {}
#        #self.mesh_topo_util = topo_util.MeshTopoUtil(mb)
#        #self.tags = {}
#
#        self.ran_kernels = set()
#
#        self.matrix_manager = MatrixManager()
#
#        self._create_matrix_maps()
#        self._create_id_maps()
#
#    def _create_matrix_maps(self):
#        for dim in range(4):
#            all_ents = self.get_entities_by_meshset('ROOT', dim)
#            self.matrix_manager.create_map(dim, len(all_ents))
#
#    def _create_id_maps(self):
#        for dim in range(4):
#            all_ents = self.get_entities_by_meshset('ROOT', dim)
#            idx = 0
#            for ent in all_ents:
#                self.id_map[ent] = idx
#                idx += 1
#
#    def resolve(self, physical):
#        physical.resolve()
#
#        root_set = self.moab.get_root_set()
#        for physical_name, physical_type in physical:
#            phys_tag = self.moab.tag_get_handle(physical_name)
#            phys_tag_elems = self.moab.tag_get_handle(physical_name + "_elems")
#            print physical_name, physical_type
#            phys_elems_set = self.moab.tag_get_data(phys_tag_elems, root_set)
#            phys_elems = self.moab.get_entities_by_handle(phys_elems_set)
#            physical_type.add_tag((set(phys_elems), phys_tag))
#
#        self.physical = physical
#
#    def elemset_entities(self, set_name, dim):
#        """Gets all the entities from an elemset.
#
#        Parameters
#        ----------
#        set_name: string
#            Name of the set.
#        dim: unsigned int
#            Dimension of the entities.
#
#        """
#        # TODO: Test me
#        ents = self.moab.get_entities_by_dimension(
#            self.meshsets[set_name], dim)
#
#        return ents
#
#    def create_double_tag(self, tag_name, dim=1):
#        """Creates a solution tag of type double with the name `tag_name`.
#
#        Parameters
#        ----------
#        tag_name: string
#            Name of the tag.
#
#        """
#        self.tags[tag_name] = self.moab.tag_get_handle(
#            tag_name, dim, types.MB_TYPE_DOUBLE, True, types.MB_TAG_SPARSE)
#
#    def set_tag_value(self, tag_name, elems, values):
#        """Sets the solution of name `tag_name`, on elements of the given
#        `dimension`, with the values from the given `values`.
#
#        Parameters
#        ----------
#        tag_name: string
#            Name of the tag.
#        elems: iterable
#            Iterable of entities.
#        values: iterable
#            Iterable containing the values associated with the entities.
#
#        """
#        self.moab.tag_set_data(self.tags[tag_name], elems, np.asarray(values))
#
#    def init_kernel(self, kernel):
#        kernel.check_kernel()
#        kernel.init_kernel(self)
#        kernel.create_array(self.matrix_manager)
#
#    def remove_ran_kernel(self, kernel):
#        self.ran_kernels.remove(kernel)
#
#    def run_kernel_recur(self, kernel):
#        """Excecutes a `kernel` in the mesh. Its dependencies are run
#        recursively.
#
#        Parameters
#        ----------
#        kernel: elliptic.Kernel.Kernel.Kernel
#            Kernel to be run.
#
#        """
#        # Check if the kernel has already been executed
#        if kernel in self.ran_kernels:
#            return
#        else:
#            self.ran_kernels.add(kernel)
#
#        self.init_kernel(kernel)
#
#        elems = kernel.get_elements(self)
#
#        # TODO: Check for circular dependencies
#        if kernel.depends:
#            for dep in kernel.depends:
#                self.run_kernel_recur(dep)
#
#        if issubclass(kernel, TransientExplicitKernelMixin):
#            if kernel.solution_init:
#                for kernel_init in kernel.solution_init:
#                    self.run_kernel_recur(kernel_init)
#
#        kernel.set_dependency_vectors(self)
#
#        self.LOG.info("Running kernel {0}".format(kernel.__name__))
#        t0 = time.time()
#        count = 0
#        percent = 0
#        for elem in elems:
#            count += 1
#            if count == (len(elems) // 100):
#                percent += 1
#                self.LOG.debug('{0}%'.format(percent))
#                count = 0
#
#            kernel.run(self, elem)
#
#        self.LOG.info("\ntook {0} seconds... Ran over {1} elems\n".format(
#            time.time() - t0, len(elems)))
#
