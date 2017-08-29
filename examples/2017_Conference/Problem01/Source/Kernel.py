import numpy as np

from elliptic.Kernel.EntityKernelMixins import DimensionEntityKernelMixin
from elliptic.Kernel.ArrayKernelMixins import FillMatrixKernelMixin
from elliptic.Kernel import AdjKernelMixin, FieldKernelMixin
from .Physical import Dirichlet, Diffusivity

import Config


class BoundaryKernel(DimensionEntityKernelMixin, FieldKernelMixin,
                     AdjKernelMixin):
    # DimensionEntityKernelMixin
    entity_dim = 3

    # FieldKernelMixin
    dimension = 1

    # FieldKernelMixin
    field_name = Config.RHS_name

    def run(self, elem):
        adj_faces = self.get_adj(elem, 2, 2, 1)
        dir_cond = self.get_physical(Dirichlet, adj_faces)

        if dir_cond:
            self.set_field_value([(elem, dir_cond[0][1])])
        else:
            self.set_field_value([(elem, 0.0)])


class FillDiag(DimensionEntityKernelMixin, FillMatrixKernelMixin,
               AdjKernelMixin):
    """Fills the LHS diagonals.

    """
    array_name = Config.LHS_name
    share = True

    entity_dim = 3
    solution_dim = 3

    def is_boundary(self, elem):
        adj_faces = self.get_adj(elem, 2, 2, 1)
        phys = self.get_physical(Dirichlet, adj_faces)
        return bool(phys)

    def run(self, elem):
        # Default value
        value = 0.0

        if self.is_boundary(elem):
            results = {
                'set': [(elem, [elem], [1.0])],
                'sum': []
            }
        else:
            results = {
                'set': [(elem, [elem], [value])],
                'sum': []
            }

        self.fill_array(results)


class CVFDKernel(DimensionEntityKernelMixin, FillMatrixKernelMixin,
                 AdjKernelMixin):
    # DimensionEntityKernelMixin
    entity_dim = 2

    # FillMatrixKernelMixin
    array_name = Config.LHS_name
    share = True
    solution_dim = 3

    # Custom
    bridge_dim = 2
    target_dim = 3
    depth = 1

    depends = [FillDiag]

    def is_boundary(self, elem):
        adj_faces = self.get_adj(elem, 2, 2, 1)
        phys = self.get_physical(Dirichlet, adj_faces)
        return bool(phys)

    def run(self, elem):
        results = {
            'set': [],
            'sum': []
        }

        D_equiv = 0.0
        adj = self.get_adj(elem, 2, 3, 1)

        if len(adj) > 1:
            edge_center = self.get_average_position(elem)
            el1_center = self.get_average_position(adj[0])
            el2_center = self.get_average_position(adj[1])
            dx1 = np.linalg.norm(el1_center - edge_center)
            dx2 = np.linalg.norm(el2_center - edge_center)
            D1 = self.get_physical(Diffusivity, [adj[0]])[0][1]
            D2 = self.get_physical(Diffusivity, [adj[1]])[0][1]

            D_equiv = (2*D1*D2) / (D1*dx2 + D2*dx1)

            if not self.is_boundary(adj[0]):
                results['set'].append((adj[0], [adj[1]], [-D_equiv]))
                results['sum'].append((adj[0], [adj[0]], [D_equiv]))

            if not self.is_boundary(adj[1]):
                results['set'].append((adj[1], [adj[0]], [-D_equiv]))
                results['sum'].append((adj[1], [adj[1]], [D_equiv]))

        self.fill_array(results)
