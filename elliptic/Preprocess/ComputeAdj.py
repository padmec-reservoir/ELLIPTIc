from pymoab import topo_util
from pymoab import types


class Preprocessor(object):
    """ Preprocessor that computes adjacencies and store them as tags.
    """
    def __init__(self, configs):
        self.configs = configs
        self.adj_config = configs['AdjConfig']
        self.adjacencies = self.adj_config['adjacencies']

    def run(self, moab):
        self._compute_adjacencies(moab)

    def _compute_adjacencies(self, moab):
        """Computes adjacencies and stores them as tags.

        Parameters
        ----------
        moab: MOAB mesh object
            Mesh used to compute the adjacencies. The get_bridge_adjacencies
            method from the topo_util module is used to compute the
            adjacencies.
        """
        mesh_topo_util = topo_util.MeshTopoUtil(moab)
        root_set = moab.get_root_set()

        all_verts = moab.get_entities_by_dimension(root_set, 0)
        mesh_topo_util.construct_aentities(all_verts)

        for (from_dim, bridge_dim, to_dim, layers) in self.adjacencies:
            ents = moab.get_entities_by_dimension(root_set, from_dim)

            adj_tag_name = "__adj_tag_{0}{1}{2}{3}".format(
                from_dim, bridge_dim, to_dim, layers)

            adj_tag = moab.tag_get_handle(
                adj_tag_name, 1, types.MB_TYPE_HANDLE,
                types.MB_TAG_SPARSE, True)

            for ent in ents:
                adjs_meshset = moab.create_meshset()
                adjs = mesh_topo_util.get_bridge_adjacencies(
                    ent, bridge_dim, to_dim, layers)

                moab.add_entities(adjs_meshset, adjs)

                moab.tag_set_data(adj_tag, ent, adjs_meshset)

    @property
    def adj_config(self):
        return self._adj_config

    @adj_config.setter
    def adj_config(self, config):
        if not config:
            raise ValueError("Must have an [AdjConfig] section in the config "
                             "file.")

        self._adj_config = config

    @property
    def adjacencies(self):
        return self._adjacencies

    @adjacencies.setter
    def adjacencies(self, adj_list):
        if not adj_list:
            raise ValueError("Must have a adjacencies option "
                             "under the [AdjConfig] section in the config "
                             "file.")

        adj_list = [tuple(int(val) for val in adj.split('_'))
                    for adj in adj_list]

        self._adjacencies = adj_list
