from KernelBase import KernelBase
from elliptic.Solver import ReadOnlyMatrix


class FillArrayKernelBase(KernelBase):
    """Base class for array-based kernel mixins.

    Attributes
    ----------
    array_name: string, optional
        Name of the array associated with this kernel. If not set,
        defaults to the kernel's class name.
    share: bool, optional
        If the array associated with this kernel could be used as the
        array_name attribute of other kernel classes. If not set, defaults to
        False. If set to True, other kernel classes could have the ability to
        access and modify the same associated array.

    """

    array_name = ""
    solution_dim = -1
    share = False

    @classmethod
    def check_kernel(cls):
        super(FillArrayKernelBase, cls).check_kernel()
        assert cls.solution_dim >= 0

    @classmethod
    def init_kernel(cls, m):
        super(FillArrayKernelBase, cls).init_kernel(m)
        if not cls.array_name:
            cls.array_name = cls.__name__

    @classmethod
    def create_array(cls, matrix_manager):
        raise NotImplementedError

    @classmethod
    def fill_array(cls, mesh, vals):
        raise NotImplementedError

    @classmethod
    def get_array(cls, mesh):
        return mesh.matrix_manager.get_vector(cls.array_name)

    @classmethod
    def set_dependency_vectors(cls, mesh):
        for dep in cls.depends:
            if issubclass(dep, FillArrayKernelBase):
                ar = dep.get_array(mesh.matrix_manager)
                readonly_ar = ReadOnlyMatrix(ar, mesh.id_map)
                setattr(cls, dep.array_name + '_array', readonly_ar)


class FillVectorKernelMixin(FillArrayKernelBase):
    """Defines a mixin for kernels that will fill a vector array.

    """

    @classmethod
    def create_array(cls, matrix_manager):
        matrix_manager.create_vector(
            cls.solution_dim, cls.array_name, cls.share)

    @classmethod
    def fill_array(cls, mesh, vals):
        id_map = mesh.id_map
        matrix_manager = mesh.matrix_manager

        for elem, value in vals:
            row = id_map[elem]
            matrix_manager.fill_vector(cls.array_name, row, value)

    @classmethod
    def get_array(cls, matrix_manager):
        return matrix_manager.get_vector(cls.array_name)


class FillMatrixKernelMixin(FillArrayKernelBase):
    """Defines a mixin for kernels that will fill a matrix array.

    """

    @classmethod
    def create_array(cls, matrix_manager):
        matrix_manager.create_matrix(
            cls.solution_dim, cls.array_name, cls.share)

    @classmethod
    def fill_array(cls, mesh, vals):
        id_map = mesh.id_map
        matrix_manager = mesh.matrix_manager

        set_values = vals['set']
        sum_values = vals['sum']

        for elem, cols, values in set_values:
            row = id_map[elem]
            cols = [id_map[col] for col in cols]
            matrix_manager.fill_matrix(cls.array_name, row, cols, values)

        for elem, cols, values in sum_values:
            row = id_map[elem]
            cols = [id_map[col] for col in cols]
            matrix_manager.sum_into_matrix(cls.array_name, row, cols, values)

    @classmethod
    def get_array(cls, matrix_manager):
        return matrix_manager.get_matrix(cls.array_name)
