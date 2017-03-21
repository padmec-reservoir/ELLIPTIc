import numpy as np

from Kernel import KernelBase
from kernel_decorators import fill_matrix, preprocess
from Padmec.Physical import PhysicalBase


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


@preprocess()
class EquivPerm(KernelBase):
    """Kernel que calcula a permeabilidade equivalente nas faces"""
    elem_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1
    solution_dim = 2

    @classmethod
    def run(cls, edge, adj, m):
        if len(adj) > 1:
            edge_center = cls.get_center(edge, m)
            el1_center = cls.get_center(adj[0], m)
            el2_center = cls.get_center(adj[1], m)
            dx1 = np.linalg.norm(el1_center - edge_center)
            dx2 = np.linalg.norm(el2_center - edge_center)
            K1 = cls.get_physical(adj[0], m).value
            K2 = cls.get_physical(adj[1], m).value

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
    def run(cls, elem, adj, m):
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
    def run(cls, elem, adj, m):
        results = {
            'set': [],
            'sum': []
        }

        for e in adj:
            results['sum'].append((e, [e], [1]))

        return results
