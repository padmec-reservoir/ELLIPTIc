from elliptic.Physical import PhysicalBase


class Dirichlet(PhysicalBase):
    """Defines a boundary condition of Dirichlet type.

    """
    def __init__(self, v):
        super(Dirichlet, self).__init__()

        self._value = None
        self.value = v

    @PhysicalBase.value.getter
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if isinstance(v, float):
            self._value = v
        else:
            raise ValueError("Boundary conditions of Dirichlet type must use "
                             "float type.")


class Symmetric(PhysicalBase):
    """Defines the boundary condition of symmetrical nature.

    """
    def __init__(self):
        super(Symmetric, self).__init__()

    @PhysicalBase.value.getter
    def value(self):
        return Symmetric


class Diffusivity(PhysicalBase):
    """Defines a scalar permeability.

    """
    def __init__(self, v):
        super(Diffusivity, self).__init__()

        self._value = None
        self.value = v

    @PhysicalBase.value.getter
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
