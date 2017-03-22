import numpy as np

from Kernel import KernelBase
from kernel_decorators import fill_matrix, fill_vector
from Padmec.Physical import PhysicalBase, Dirichlet


class TPFAPermeability(PhysicalBase):
    """Defines permeability boundary condition"""
    def __init__(self, v):
        super(PhysicalBase, self).__init__()

        self._value = None
        self.value = v

    @PhysicalBase.value.getter
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v


@fill_vector()
class EquivPerm(KernelBase):
    """Kernel que calcula a permeabilidade equivalente nas faces"""
    elem_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1
    solution_dim = 2

    @classmethod
    def run(cls, m, edge, adj):
        if len(adj) > 1:
            edge_center = cls.get_center(m, edge)
            el1_center = cls.get_center(m, adj[0])
            el2_center = cls.get_center(m, adj[1])
            dx1 = np.linalg.norm(el1_center - edge_center)
            dx2 = np.linalg.norm(el2_center - edge_center)
            K1 = cls.get_physical(m, adj[0]).value
            K2 = cls.get_physical(m, adj[1]).value

            K_equiv = (2*K1*K2) / (K1*dx2 + K2*dx1)

            return [(edge, K_equiv)]
        else:
            return [(edge, 0)]


@fill_matrix(name="T", share=True)
class FillDiag(KernelBase):
    """Preenche a diagonal dos volumes"""
    elem_dim = 3
    bridge_dim = 3
    target_dim = 3
    depth = 1
    solution_dim = 3

    @classmethod
    def run(cls, m, elem, adj):

        results = {
            'set': [(elem, [elem], [0])],
            'sum': []
        }

        return results


@fill_matrix(name="B", share=True)
class FillInitialAndBoundary(KernelBase):
    """Preenche a diagonal dos volumes"""
    elem_dim = 3
    bridge_dim = 3
    target_dim = 3
    depth = 1
    solution_dim = 3

    @classmethod
    def run(cls, m, elem, adj):
        results = {
            'set': [(elem, [elem], [0])],
            'sum': []
        }

        return results


@fill_matrix(name="T", share=True)
class TPFAKernel(KernelBase):
    """Kernel de exemplo TPFA"""
    elem_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1
    solution_dim = 3

    depends = [EquivPerm, FillDiag]

    @classmethod
    def run(cls, m, elem, adj):
        results = {
            'set': [],
            'sum': []
        }

        K_equiv = cls.EquivPerm_array[elem]

        adj0_faces_physical = cls.get_adj_physical(
            m, adj[0], 2, 2, phys_type=Dirichlet)

        adj1_faces_physical = cls.get_adj_physical(
            m, adj[0], 2, 2, phys_type=Dirichlet)

        adj = list(adj)
        if len(adj) == 2:
            if not adj0_faces_physical:
                results['set'].append((adj[0], [adj[1]], [-K_equiv]))
                results['sum'].append((adj[0], [adj[0]], [K_equiv]))

            if not adj1_faces_physical:
                results['set'].append((adj[1], [adj[0]], [-K_equiv]))
                results['sum'].append((adj[1], [adj[1]], [K_equiv]))

        return results
