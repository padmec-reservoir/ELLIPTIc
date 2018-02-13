from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilderSubClass
from .Selector import Selector


class Interface(Selector):

    def __init__(self, to_ent: Selector):
        super().__init__()

        self.to_id = to_ent.unique_id

        self.name = f"Interface({self.to_id})"

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        return backend_builder.interface_delegate(to_ent=self.to_id)
