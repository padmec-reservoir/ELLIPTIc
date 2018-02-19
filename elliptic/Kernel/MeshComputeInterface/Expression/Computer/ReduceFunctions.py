from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticReduce


class Sum(EllipticReduce):

    def __init__(self, initial_value):
        super().__init__(name="reduce_sum", initial_value=initial_value)
