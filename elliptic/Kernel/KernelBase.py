import numpy as np


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
    def get_physical(cls, m, phys_type, elems):
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
        phys_type_inst = m.physical.query(phys_type)
        elems = set(elems)

        for phys_elems, phys_tag in phys_type_inst:
            adj_phys_elems = elems.intersection(phys_elems)

            if adj_phys_elems:
                adj_phys_val = m.moab.tag_get_data(
                    phys_tag,
                    adj_phys_elems,
                    flat=True)

                return zip(adj_phys_elems, adj_phys_val)

        return []

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
