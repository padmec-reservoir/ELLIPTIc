# coding=utf-8
from Physical import PhysicalBase


class PhysicalMap(object):
    """Classe responsável por gerenciar valores iniciais,
    condições de contorno, propriedades físicas, etc"""
    def __init__(self):
        self.physical_values = {}

    def __setitem__(self, id, value):
        """Adiciona um novo valor físico associado a um ID"""
        if isinstance(value, PhysicalBase):
            self.physical_values[id] = value
        else:
            raise ValueError("O valor físico deve herdar da classe Physical!")

    def __getitem__(self, id):
        return self.physical_values[id]

    def __contains__(self, id):
        """Checa se o id físico foi definido"""
        return id in self.physical_values

    def tags(self):
        """Retorna todas as tags e os valores definidos"""
        return self.physical_values.iteritems()
