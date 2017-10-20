import colorlog
import time


class MOABMesh(object):

    LOG = colorlog.getLogger('elliptic.Mesh.Mesh')

    def __init__(self, mb):
        self.moab = mb

    def run_kernel(self, kernel):
        self.LOG.info(f"Running kernel { kernel.__class__.__name__ }")
        t0 = time.time()

        kernel.run(self.moab)

        self.LOG.info(f"\ntook { time.time() - t0 } seconds...\n")
