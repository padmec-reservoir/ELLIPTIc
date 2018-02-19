from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate, BackendBuilderSubClass
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

    def get_context_delegate(self, backend_builder: BackendBuilderSubClass) -> ContextDelegate:
        return backend_builder.where_delegate(conditions=self.conditions.items())
