import numpy as np

from KernelBase import KernelBase
from elliptic.Physical import PhysicalBase


class AdjKernelMixin(KernelBase):

    cache_adj = False
    adj = {}

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
        if cls.cache_adj:
            try:
                return cls.adj[(elem, bridge_dim, target_dim, depth)]
            except KeyError:
                cls.adj[
                    (elem,
                     bridge_dim,
                     target_dim,
                     depth)] = m.mesh_topo_util.get_bridge_adjacencies(
                    np.asarray([elem]),
                    bridge_dim,
                    target_dim,
                    depth)

                return cls.adj[(elem, bridge_dim, target_dim, depth)]
        else:
            adj = m.mesh_topo_util.get_bridge_adjacencies(
                np.asarray([elem]),
                bridge_dim,
                target_dim,
                depth)

        return adj

    @classmethod
    def get_adj_physical(cls, m, elem, bridge_dim,
                         target_dim, depth=1, phys_type=[PhysicalBase]):
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
        phys_type: Iterable of elliptic.Physical.Physical, optional
            The target Physical types (class). If not set, defaults to
            [None].
            If set, will return the first Physical of the given types that is
            found.

        Returns
        -------
        list of elliptic.Physical.Physical or elliptic.Physical.Physical
            If `phys_type` is set to none, will return the first Physical
            found. Returns a list containing all Physicals found otherwise.
        """
        adj = cls.get_adj(m, elem, bridge_dim, target_dim, depth)
        adj = set(adj)
        physicals = []
        for tag, elemset in m.tag2entset.iteritems():
            if adj.intersection(elemset):
                phys = m.physical_manager[tag]
                for phys_check in phys_type:
                    if isinstance(phys, phys_check):
                        return phys

                physicals.append(m.physical_manager[tag])

        if not phys_type:
            return physicals
