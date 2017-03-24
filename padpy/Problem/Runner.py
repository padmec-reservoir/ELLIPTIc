
class RunnerBase(object):
    """Class to abstract problem runners. A problem runnner should expose
    a run() method, responsible for setting up a problem and running it."""
    def __init__(self, problem):
        self.problem = problem

    def run(self):
        raise NotImplementedError
