import numpy as np

from Kernel import KernelBase
from kernel_decorators import fill_matrix, fill_vector
from padpy.Physical import PhysicalBase, Dirichlet
from padpy.Problem import RunnerBase


class TPFAPermeability(PhysicalBase):
    """Defines a scalar permeability.

    """
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


class TPFARunner(RunnerBase):
    """Runner class for the TPFA method.

    """
    def run(self):
        self.problem.run_pipeline()
        self.problem.fill_matrices()

        self.problem.setup_linear_problem(A_name='T', b_name='b')
        self.problem.solve()


@fill_vector()
class EquivPerm(KernelBase):
    """Kernel which calculates the equivalent permeability in the faces.

    """
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
    """Fills the matrix diagonals.

    """
    elem_dim = 3
    bridge_dim = 3
    target_dim = 3
    depth = 1
    solution_dim = 3

    @classmethod
    def run(cls, m, elem, adj):
        # Default value
        value = 0

        adj_faces_physical = cls.get_adj_physical(
            m, elem, 2, 2, phys_type=Dirichlet)
        # If the current element has a boundary condition, sets value to 1
        if adj_faces_physical:
            value = 1

        results = {
            'set': [(elem, [elem], [value])],
            'sum': []
        }

        return results


@fill_vector(name="b")
class FillBoundary(KernelBase):
    """Fills the vector 'b' with boundary conditions.

    """
    elem_dim = 3
    bridge_dim = 3
    target_dim = 3
    depth = 1
    solution_dim = 3

    @classmethod
    def run(cls, m, elem, adj):
        value = 0

        adj_faces_physical = cls.get_adj_physical(
            m, elem, 2, 2, phys_type=Dirichlet)
        if adj_faces_physical:
            value = adj_faces_physical.value

        return [(elem, value)]


@fill_matrix(name="T", share=True)
class TPFAKernel(KernelBase):
    """Example kernel for the TPFA method. This kernel iterates on the mesh
    faces and fills the transmissibility matrix accordingly.

    """
    elem_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1
    solution_dim = 3

    depends = [EquivPerm, FillDiag, FillBoundary]

    @classmethod
    def run(cls, m, elem, adj):
        results = {
            'set': [],
            'sum': []
        }

        # Gets the equivalent permeability for the face
        K_equiv = cls.EquivPerm_array[elem]

        adj = list(adj)
        # If the face has two adjacend volumes
        if len(adj) == 2:
            # Check if those volumes do not have any faces with boundary
            # conditions of type Dirichlet
            adj0_faces_physical = cls.get_adj_physical(
                m, adj[0], 2, 2, phys_type=Dirichlet)

            adj1_faces_physical = cls.get_adj_physical(
                m, adj[1], 2, 2, phys_type=Dirichlet)

            if not adj0_faces_physical:
                results['set'].append((adj[0], [adj[1]], [-K_equiv]))
                results['sum'].append((adj[0], [adj[0]], [K_equiv]))

            if not adj1_faces_physical:
                results['set'].append((adj[1], [adj[0]], [-K_equiv]))
                results['sum'].append((adj[1], [adj[1]], [K_equiv]))

        return results
