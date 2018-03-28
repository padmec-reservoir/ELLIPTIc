from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilder
from .Selector import Selector


class Filter(Selector):

    def __init__(self):
        super().__init__()


class Where(Filter):

    def __init__(self, **conditions):
        super().__init__()

        self.conditions = conditions

        conditions_str = ""
        for k, v in conditions.items():
            conditions_str = conditions_str + '\n' + k + "=" + str(v)
        self.name = "Where" + conditions_str

    def get_context_delegate(self, context, backend_builder: BackendBuilder) -> ContextDelegate:
        return backend_builder.where_delegate(context=context, conditions=self.conditions.items())
