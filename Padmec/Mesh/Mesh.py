# coding=utf-8
from pymoab import types
from pymoab import topo_util
import numpy as np

from Padmec.Solver import MatrixManager
from Padmec.Kernel import check_kernel


class Mesh(object):
    """Defines mesh behavior using MOAB as library"""
    def __init__(self, mb, physical):
        self.physical_manager = physical
        self.moab = mb
        self.tag2entset = {}
        self.id_map = {}
        self.mesh_topo_util = topo_util.MeshTopoUtil(mb)
        self.root_set = mb.get_root_set()

        self.matrix_manager = MatrixManager()

    def _save_tags(self):
        self.physical_tag = self.moab.tag_get_handle("MATERIAL_SET")

    def _save_physical_tags(self):
        physical_sets = self.moab.get_entities_by_type_and_tag(
            0, types.MBENTITYSET,
            np.array((self.physical_tag,)), np.array((None,)))

        print "Loading physical tags..."
        for tag in physical_sets:
            tag_id = self.moab.tag_get_data(self.physical_tag, np.array([tag]))

            if tag_id[0] not in self.physical_manager:
                raise ValueError("Tag {0} not defined in the physical"
                                 "properties structure".format(tag_id))

            elems = self.moab.get_entities_by_handle(tag, True)
            self.tag2entset[tag_id[0]] = {e for e in elems}

    def _generate_dense_elements(self):
        """Generates all aentities"""
        all_verts = self.moab.get_entities_by_dimension(self.root_set, 0)
        self.mesh_topo_util.construct_aentities(all_verts)

    def _create_matrix_maps(self):
        for dim in range(4):
            all_ents = self.moab.get_entities_by_dimension(self.root_set, dim)
            self.matrix_manager.create_map(dim, len(all_ents))

    def _create_id_maps(self):
        for dim in range(4):
            all_ents = self.moab.get_entities_by_dimension(self.root_set, dim)
            idx = 0
            for ent in all_ents:
                self.id_map[ent] = idx
                idx += 1

    def run_kernel(self, kernel):
        """Excetures a kernel in the mesh"""
        check_kernel(kernel)

        elems = self.moab.get_entities_by_dimension(
            self.root_set, kernel.elem_dim)

        # TODO: Check for dependencies already run, and circular dependencies
        for dep in kernel.depends:
            self.run_kernel(dep)

        kernel.create_array(self.matrix_manager)
        kernel.set_dependency_vectors(self)

        for elem in elems:
            adj = self.mesh_topo_util.get_bridge_adjacencies(
                np.asarray([elem]),
                kernel.bridge_dim,
                kernel.target_dim,
                kernel.depth)

            kernel.run(self, elem, adj)
