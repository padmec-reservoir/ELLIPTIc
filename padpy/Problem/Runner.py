
class RunnerBase(object):

    def __init__(self, problem):
        self.problem = problem

    def run(self):
        raise NotImplementedError
