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

    Attributes
    ----------
    elem_dim: unsigned int
        Dimension of the elements which the kernel operates at.
    bridge_dim: unsigned int
        Intermediary dimension to obtain the adjacencies.
    target_dim: unsigned int
        Dimension of the adjacent elements.
    depth: unsigned int
        Adjacency depth.
    solution_dim: unsigned int
        Dimension of the elements that will hold the solution
        calculated in this kernel.
    depends: list of kernels
        List of other kernels that are supposed to run before this kernel.

    """
    elem_dim = -1
    bridge_dim = -1
    target_dim = -1
    depth = -1
    solution_dim = -1

    depends = []

    @classmethod
    def get_physical(cls, m, elem):
        """Gets the first Physical instance found for a given element.

        Parameters
        ----------
        m: padpy.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        elem:
            Target element to get the physical property.

        Returns
        -------
        padpy.Physical.Physical
            Returns the Physical instance associated with `elem`.

        """
        for tag, elemset in m.tag2entset.iteritems():
            if elem in elemset:
                return m.physical_manager[tag]

    @classmethod
    def get_adj(cls, m, elem, bridge_dim,
                target_dim, depth=1):
        """Returns the elements adjacent to the element `elem`, through
        `bridge_dim`, with dimension `target_dim`, and with the given `depth`.

        Parameters
        ----------
        m: padpy.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        elem:
            Target element to get the adjacencies.
        bridge_dim: unsigned int
            Bridge dimention through which the adjacent elements are obtained.
        target_dim: unsigned int
            Target dimesion. The adjacent elements will have this dimension.
        depth: unsigned int, optional
            Depth of the adjacency query. Defaults to 1.

        Returns
        -------
        list
            List of the adjacent elements.
        """
        adj = m.mesh_topo_util.get_bridge_adjacencies(
            np.asarray([elem]),
            bridge_dim,
            target_dim,
            depth)

        return adj

    @classmethod
    def get_adj_physical(cls, m, elem, bridge_dim,
                         target_dim, depth=1, phys_type=None):
        """Gets the Physical instances of the adjacent elements.

        Parameters
        ----------
        m: padpy.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        elem:
            Target element to get the adjacent physicals.
        bridge_dim: unsigned int
            Bridge dimention through which the adjacent elements are obtained.
        target_dim: unsigned int
            Target dimesion. The adjacent elements will have this dimension.
        depth: unsigned int, optional
            Depth of the adjacency query. Defaults to 1.
        phys_type: padpy.Physical.Physical type, optional
            The target Physical type (class). If not set, defaults to None.
            If set, will returnthe first Physical of the given type that is
            found.

        Returns
        -------
        list of padpy.Physical.Physical or padpy.Physical.Physical
            If `phys_type` is set to none, will return the first Physical
            found. Returns a list containing all Physicals found otherwise.
        """
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
        """Average vertex coords.

        Parameters
        ----------
        m: padpy.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        elem:
            Target element to get the averaged center.

        Returns
        -------
        numpy.ndarray
            Array representing the coordinates of the averaged center.

        """
        return m.mesh_topo_util.get_average_position(
            np.array([elem], dtype='uint64'))

    @classmethod
    def run(cls, m, elem, adj):
        """Runs the kernel over the elements elems. The kernel return value
        depends on its type (defined by a kernel decorator), and should always
        be associated with the filling of a matrix or vector.

        If the kernel is of type fill_vector, the return value must be a list
        of (line, value) values.

        If the kernel is of type fill_matrix, the return must be a dictionary
        that contains the keys 'set' and 'sum'. Both keys should have a list of
        (line, columns, values) value. The 'set' values will be set on the
        matrix, and the 'sum' values will be summed.

        Raises
        ------
        NotImplementedError
            If not overriden by a subclass.
        """
        raise NotImplementedError
