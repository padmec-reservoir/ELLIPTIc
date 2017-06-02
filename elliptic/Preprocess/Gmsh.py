import json

import numpy as np
from pymoab import core
from pymoab import types
from pymoab import topo_util

from PreprocessorMixins import ConfigFilePreprocessorMixin


class Preprocessor(ConfigFilePreprocessorMixin):

    INFO = """
    Reads a gmsh file and converts its physical entities to a format that
    is understandable by ELLIPTIc.
    """

    def __init__(self, configs):
        self.configs = configs

        self.tag_data = {}

    def run(self):
        self._init_mesh()
        self._read_input_data()
        self._read_physical_tags()
        self._write_mesh()

    def _init_mesh(self):
        self.moab = core.Core()
        self.moab.load_file(self.input_file)
        self.physical_tag = self.moab.tag_get_handle("MATERIAL_SET")

    def _read_input_data(self):
        input_data = self.configs['GmshConfig']['InputData']

        if not input_data:
            return

        for tag_name, tag_data in input_data.iteritems():
            data_size = int(tag_data['data-size'])
            tag_handle = self.moab.tag_get_handle(
                tag_name, data_size, types.MB_TYPE_DOUBLE, True,
                types.MB_TAG_SPARSE)

            for phys_id, gmsh_tag_info in tag_data['GmshTags'].iteritems():
                try:
                    data = json.load(open(gmsh_tag_info['data-file']))
                except IOError:
                    print ("Error reading {0} in the {1} section of the "
                           "config file.".format(
                               gmsh_tag_info['data-file'], tag_name))
                    exit()

                self.tag_data[int(phys_id)] = {
                    'tag': tag_handle,
                    'type': 'data',
                    'data': data}

    def _read_physical_tags(self):
        physical_sets = self.moab.get_entities_by_type_and_tag(
            0, types.MBENTITYSET,
            np.array((self.physical_tag,)), np.array((None,)))

        gid_tag = self.moab.tag_get_handle('GLOBAL_ID')

        print "Loading physical tags..."
        for tag_ms in physical_sets:
            tag_id = self.moab.tag_get_data(
                self.physical_tag, np.array([tag_ms]), flat=True)[0]

            elems = self.moab.get_entities_by_handle(tag_ms, True)

            data_tag_handle = self.tag_data[tag_id]['tag']
            data = self.tag_data[tag_id]['data']
            gids = self.moab.tag_get_data(gid_tag, elems, flat=True)

            try:
                for gid, elem in zip(gids, elems):
                    self.moab.tag_set_data(
                        data_tag_handle, elem, data[str(gid)])
            except Exception as e:
                print ("Error while storing input data. Please verify your "
                       "config and data files.")
                print "Error: ", e
                exit()

            self.moab.clear_meshset(tag_ms)

        self.moab.tag_delete(self.physical_tag)

    def _write_mesh(self):
        self.moab.write_file(self.output_file)
