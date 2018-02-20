from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilder
from ..Expression import ExpressionBase


class Manager(ExpressionBase):

    def __init__(self):
        super().__init__()


class PutField(Manager):

    def __init__(self, field_name):
        super().__init__()

        self.field_name = field_name

        self.name = "PutField " + '\n' + field_name

    def get_context_delegate(self, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.put_field_delegate(field_name=self.field_name)
