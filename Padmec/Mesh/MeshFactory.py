# coding=utf-8
from pymoab import core

from Mesh import Mesh


class MeshFactory(object):
    """Mesh factory that uses MOAB as backend."""

    def load_mesh(self, filename, physical):
        """Loads a mesh file using MOAB."""
        print "Loading mesh file..."
        mb = core.Core()
        mb.load_file(filename)

        the_mesh = Mesh(mb, physical)
        the_mesh._save_tags()
        the_mesh._save_physical_tags()
        the_mesh._generate_dense_elements()
        the_mesh._create_maps()

        return the_mesh
