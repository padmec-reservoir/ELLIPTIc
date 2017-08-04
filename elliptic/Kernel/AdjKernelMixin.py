import itertools

from KernelBase import KernelBase


class AdjKernelMixin(KernelBase):

    adj_str = {}
    for (bridge_dim, target_dim, depth) in itertools.product(
                                           *itertools.repeat([0, 1, 2, 3], 3)):
        tag_name = "_adj_tag_{0}{1}{2}".format(
            bridge_dim, target_dim, depth)
        adj_str[(bridge_dim, target_dim, depth)] = tag_name

    def get_adj(self, elem, bridge_dim,
                target_dim, depth=1):
        """Returns the elements adjacent to the element `elem`, through
        `bridge_dim`, with dimension `target_dim`, and with the given `depth`.

        Parameters
        ----------
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
        iterable
            Iterable of the adjacent elements.
        """
        tag_name = self.adj_str[(bridge_dim, target_dim, depth)]

        adj_tag = self.mesh.moab.tag_get_handle(tag_name)
        adj_set = self.mesh.moab.tag_get_data(adj_tag, elem, flat=True)
        adj = self.mesh.moab.get_entities_by_handle(adj_set)
        return adj
