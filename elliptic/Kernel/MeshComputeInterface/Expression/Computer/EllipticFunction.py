from elliptic.Kernel.MeshComputeInterface.BackendBuilder import BackendBuilder


class EllipticFunction:

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def process_fun_args(self, backend_builder: BackendBuilder):
        return getattr(backend_builder, self.name)(**self.kwargs)


class EllipticReduce(EllipticFunction):

    def __init__(self, name, initial_value):
        super().__init__(name, initial_value=initial_value)
