# coding=utf-8
from pymoab import types
from pymoab import topo_util
import numpy as np

from Padmec.Kernel import check_kernel


class Mesh(object):
    """Define comportamento de malhas utilizando MOAB como biblioteca"""
    def __init__(self, mb, physical):
        self.physical_manager = physical
        self.mb = mb
        self.tag2entset = {}
        self.mtu = topo_util.MeshTopoUtil(mb)
        self.rs = self.mb.get_root_set()

    def _save_tags(self):
        self.physical_tag = self.mb.tag_get_handle("MATERIAL_SET")

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

            elems = self.mb.get_entities_by_handle(tag, True)
            self.tag2entset[tag_id[0]] = {e for e in elems}

    def _generate_dense_elements(self):
        """Gera todos os aentities"""
        all_verts = self.mb.get_entities_by_dimension(self.rs, 0)
        self.mtu.construct_aentities(all_verts)

    def run_kernel(self, kernel):
        """Executa um kernel na malha"""
        check_kernel(kernel)
        elems = self.mb.get_entities_by_dimension(self.rs, kernel.elem_dim)
        for elem in elems:
            adj = self.mtu.get_bridge_adjacencies(
                np.asarray([elem]),
                kernel.bridge_dim,
                kernel.target_dim,
                kernel.depth)

            kernel.run(adj)
