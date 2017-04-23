from elliptic.Problem import RunnerBase


class CCFVMRunner(RunnerBase):
    """Runner class for the CC-FVM method.

    """
    def _run(self):
        self.problem.run_pipeline()
        self.problem.fill_matrices()

        self.problem.setup_linear_problem(A_name='A', b_name='b')
        self.problem.solve()
