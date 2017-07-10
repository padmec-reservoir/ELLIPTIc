from KernelBase import KernelBase


class AdjKernelMixin(KernelBase):

    adj_str = {}

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
        try:
            tag_name = cls.adj_str[(bridge_dim, target_dim, depth)]
        except KeyError:
            tag_name = "_adj_tag_{0}{1}{2}".format(
                bridge_dim, target_dim, depth)
            cls.adj_str[(bridge_dim, target_dim, depth)] = tag_name

        adj_tag = m.moab.tag_get_handle(tag_name)
        adj_set = m.moab.tag_get_data(adj_tag, elem, flat=True)
        adj = m.moab.get_entities_by_handle(adj_set)
        return adj
