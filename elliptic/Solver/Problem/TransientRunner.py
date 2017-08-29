import time

from Runner import RunnerBase


class TransientRunner(RunnerBase):
    def __init__(self, problem):
        super(TransientRunner, self).__init__(problem)

    def run(self, steps, export_frequency, export_name):
        """Calls the _run method and measures its running time.

        """
        self.LOG.info("Running problem {0}".format(
            self.problem.__class__.__name__))
        step = 1
        export_step = 0

        while step <= steps:
            t0 = time.time()
            self._run(step)
            self.LOG.info("Running step {0} took {1} seconds...".format(
                step, time.time() - t0))

            if step % export_frequency == 0:
                print export_name.format(export_step)
                self.problem.export_solution(export_name.format(export_step))
                export_step = export_step + 1

            step = step + 1

    def transient_step(self):
        for kernel in self.problem.pipeline:
            self.problem.mesh.matrix_manager.swap_vector(
                kernel.array_name, kernel.array_name_old)


class TransientExplicitRunner(TransientRunner):
    def _run(self, step):
        self.problem.run_pipeline()
        self.transient_step()
        self.problem.clear_mesh_ran_kernel()
