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

    if kernel_class.solution_dim == -1:
        raise ValueError('Value of solution_dim not initialized in {0}'.format(
            kernel_class.__name__))


class KernelBase(object):
    """Class which defines the Kernel interface.

    Properties:
        elem_dim -- Dimension of the elements which the kernel operates at
        bridge_dim -- Intermediary dimension to obtain the adjacencies
        target_dim -- Dimension of the adjacent elements
        depth -- Adjacency depth
        solution_dim -- Dimension of the elements that will hold the solution
            calculated in this kernel
        depends -- List of other kernels that are supposed to run before this
    """
    elem_dim = -1
    bridge_dim = -1
    target_dim = -1
    depth = -1
    solution_dim = -1

    depends = []

    @classmethod
    def run(cls, elems):
        """Executa o kernel nos elementos elems. O retorno do kernel depende
        do seu tipo, e deve sempre estar associado ao preenchimento de uma
        matriz ou vetor.

        Caso o kernel seja do tipo fill_matrix, o retorno deve ser uma lista de
        (linha, colunas, valores).

        Caso o kernel seja do tipo preprocess, o retorno deve ser uma lista de
        (linha, valor)."""
        raise NotImplementedError
