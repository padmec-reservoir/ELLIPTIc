import numpy as np

from EntityKernelMixins import DimensionEntityKernelMixin
from ArrayKernelMixins import FillVectorKernelMixin, FillMatrixKernelMixin
from elliptic.Physical import PhysicalBase, Dirichlet
from elliptic.Problem import RunnerBase


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
    def _run(self):
        self.problem.run_pipeline()
        self.problem.fill_matrices()

        self.problem.setup_linear_problem(A_name='T', b_name='b')
        self.problem.solve()


class EquivPerm(DimensionEntityKernelMixin, FillVectorKernelMixin):
    """Kernel which calculates the equivalent permeability in the faces.

    """
    entity_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1
    solution_dim = 2

    @classmethod
    def run(cls, m, elem):
        adj = cls.get_adj(m, elem, cls.bridge_dim, cls.target_dim, cls.depth)

        if len(adj) > 1:
            edge_center = cls.get_center(m, elem)
            el1_center = cls.get_center(m, adj[0])
            el2_center = cls.get_center(m, adj[1])
            dx1 = np.linalg.norm(el1_center - edge_center)
            dx2 = np.linalg.norm(el2_center - edge_center)
            K1 = cls.get_physical(m, adj[0]).value
            K2 = cls.get_physical(m, adj[1]).value

            K_equiv = (2*K1*K2) / (K1*dx2 + K2*dx1)

            cls.fill_array(m, [(elem, K_equiv)])
        else:
            cls.fill_array(m, [(elem, 0)])


class FillDiag(DimensionEntityKernelMixin, FillMatrixKernelMixin):
    """Fills the matrix diagonals.

    """
    array_name = "T"
    share = True

    entity_dim = 3
    solution_dim = 3

    @classmethod
    def run(cls, m, elem):
        # Default value
        value = 0

        for dim in range(0, cls.entity_dim):
            adj_faces_physical = cls.get_adj_physical(
                m, elem, dim, dim, phys_type=Dirichlet)
            # If the current element has a boundary condition,
            # sets value to 1
            if adj_faces_physical:
                    value = 1
                    break

        results = {
            'set': [(elem, [elem], [value])],
            'sum': []
        }

        cls.fill_array(m, results)


class FillBoundary(DimensionEntityKernelMixin, FillVectorKernelMixin):
    """Fills the vector 'b' with boundary conditions.

    """
    name = "b"
    entity_dim = 3
    bridge_dim = 3
    target_dim = 3
    depth = 1
    solution_dim = 3

    @classmethod
    def run(cls, m, elem):
        value = 0

        for dim in range(0, cls.entity_dim):
            adj_faces_physical = cls.get_adj_physical(
                m, elem, dim, dim, phys_type=Dirichlet)
            # If the current element has a boundary condition,
            # sets value to 1
            if adj_faces_physical:
                    value = adj_faces_physical.value
                    break

        cls.fill_array(m, [(elem, value)])


class TPFAKernel(DimensionEntityKernelMixin, FillMatrixKernelMixin):
    """Example kernel for the TPFA method. This kernel iterates on the mesh
    faces and fills the transmissibility matrix accordingly.

    """
    array_name = "T"
    share = True

    entity_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1
    solution_dim = 3

    depends = [EquivPerm, FillDiag, FillBoundary]

    @classmethod
    def run(cls, m, elem):
        results = {
            'set': [],
            'sum': []
        }

        # Gets the equivalent permeability for the face
        K_equiv = cls.EquivPerm_array[elem]

        adj = cls.get_adj(m, elem, cls.bridge_dim, cls.target_dim, cls.depth)
        adj = list(adj)

        # If the face has two adjacend volumes
        if len(adj) == 2:
            # Check if those volumes do not have any faces with boundary
            # conditions of type Dirichlet
            for dim in range(0, cls.entity_dim):
                adj0_faces_physical = cls.get_adj_physical(
                    m, adj[0], dim, dim, phys_type=Dirichlet)
                # Uses the first Dirichlet condition found
                if adj0_faces_physical:
                        break

            for dim in range(0, cls.entity_dim):
                adj1_faces_physical = cls.get_adj_physical(
                    m, adj[1], dim, dim, phys_type=Dirichlet)
                # Uses the first Dirichlet condition found
                if adj1_faces_physical:
                        break

            if not adj0_faces_physical:
                results['set'].append((adj[0], [adj[1]], [-K_equiv]))
                results['sum'].append((adj[0], [adj[0]], [K_equiv]))

            if not adj1_faces_physical:
                results['set'].append((adj[1], [adj[0]], [-K_equiv]))
                results['sum'].append((adj[1], [adj[1]], [K_equiv]))

        cls.fill_array(m, results)
