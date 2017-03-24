# coding=utf-8
import numpy as np


def check_kernel(kernel_class):
    if kernel_class.elem_dim == -1:
        raise ValueError('Value of elem_dim not initialized in {0}'.format(
            kernel_class.__name__))

    if kernel_class.bridge_dim == -1:
        raise ValueError('Value of bridge_dim not initialized in {0}'.format(
            kernel_class.__name__))

    if kernel_class.target_dim == -1:
        raise ValueError('Value of target_dim not initialized in {0}'.format(
            kernel_class.__name__))

    if kernel_class.depth == -1:
        raise ValueError('Value of depth not initialized in {0}'.format(
            kernel_class.__name__))

    if kernel_class.solution_dim == -1:
        raise ValueError('Value of solution_dim not initialized in {0}'.format(
            kernel_class.__name__))


class KernelBase(object):
    """Class which defines the Kernel interface.

    Properties:
        elem_dim -- Dimension of the elements which the kernel operates at
        bridge_dim -- Intermediary dimension to obtain the adjacencies
        target_dim -- Dimension of the adjacent elements
        depth -- Adjacency depth
        solution_dim -- Dimension of the elements that will hold the solution
            calculated in this kernel
        depends -- List of other kernels that are supposed to run before this
    """
    elem_dim = -1
    bridge_dim = -1
    target_dim = -1
    depth = -1
    solution_dim = -1

    depends = []

    @classmethod
    def get_physical(cls, m, elem):
        """Gets the first physical found for a given element."""
        for tag, elemset in m.tag2entset.iteritems():
            if elem in elemset:
                return m.physical_manager[tag]

    @classmethod
    def get_adj(cls, m, elem, bridge_dim,
                target_dim, depth=1):
        """Returns the elements adjacent to the element elem, through
        bridge_dim, with dimension target_dim with the given depth."""
        adj = m.mesh_topo_util.get_bridge_adjacencies(
            np.asarray([elem]),
            bridge_dim,
            target_dim,
            depth)

        return adj

    @classmethod
    def get_adj_physical(cls, m, elem, bridge_dim,
                         target_dim, depth=1, phys_type=None):
        # TODO: phys_type ser um array
        adj = m.mesh_topo_util.get_bridge_adjacencies(
            np.asarray([elem]),
            bridge_dim,
            target_dim,
            depth)
        adj = set(adj)
        physicals = []
        for tag, elemset in m.tag2entset.iteritems():
            if adj.intersection(elemset):
                phys = m.physical_manager[tag]
                if isinstance(phys, phys_type):
                    return phys

                physicals.append(m.physical_manager[tag])

        if not phys_type:
            return physicals

    @classmethod
    def get_center(cls, m, elem):
        """Average vertex coords"""
        return m.mesh_topo_util.get_average_position(
            np.array([elem], dtype='uint64'))

    @classmethod
    def run(cls, m, elem, adj):
        """Runs the kernel over the elements elems. The kernel return value
        depends on its type, and should always be associated with the filling
        of a matrix or vector.

        If the kernel is of type fill_vector, the return value must be a list
        of (line, value) values.

        If the kernel is of type fill_matrix, the return must be a dictionary
        that contains the keys 'set' and 'sum'. Both keys should have a list of
        (line, columns, values) value. The 'set' values will be set on the
        matrix, and the 'sum' values will be summed.
        """
        raise NotImplementedError
