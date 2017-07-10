from KernelBase import KernelBase


class PropertyKernelMixin(KernelBase):
    """Defines a mixin for Kernels that will preprocess properties.

    Attributes
    ----------
    num_values: unsigned int
        The number of values that will be associated with the property
        calculated. By default, the value 1 is for scalars, 3 for vectors and
        9 for tensors.
    property_name: string, optional
        The name of the property. If not set, defaults to the kernel's class
        name.

    """

    num_values = -1
    property_name = ""

    @classmethod
    def check_kernel(cls):
        """Checks if the kernel has defined the `solution_dim` attribute.

        """
        super(PropertyKernelMixin, cls).check_kernel()
        if cls.num_values < 0:
                raise ValueError("Kernel not properly initialized.")

    @classmethod
    def init_kernel(cls, m):
        """Initializes the property memory storage.

        """
        super(PropertyKernelMixin, cls).init_kernel(m)

        if not cls.property_name:
            cls.property_name = cls.__name__

        m.create_double_solution_tag(cls.property_name, cls.num_values)

    @classmethod
    def set_property_value(cls, mesh, vals):
        """Defines how the associated property will be set.

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
