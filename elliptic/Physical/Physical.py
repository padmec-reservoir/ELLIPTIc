# coding=utf-8
import numpy as np


class PhysicalBase(object):
    """Defines the interface for physical properties.

    A subclass should override the `value` property getter and setter
    accordingly.
    """
    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, v):
        raise NotImplementedError


class Dirichlet(PhysicalBase):
    """Defines a boundary condition of Dirichlet type.

    """
    def __init__(self, v):
        super(PhysicalBase, self).__init__()

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


class Neumann(PhysicalBase):
    # TODO
    pass


class Robin(PhysicalBase):
    # TODO
    pass


class Wall(PhysicalBase):
    # TODO
    pass


class Symmetric(PhysicalBase):
    """Defines the boundary condition of symmetrical nature.

    """
    def __init__(self):
        super(PhysicalBase, self).__init__()

    @PhysicalBase.value.getter
    def value(self):
        return Symmetric


class InitialCondition(PhysicalBase):
    """Defines the interface for initial conditions.

    """
    pass


class Permeability(InitialCondition):
    """Defines the permeability initial condition.

    """
    def __init__(self, v):
        super(PhysicalBase, self).__init__()

        self._value = None
        self.value = v

    @PhysicalBase.value.getter
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if isinstance(v, np.ndarray) and v.shape == (3, 3):
            self._value = v
        else:
            raise ValueError("Permeability conditions must be second order "
                             "tensors using numpy arrays.")
