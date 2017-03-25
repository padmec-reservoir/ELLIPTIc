
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
        """Runs the steps required to set-up the problem, and finally solve it.

        """
        raise NotImplementedError
