from elliptic.Kernel.MeshComputeInterface.BackendBuilder import BackendBuilderSubClass


class EllipticFunction:

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def process_fun_args(self, backend_builder: BackendBuilderSubClass):
        return getattr(backend_builder, self.name)(**self.kwargs)
