# coding=utf-8
from pymoab import types
from pymoab import topo_util
import numpy as np

from Mesh import Mesh


class MoabMesh(Mesh):
    """Define comportamento de malhas utilizando MOAB como biblioteca"""
    def __init__(self, mb, physical, comm=None):
        super(MoabMesh, self).__init__(physical, comm)
        self.mb = mb
        self.tag2entset = {}
        self.mtu = topo_util.MeshTopoUtil(mb)

    def _save_tags(self):
        self.part_tag = self.mb.tag_get_handle(
            "PARALLEL_PARTITION", 1, types.MB_TYPE_INTEGER)
        self.physical_tag = self.mb.tag_get_handle("MATERIAL_SET")
        self.gid_tag = self.mb.tag_get_handle("GLOBAL_ID")

    def _save_physical_tags(self):
        physical_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET,
            np.array((self.physical_tag,)), np.array((None,)))

        print "Carregando tags físicas..."
        for tag in physical_sets:
            tag_id = self.mb.tag_get_data(self.physical_tag, np.array([tag]))

            print tag_id,

            if tag_id[0] not in self.physical_manager:
                raise ValueError("Tag {0} não definida na estrutura de"
                                 "propriedades físicas".format(tag_id))

            # TODO: Melhorar isso para paralelismo (cada processo só deve
            # armazenar seus próprios elementos)
            elems = self.mb.get_entities_by_handle(tag, True)
            self.tag2entset[tag_id[0]] = {e for e in elems}

    def _save_partition_elements(self):
        part_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array((self.part_tag,)),
            np.array((None,)))

        self.my_part_set = part_sets[self.comm.MyPID()]

        rs = self.mb.get_root_set()
        self.all_volumes = self.mb.get_entities_by_dimension(rs, 3)
        self.my_volumes = self.mb.get_entities_by_dimension(
            self.my_part_set, 3)
        self.my_global_element_ids = self.mb.tag_get_data(
            self.gid_tag, self.my_volumes)

    def _generate_dense_elements(self, to_dimension):
        """Gera todos os elementos deste processo com dimensão to_dimension

        1- Obtenha todos os vértices
        2- Chame get_adjacencies com to_dimension sendo a dimensão objetivo
            e create_if_missing = True
        """
        my_verts = self.mtu.get_bridge_adjacencies(self.my_volumes, 0, 0)
        self.mb.get_adjacencies(my_verts, to_dimension, create_if_missing=True)

    def check_physical_constraint(self, elems):
        for tag_and_value in self.physical_manager.tags():
            if elems.intersection(self.tag2entset[tag_and_value[0]]):
                return tag_and_value

        return ()

    def get_adj_elems(self, elem, bridge_dim, target_dim):
        return self.mtu.get_bridge_adjacencies(np.asarray([elem]), 2, 2, 0)
