# coding=utf-8
import numpy as np


class PhysicalBase(object):
    """Define interface for physical properties"""
    @property
    def value(self):
        """Get the property value"""
        raise NotImplementedError

    @value.setter
    def value(self, v):
        """Defines the property value"""
        raise NotImplementedError


class Dirichlet(PhysicalBase):
    """Defines a boundary condition of Dirichlet type"""
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
    """Defines boundary condition of symmetrical nature"""
    def __init__(self):
        super(PhysicalBase, self).__init__()

    # TODO: No futuro isso deve significar fluxo nulo!
    @PhysicalBase.value.getter
    def value(self):
        return Symmetric


class Permeability(PhysicalBase):
    """Defines permeability initial condition"""
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


class InitialCondition(PhysicalBase):
    """Defines interface for initial conditions"""
    pass
