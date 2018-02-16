from elliptic.Kernel.MeshComputeInterface.Expression.Computer import EllipticFunction


class GetScalarField(EllipticFunction):

    def __init__(self, field_name):
        super().__init__(name="get_scalar_field", field_name=field_name)


class PutScalar(EllipticFunction):

    def __init__(self, value):
        super().__init__(name="put_scalar", value=value)


class GetCentroid(EllipticFunction):

    def __init__(self):
        super().__init__(name="get_centroid")


class NormDist(EllipticFunction):

    def __init__(self, other):
        super().__init__(name="norm_dist", other=other)


class ScalarProd(EllipticFunction):

    def __init__(self, other):
        super().__init__(name="scalar_prod", other=other)


class ScalarSum(EllipticFunction):

    def __init__(self, other):
        super().__init__(name="scalar_sum", other=other)


class ScalarDiv(EllipticFunction):

    def __init__(self, other):
        super().__init__(name="scalar_div", other=other)
