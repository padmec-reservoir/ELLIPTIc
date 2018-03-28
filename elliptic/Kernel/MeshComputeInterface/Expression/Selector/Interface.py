from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilder
from .Selector import Selector


class Interface(Selector):

    def __init__(self, to_ent: Selector) -> None:
        super().__init__()

        self.to_id = to_ent.unique_id

        self.name = f"Interface({self.to_id})"

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.interface_delegate(context=context, to_ent=self.to_id)
