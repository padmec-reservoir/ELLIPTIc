from elliptic.Kernel.MeshComputeInterface.BackendBuilder import BackendBuilder, ContextDelegate
from .Selector import Selector


class Dilute(Selector):

    def __init__(self):
        super().__init__()


class ByEnt(Dilute):

    def __init__(self, dim):
        super().__init__()

        self.dim = dim
        self.name = f"By Ent({dim})"

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.by_ent_delegate(context=context, dim=self.dim)


class ByAdj(Dilute):

    def __init__(self, bridge_dim, to_dim):
        super().__init__()

        self.bridge_dim = bridge_dim
        self.to_dim = to_dim
        self.name = f"By Adj(bridge_dim={bridge_dim}, to_dim={to_dim})"

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.by_adj_delegate(context=context,
                                               bridge_dim=self.bridge_dim,
                                               to_dim=self.to_dim)
