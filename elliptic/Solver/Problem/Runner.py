import time

import colorlog


class RunnerBase(object):
    """Class to abstract problem runners. A problem runnner should expose
    a run() method, responsible for setting up a problem and running it.

    Parameters
    ----------
    problem: elliptic.Problem.Problem.ProblemBase
        The Problem instance that this runner will use.

    """

    LOG = colorlog.getLogger('elliptic.Mesh.Mesh')

    def __init__(self, problem):
        self.problem = problem

    def run(self):
        """Calls the _run method and measures its running time.

        """
        self.LOG.info("Running problem {0}".format(
            self.problem.__class__.__name__))
        t0 = time.time()
        self._run()
        self.LOG.info("Running the problem took {0} seconds...".format(
            time.time() - t0))

    def _run(self):
        """Runs the steps required to set-up the problem, and finally solve it.

        """
        raise NotImplementedError
