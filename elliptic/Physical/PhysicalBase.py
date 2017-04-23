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


class Symmetric(PhysicalBase):
    """Defines the boundary condition of symmetrical nature.

    """
    def __init__(self):
        super(Symmetric, self).__init__()

    @PhysicalBase.value.getter
    def value(self):
        return Symmetric


class InitialCondition(PhysicalBase):
    """Defines the interface for initial conditions.

    """
    pass


class DiffusionCoefficient(InitialCondition):
    """Defines the diffusion coefficient initial condition.

    """
    def __init__(self, v):
        super(DiffusionCoefficient, self).__init__()

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
            raise ValueError("The diffusion coefficient initial condition "
                             "must be second order tensors "
                             "using numpy arrays.")
