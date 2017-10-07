from .KernelBase import KernelBase
from elliptic.Solver import ReadOnlyMatrix


class FillArrayKernelBase(KernelBase):
    """Base class for array-based kernel mixins.

    Attributes
    ----------
    array_name: string, optional
        Name of the array associated with this kernel. If not set,
        defaults to the kernel's class name.
    solution_dim: unsigned int
        The dimension of the solution that will be calculated in this Kernel.
    share: bool, optional
        If the array associated with this kernel could be used as the
        array_name attribute of other kernel classes. If not set, defaults to
        False. If set to True, other kernel classes could have the ability to
        access and modify the same associated array.

    """

    array_name = ""
    solution_dim = -1
    share = False

    def __init__(self, mesh):
        """Initializes the `array_name` attribute, defaulting it to the Kernel's
        class name if it was not defined.

        """
        super(FillArrayKernelBase, self).__init__(mesh)

        if not self.array_name:
            self.array_name = self.__class__.__name__

        self.create_array()

    def create_array(self):
        """Abstract method. Defines how the array associated with the Kernel
        and the Mesh will be created.

        Raises
        ------
        NotImplementedError
            If not overriden by a subclass.
        """
        raise NotImplementedError

    def fill_array(self, vals):
        """Abstract method. Defines how to fill the associated array with
        calculated values during the run method.

        Raises
        ------
        NotImplementedError
            If not overriden by a subclass.
        """
        raise NotImplementedError

    def get_array(self):
        """Defines how the associated array can be obtained.

        """
        raise NotImplementedError

    def set_dependency_vectors(self):
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
        ...     def run(cls, m, elem):
        ...         Test1_val = cls.Test1_array[elem]

        """
        if self.depends_instances:
            for dep in self.depends_instances:
                if isinstance(dep, FillArrayKernelBase):
                    ar = dep.get_array(self.mesh.matrix_manager)
                    readonly_ar = ReadOnlyMatrix(ar, self.mesh.id_map)
                    setattr(self, dep.array_name + '_array', readonly_ar)


class FillVectorKernelMixin(FillArrayKernelBase):
    """Defines a mixin for kernels that will fill a vector array.

    """

    def __init__(self, mesh, solution_access=None):
        super(FillVectorKernelMixin, self).__init__(mesh)
        self.solution_access = solution_access

    def create_array(self):
        """Defines how the associated vector will be created.

        """
        self.mesh.matrix_manager.create_vector(
            self.solution_dim, self.array_name, self.share)

    def fill_array(self, vals):
        """Defines how the associated vector will be filled within the run()
        method.

        Parameters
        ----------
        vals: list
            List of (line, value) values.

        """
        id_map = self.mesh.id_map
        matrix_manager = self.mesh.matrix_manager

        for elem, value in vals:
            row = id_map[elem]
            matrix_manager.fill_vector(self.array_name, row, value)

    def get_array(self):
        """Defines how the associated vector can be obtained.

        """
        return self.mesh.matrix_manager.get_vector(self.array_name)

    def set_dependency_vectors(self):
        super(FillVectorKernelMixin, self).set_dependency_vectors()
        if self.solution_access:
            for dep in self.solution_access:
                ar = dep.get_array(self.mesh.matrix_manager)
                readonly_ar = ReadOnlyMatrix(ar, self.mesh.id_map)
                setattr(self, dep.array_name + '_array', readonly_ar)


class TransientExplicitKernelMixin(FillVectorKernelMixin):

    @classmethod
    def init_kernel(cls, m):
        super(TransientExplicitKernelMixin, cls).init_kernel(m)
        setattr(cls, 'array_name_old', cls.array_name + '_old')

    @classmethod
    def create_array(cls, matrix_manager):
        super(TransientExplicitKernelMixin, cls).create_array(matrix_manager)
        matrix_manager.create_vector(
            cls.solution_dim, cls.array_name_old, True)

    @classmethod
    def set_dependency_vectors(cls, mesh):
        super(TransientExplicitKernelMixin, cls).set_dependency_vectors(mesh)
        ar = mesh.matrix_manager.get_vector(cls.array_name_old)
        readonly_ar = ReadOnlyMatrix(ar, mesh.id_map)
        setattr(cls, cls.array_name + '_old_array', readonly_ar)


class FillMatrixKernelMixin(FillArrayKernelBase):
    """Defines a mixin for kernels that will fill a matrix array.

    """

    def __init__(self, mesh, solution_access=None):
        super(FillMatrixKernelMixin, self).__init__(mesh)
        self.solution_access = solution_access

    def create_array(self):
        """Defines how the associated matrix will be created.

        """
        self.mesh.matrix_manager.create_matrix(
            self.solution_dim, self.array_name, self.share)

    def fill_array(self, vals):
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
        id_map = self.mesh.id_map
        matrix_manager = self.mesh.matrix_manager

        set_values = vals['set']
        sum_values = vals['sum']

        for elem, cols, values in set_values:
            row = id_map[elem]
            cols = [id_map[col] for col in cols]
            matrix_manager.fill_matrix(self.array_name, row, cols, values)

        for elem, cols, values in sum_values:
            row = id_map[elem]
            cols = [id_map[col] for col in cols]
            matrix_manager.sum_into_matrix(self.array_name, row, cols, values)

    def get_array(self):
        """Defines how the associated matrix can be obtained.

        """
        return self.mesh.matrix_manager.get_matrix(self.array_name)

    def set_dependency_vectors(self):
        super(FillMatrixKernelMixin, self).set_dependency_vectors()
        if self.solution_access:
            for dep in self.solution_access:
                ar = dep.get_array(self.mesh.matrix_manager)
                readonly_ar = ReadOnlyMatrix(ar, self.mesh.id_map)
                setattr(self, dep.array_name + '_array', readonly_ar)
