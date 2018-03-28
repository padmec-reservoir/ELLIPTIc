from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilder
from .EllipticFunction import EllipticFunction
from .Computer import Computer


class Map(Computer):

    def __init__(self, mapping_function: EllipticFunction) -> None:
        super().__init__()

        self.mapping_function = mapping_function

        fkwargs_str = ""
        for k, v in mapping_function.kwargs.items():
            fkwargs_str = fkwargs_str + '\n' + k + "=" + str(v)
        self.name = "Map " + mapping_function.name + fkwargs_str

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        processed_fkwargs = self.mapping_function.process_fun_args(backend_builder)
        return backend_builder.map_delegate(context=context,
                                            mapping_function=self.mapping_function,
                                            fargs=processed_fkwargs.items())
