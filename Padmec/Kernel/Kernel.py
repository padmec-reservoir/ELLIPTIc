# coding=utf-8


def check_kernel(kernel_class):
    if kernel_class.elem_dim == -1:
        raise ValueError('Value of elem_dim not initialized in {0}'.format(
            kernel_class.__name__))

    if kernel_class.bridge_dim == -1:
        raise ValueError('Value of bridge_dim not initialized in {0}'.format(
            kernel_class.__name__))

    if kernel_class.target_dim == -1:
        raise ValueError('Value of target_dim not initialized in {0}'.format(
            kernel_class.__name__))

    if kernel_class.depth == -1:
        raise ValueError('Value of depth not initialized in {0}'.format(
            kernel_class.__name__))


class KernelBase(object):
    """Classe que define a interface do Kernel.

    Propriedades:
        elem_dim -- É a dimensão dos elementos que o kernel opera sobre
        bridge_dim -- Dimensão intermediária utilizada na obtenção dos
            stencils
        target_dim -- Dimensão dos elementos do stencil
        depth -- Profundidade do stencil
    """
    elem_dim = -1
    bridge_dim = -1
    target_dim = -1
    depth = -1

    @classmethod
    def run_kernel(cls, elems):
        """Executa o kernel nos elementos elems. O retorno do kernel depende
        do seu tipo, e deve sempre estar associado ao preenchimento de uma
        matriz ou vetor.

        Caso o kernel seja do tipo fill_matrix, o retorno deve ser uma lista de
        (linha, colunas, valores).

        Caso o kernel seja do tipo preprocess, o retorno deve ser uma lista de
        (linha, valor)."""
        raise NotImplementedError
