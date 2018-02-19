from elliptic.Kernel.MeshComputeInterface.BackendBuilder import BackendBuilderSubClass, ContextDelegate
from .EllipticFunction import EllipticReduce
from .Computer import Computer


class Reduce(Computer):

    def __init__(self, reducing_function: EllipticReduce):
        super().__init__()

        self.reducing_function = reducing_function

        self.name = "Reduce " + reducing_function.name

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        processed_fkwargs = self.reducing_function.process_fun_args(backend_builder)
        return backend_builder.reduce_delegate(reducing_function=self.reducing_function,
                                               fargs=processed_fkwargs.items())
