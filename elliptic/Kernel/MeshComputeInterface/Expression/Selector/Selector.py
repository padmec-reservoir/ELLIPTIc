from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilderSubClass
from ..Expression import ExpressionBase


class Selector(ExpressionBase):

    def __init__(self):
        super().__init__()

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        raise NotImplementedError
