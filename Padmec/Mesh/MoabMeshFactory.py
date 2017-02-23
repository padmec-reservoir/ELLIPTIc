# coding=utf-8
from pymoab import core

from MoabMesh import MoabMesh
from PyTrilinos import Epetra  # TODO: Remover isso!


class MoabMeshFactory(object):
    """Factory de malhas que utilizam o MOAB como backend."""
    def __init__(self):
        pass

    def load_mesh(self, filename, physical):
        """Carrega um arquivo de malha utilizando o MOAB."""
        print "Carregando arquivo de malha..."
        mb = core.Core()
        mb.load_file(filename)

        the_mesh = MoabMesh(mb, physical, Epetra.PyComm())
        the_mesh._save_tags()
        the_mesh._save_physical_tags()
        the_mesh._save_partition_elements()
        the_mesh._generate_dense_elements(2)

        return the_mesh
