# coding=utf-8
from pymoab import core

from Mesh import Mesh


class MeshFactory(object):
    """Mesh factory for meshes that use MOAB as backend.

    """

    def load_mesh(self, filename, physical):
        """Loads a mesh file using MOAB.

        Parameters
        ----------
        filename: string
            Path to the file to be open.
        physical: padpy.Physical.PhysicalMap.PhysicalMap
            PhysicalMap to be associated with the mesh.

        """
        print "Loading mesh file..."
        mb = core.Core()
        mb.load_file(filename)

        the_mesh = Mesh(mb, physical)
        the_mesh._save_tags()
        the_mesh._save_physical_tags()
        the_mesh._generate_dense_elements()
        the_mesh._create_matrix_maps()
        the_mesh._create_id_maps()

        return the_mesh
