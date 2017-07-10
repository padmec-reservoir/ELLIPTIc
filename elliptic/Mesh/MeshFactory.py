# coding=utf-8
import colorlog
from pymoab import core

from Mesh import Mesh


class MeshFactory(object):
    """Mesh factory for meshes that use MOAB as backend.

    """

    LOG = colorlog.getLogger('elliptic.Mesh.MeshFactory')

    def load_mesh(self, filename):
        """Loads a mesh from a file and initializes it using MOAB.

        Parameters
        ----------
        filename: string
            Path to the file to be open.

        Returns
        -------
         elliptic.Mesh.Mesh.Mesh
            The initialized mesh.
        """
        self.LOG.info("Loading mesh file...")
        mb = core.Core()
        mb.load_file(filename)

        the_mesh = Mesh(mb)

        return the_mesh
