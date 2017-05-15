import colorlog
import time

from pymoab import types
from pymoab import topo_util
import numpy as np

from elliptic.Solver import MatrixManager


class Mesh(object):
    """Defines mesh behavior using MOAB as library.
    A Mesh should only be associated with one problem at a time.

    Note
    ----
    This class is tightly coupled with the entire system. If you
    wish to extend it, you may need to replicate behavior from the MOAB
    library.

    """

    LOG = colorlog.getLogger('elliptic.Mesh.Mesh')

    def __init__(self, mb, physical):
        self.physical_manager = physical
        self.moab = mb
        self.tag2entset = {}
        self.id_map = {}
        self.mesh_topo_util = topo_util.MeshTopoUtil(mb)
        self.meshsets = {'ROOT': mb.get_root_set()}
        self.tags = {}

        self.ran_kernels = set()

        self.matrix_manager = MatrixManager()

        self._save_tags()
        self._save_physical_tags()
        self._generate_dense_elements()
        self._create_matrix_maps()
        self._create_id_maps()

    def _save_tags(self):
        self.physical_tag = self.moab.tag_get_handle("MATERIAL_SET")

    def _save_physical_tags(self):
        physical_sets = self.moab.get_entities_by_type_and_tag(
            0, types.MBENTITYSET,
            np.array((self.physical_tag,)), np.array((None,)))

        self.LOG.debug("Loading physical tags...")
        for tag in physical_sets:
            tag_id = self.moab.tag_get_data(
                self.physical_tag, np.array([tag]), flat=True)

            if tag_id[0] not in self.physical_manager:
                raise ValueError("Tag {0} not defined in the physical "
                                 "properties structure".format(tag_id))

            elems = self.moab.get_entities_by_handle(tag, True)
            self.tag2entset[tag_id[0]] = {e for e in elems}

    def _generate_dense_elements(self):
        """Generates all aentities

        """
        self.LOG.debug("Generating dense elements...")
        all_verts = self.get_entities_by_meshset('ROOT', 0)
        self.mesh_topo_util.construct_aentities(all_verts)

    def _create_matrix_maps(self):
        for dim in range(4):
            all_ents = self.get_entities_by_meshset('ROOT', dim)
            self.matrix_manager.create_map(dim, len(all_ents))

    def _create_id_maps(self):
        for dim in range(4):
            all_ents = self.get_entities_by_meshset('ROOT', dim)
            idx = 0
            for ent in all_ents:
                self.id_map[ent] = idx
                idx += 1

    def get_entities_by_meshset(self, set_name, dim):
        """Gets all the entities form a meshset.

        Parameters
        ----------
        set_name: string
            Name of the set.
        dim: unsigned int
            Dimension of the entities.

        """
        # TODO: Test me
        ents = self.moab.get_entities_by_dimension(
            self.meshsets[set_name], dim)

        return ents

    def create_double_solution_tag(self, tag_name, dim=1):
        """Creates a solution tag of type double with the name `tag_name`.

        Parameters
        ----------
        tag_name: string
            Name of the tag.

        """
        self.tags[tag_name] = self.moab.tag_get_handle(
            tag_name, dim, types.MB_TYPE_DOUBLE, True)

    def set_double_solution_tag(self, tag_name, elem, values):
        """Sets the values `values` on the tag of name `tag_name`, on the
        element `elem`.

        Parameters
        ----------
        tag_name: string
            Name of the tag.
        elem: unsigned int
            The element.
        values: iterable
            Iterable containing the values associated with the element `elem`.

        """
        self.moab.tag_set_data(self.tags[tag_name], elem, values)

    def create_handle_tag(self, tag_name, dim=1):
        """Creates a solution tag of type double with the name `tag_name`.

        Parameters
        ----------
        tag_name: string
            Name of the tag.

        """
        self.tags[tag_name] = self.moab.tag_get_handle(
            tag_name, dim, types.MB_TYPE_HANDLE, True)

    def set_handle_tag(self, tag_name, elem, handles):
        self.moab.tag_set_data(self.tags[tag_name], elem, handles)

    def set_solution(self, tag_name, dimension, vector):
        """Sets the solution of name `tag_name`, on elements of the given
        `dimension`, with the values from the given `vector`.

        Parameters
        ----------
        tag_name: string
            Name of the tag.
        dimension: unsigned int
            Dimension of the target elements which will hold the solution.
        vector: PyTrilinos.Epetra.Vector vector or numpy.ndarray
            Array containing the solution.

        """
        ents = self.get_entities_by_meshset('ROOT', dimension)
        self.moab.tag_set_data(self.tags[tag_name], ents, np.asarray(vector))

    def run_kernel(self, kernel):
        """Excecutes a `kernel` in the mesh. Its dependencies are run
        recursively.

        Parameters
        ----------
        kernel: elliptic.Kernel.Kernel.Kernel
            Kernel to be run.

        """
        # Check if the kernel has already been executed
        if kernel in self.ran_kernels:
            return
        else:
            self.ran_kernels.add(kernel)

        kernel.check_kernel()
        kernel.init_kernel(self)

        elems = kernel.get_elements(self)

        # TODO: Check for circular dependencies
        for dep in kernel.depends:
            self.run_kernel(dep)

        kernel.create_array(self.matrix_manager)
        kernel.set_dependency_vectors(self)

        self.LOG.info("Running kernel {0}".format(kernel.__name__))
        t0 = time.time()
        count = 0
        percent = 0
        for elem in elems:
            count += 1
            if count == (len(elems) // 100):
                percent += 1
                self.LOG.debug('{0}%'.format(percent))
                count = 0

            kernel.run(self, elem)

        self.LOG.info("\ntook {0} seconds... Ran over {1} elems\n".format(
            time.time() - t0, len(elems)))
