import time


class RunnerBase(object):
    """Class to abstract problem runners. A problem runnner should expose
    a run() method, responsible for setting up a problem and running it.

    Parameters
    ----------
    problem: padpy.Problem.Problem.ProblemBase
        The Problem instance that this runner will use.

    """
    def __init__(self, problem):
        self.problem = problem

    def run(self):
        """Calls the _run method and measures its running time.

        """
        print "Running problem", self.problem.__class__.__name__
        t0 = time.time()
        self._run()
        print "Running the problem took", time.time() - t0, "seconds..."

    def _run(self):
        """Runs the steps required to set-up the problem, and finally solve it.

        """
        raise NotImplementedError
