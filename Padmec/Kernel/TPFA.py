from Kernel import KernelBase
from kernel_decorators import fill_matrix, preprocess


@preprocess()
class EquivPerm(KernelBase):
    """Kernel que calcula a permeabilidade equivalente nas faces"""
    elem_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1

    @classmethod
    def run(self, elems):
        pass


@fill_matrix()
class TPFA(KernelBase):
    """Kernel de exemplo TPFA"""
    elem_dim = 2
    bridge_dim = 2
    target_dim = 3
    depth = 1

    depends = [EquivPerm]

    @classmethod
    def run(self, elems):
        pass
