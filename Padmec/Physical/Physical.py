# coding=utf-8
import numpy as np


class Physical(object):
    """Define interface para propriedades físicas"""
    @property
    def value(self):
        """Obtém o valor da propriedade"""
        raise NotImplementedError

    @value.setter
    def value(self, v):
        """Define o valor da propriedade"""
        raise NotImplementedError


class Dirichlet(Physical):
    """Define uma condição de contorno do tipo Dirichlet"""
    def __init__(self, v):
        super(Physical, self).__init__()

        self._value = None
        self.value = v

    @Physical.value.getter
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if isinstance(v, float):
            self._value = v
        else:
            raise ValueError("Condições de contorno do tipo Dirichlet devem "
                             "utilizar valores do tipo float.")


class Neumann(Physical):
    # TODO
    pass


class Robin(Physical):
    # TODO
    pass


class Wall(Physical):
    # TODO
    pass


class Symmetric(Physical):
    """Define uma condição de contorno do tipo simétrico"""
    def __init__(self):
        super(Physical, self).__init__()

    # TODO: No futuro isso deve significar fluxo nulo!
    @Physical.value.getter
    def value(self):
        return Symmetric


class Permeability(Physical):
    """Define uma condição de permeabilidade (tensor de segunda ordem)"""
    def __init__(self, v):
        super(Physical, self).__init__()

        self._value = None
        self.value = v

    @Physical.value.getter
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if isinstance(v, np.ndarray) and v.shape == (3, 3):
            self._value = v
        else:
            raise ValueError("Condições de permeabilidade devem ser tensores "
                             "de segunda ordem utilizando arrays do numpy.")


class InitialCondition(Physical):
    """Define interface para condições iniciais"""
    pass
