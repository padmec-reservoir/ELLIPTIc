import numpy as np

from elliptic.Kernel.EntityKernelMixins import DimensionEntityKernelMixin
from elliptic.Kernel import AdjKernelMixin, FieldKernelMixin
from .Physical import Saturation


class VelocityField(DimensionEntityKernelMixin, FieldKernelMixin):
    entity_dim = 3
    dimension = 3

    field_name = "v"

    def run(self, elem):

        self.set_field_value([(elem, [1.0, 0.0, 0.0])])


class InitialSatField(DimensionEntityKernelMixin, FieldKernelMixin,
                      AdjKernelMixin):
    entity_dim = 3
    dimension = 1

    field_name = "Sw_old"

    def run(self, elem):
        adj_faces = self.get_adj(elem, 2, 2, 1)
        sat_cond = self.get_physical(Saturation, adj_faces)

        if sat_cond:
            self.set_field_value([(elem, sat_cond[0][1])])
        else:
            self.set_field_value([(elem, 0.0)])


class WaterFractionalFluxField(DimensionEntityKernelMixin, FieldKernelMixin):
    entity_dim = 3
    dimension = 1

    field_name = "fw"

    def run(self, elem):
        Ksw = self.get_field_value("Sw_old", elem)**2
        Kso = (1.0 - Ksw)**2

        lbd_w = Ksw / 1.0
        lbd_o = Kso / 1.0

        lbd = lbd_o + lbd_w

        fw = lbd_w / lbd

        self.set_field_value([(elem, fw)])


class SatField(DimensionEntityKernelMixin, FieldKernelMixin,
               AdjKernelMixin):
    entity_dim = 3
    dimension = 1

    field_name = "Sw"

    def run(self, elem):
        adj_faces = self.get_adj(elem, 2, 2, 1)
        sat_cond = self.get_physical(Saturation, adj_faces)
        if sat_cond:
            self.set_field_value([(elem, sat_cond[0][1])])
        else:
            adj_vols = self.get_adj(elem, 2, 3, 1)
            adj_faces = set(self.get_adj(elem, 2, 2, 1))

            acc = 0.0

            elem_fw = self.get_field_value("fw", elem)
            elem_v = self.get_field_value("v", elem)
            point_inside_elem = self.get_average_position(elem)

            for adj_vol in adj_vols:
                adj_vol_faces = set(self.get_adj(adj_vol, 2, 2, 1))
                adj_face = adj_faces & adj_vol_faces
                adj_face_nodes = self.get_adj(adj_face, 0, 0, 1)

                normal = self.face_normal(adj_face_nodes, point_inside_elem)

                adj_fw = self.get_field_value("fw", adj_vol)

                Fi = np.dot(elem_v, normal)

                if Fi > 0:
                    acc = acc + adj_fw * Fi
                else:
                    acc = acc + elem_fw * Fi

            Sw_old = self.get_field_value("Sw_old", elem)

            Sw_new = Sw_old + 0.3 * acc

            self.set_field_value([(elem, Sw_new)])
