# coding=utf-8


class Mesh(object):
    """Define uma interface para malhas."""
    def __init__(self, physical, comm=None):
        self.comm = comm
        self.physical_manager = physical

    def check_physical_constraint(self, elems):
        """Checa se o set elems possui alguma propriedade física. Caso sim,
        retorna uma tupla (physical_id, physical_value), onde physical_id
        é um ID para a propriedade física, e physical_value é um valor
        correspondente a esta propriedade. Caso contrário, retorna uma tupla
        vazia."""
        # TODO: Retornar tupla vazia é a melhor forma?
        raise NotImplementedError

    def get_adj_elems(self, elem, bridge_dim, target_dim):
        """Retorna os elementos adjacentes ao elemento elem, de dimensão
        target_dim passando por elementos de dimensão bridge_dim"""
        raise NotImplementedError

    def iterate_elems(self, dim):
        """Itera em todos os elementos de dimensão dim"""
        raise NotImplementedError
