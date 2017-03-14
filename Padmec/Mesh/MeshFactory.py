# coding=utf-8
from pymoab import core

from Mesh import Mesh


class MeshFactory(object):
    """Factory de malhas que utilizam o MOAB como backend."""

    def load_mesh(self, filename, physical):
        """Carrega um arquivo de malha utilizando o MOAB."""
        print "Carregando arquivo de malha..."
        mb = core.Core()
        mb.load_file(filename)

        the_mesh = Mesh(mb, physical)
        the_mesh._save_tags()
        the_mesh._save_physical_tags()
        the_mesh._generate_dense_elements()

        return the_mesh
