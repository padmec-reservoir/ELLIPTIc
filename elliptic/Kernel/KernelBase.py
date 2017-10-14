from .MeshComputeInterface import MeshComputeInterface


class KernelBase:

    mci_class = MeshComputeInterface
    default_context_class = None

    def __build_module(self):
        mci = self.mci_class(self.default_context_class)

        self.compute(mci)
        module = mci._build_context()

        return module

    def run(self, mb):
        module = self.__build_module()
        module.execute(mb)

    def compute(self, mci):
        raise NotImplementedError
