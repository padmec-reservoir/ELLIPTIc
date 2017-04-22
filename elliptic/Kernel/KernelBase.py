import numpy as np
from elliptic.Physical import PhysicalBase


class KernelBase(object):
    """Class which defines the Kernel interface.

    Attributes
    ----------
    depends: list of kernels
        List of other kernels that are supposed to run before this kernel.

    """

    depends = []

    @classmethod
    def init_kernel(cls, m):
        """Initializes a kernel with a mesh.

        """
        pass

    @classmethod
    def check_kernel(cls):
        """Checks if the kernel have all attributes set to a sane value.

        """
        pass

    @classmethod
    def get_elements(cls, m):
        """Gets the elements that this Kernel iterates on.

        """
        raise NotImplementedError

    @classmethod
    def get_physical(cls, m, elem):
        """Gets the first Physical instance found for a given element.

        Parameters
        ----------
        m: elliptic.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        elem:
            Target element to get the physical property.

        Returns
        -------
        elliptic.Physical.Physical
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
        m: elliptic.Mesh.Mesh.Mesh
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
                         target_dim, depth=1, phys_type=PhysicalBase):
        """Gets the Physical instances of the adjacent elements.

        Parameters
        ----------
        m: elliptic.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        elem:
            Target element to get the adjacent physicals.
        bridge_dim: unsigned int
            Bridge dimention through which the adjacent elements are obtained.
        target_dim: unsigned int
            Target dimesion. The adjacent elements will have this dimension.
        depth: unsigned int, optional
            Depth of the adjacency query. Defaults to 1.
        phys_type: elliptic.Physical.Physical type, optional
            The target Physical type (class). If not set, defaults to None.
            If set, will returnthe first Physical of the given type that is
            found.

        Returns
        -------
        list of elliptic.Physical.Physical or elliptic.Physical.Physical
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
        m: elliptic.Mesh.Mesh.Mesh
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
    def run(cls, m, elem):
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
