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
        """Checks if the kernel has defined the `solution_dim` attribute.

        """
        super(FillArrayKernelBase, cls).check_kernel()
        assert cls.solution_dim >= 0

    @classmethod
    def init_kernel(cls, m):
        """Initializes the `array_name` attribute, defaulting it to the Kernel's
        class name if it was not defined.

        """
        super(FillArrayKernelBase, cls).init_kernel(m)
        if not cls.array_name:
            cls.array_name = cls.__name__

    @classmethod
    def create_array(cls, matrix_manager):
        """Abstract method. Defines how the array associated with the Kernel
        and the Mesh will be created.

        Raises
        ------
        NotImplementedError
            If not overriden by a subclass.
        """
        raise NotImplementedError

    @classmethod
    def fill_array(cls, mesh, vals):
        """Abstract method. Defines how to fill the associated array with
        calculated values during the run method.

        Raises
        ------
        NotImplementedError
            If not overriden by a subclass.
        """
        raise NotImplementedError

    @classmethod
    def get_array(cls, mesh):
        """Defines how the associated array can be obtained.

        """
        return mesh.matrix_manager.get_vector(cls.array_name)

    @classmethod
    def set_dependency_vectors(cls, mesh):
        """Iterates over the `depends` attribute, and adds the associated array
        of each Kernel, if applicable, with an attribute on this Kernel.

        The attribute will have the form `dep.array_name + '_array'` for each
        dependency that has an associated array. That is, for a dependency
        that has the name TestKernel, the associated attribute will be called
        TestKernel_array.

        Example
        -------
        >>> class Test1(DimensionEntityKernelMixin, FillMatrixKernelMixin):
        ...     #...
        >>> class Test2(DimensionEntityKernelMixin, FillMatrixKernelMixin):
        ...     #...
        ...     depends = [Test1]
        ...     @classmethod
        ...     def run(cls, m, elem):
        ...         Test1_val = cls.Test1_array[elem]

        """
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
        """Defines how the associated vector will be created.

        """
        matrix_manager.create_vector(
            cls.solution_dim, cls.array_name, cls.share)

    @classmethod
    def fill_array(cls, mesh, vals):
        """Defines how the associated vector will be filled within the run()
        method.

        Parameters
        ----------
        mesh: elliptic.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        vals: list
            List of (line, value) values.

        """
        id_map = mesh.id_map
        matrix_manager = mesh.matrix_manager

        for elem, value in vals:
            row = id_map[elem]
            matrix_manager.fill_vector(cls.array_name, row, value)

    @classmethod
    def get_array(cls, matrix_manager):
        """Defines how the associated vector can be obtained.

        """
        return matrix_manager.get_vector(cls.array_name)


class FillMatrixKernelMixin(FillArrayKernelBase):
    """Defines a mixin for kernels that will fill a matrix array.

    """

    @classmethod
    def create_array(cls, matrix_manager):
        """Defines how the associated matrix will be created.

        """
        matrix_manager.create_matrix(
            cls.solution_dim, cls.array_name, cls.share)

    @classmethod
    def fill_array(cls, mesh, vals):
        """Defines how the associated matrix will be filled within the run()
        method.

        Parameters
        ----------
        mesh: elliptic.Mesh.Mesh.Mesh
            Mesh object that is running the kernel.
        vals: dictionary
            Dictionary that contains the keys 'set' and 'sum'. Both keys should
            have a list of (line, columns, values) value. The 'set' values will
            be set on the matrix, and the 'sum' values will be summed.
        """
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
        """Defines how the associated matrix can be obtained.

        """
        return matrix_manager.get_matrix(cls.array_name)
