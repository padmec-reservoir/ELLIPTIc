from KernelBase import KernelBase


class FieldKernelMixin(KernelBase):
    """Defines a mixin for Kernels that will preprocess properties.

    Attributes
    ----------
    dimension: unsigned int
        The number of dimensions that will be associated with the field
        calculated. By default, the value 1 is for scalars, 3 for vectors and
        9 for tensors.
    field_name: string, optional
        The name of the property. If not set, defaults to the kernel's class
        name.

    """

    dimension = -1
    field_name = ""

    def __init__(self, mesh):
        """Initializes the property memory storage.

        """
        super(FieldKernelMixin, self).__init__(mesh)

        if not self.field_name:
            self.field_name = self.__class__.__name__

        self.mesh.create_field(self.field_name, self.dimension)

        self.field_handle = self.mesh.get_field(self.field_name)

        self.dependency_handles = {}

    def set_field_value(self, vals):
        """Sets the associated property.

        Parameters
        ----------
        vals: iterable
            Iterable of (elem, value) values.

        """
        for elem, value in vals:
            self.mesh.set_field_value(self.field_handle, [elem], [value])

    def get_field_value(self, field_name, elems, flat=True):
        field_handle = self.mesh.get_field(field_name)
        return self.mesh.get_field_value(field_handle, elems, flat=flat)

    def set_field_with_field(self, from_field_name, to_field_name):
        from_field_handle = self.mesh.get_field(from_field_name)
        to_field_handle = self.mesh.get_field(to_field_name)

        elems = self.get_elements()

        from_field_vals = self.mesh.get_field_value(
            from_field_handle, elems, flat=False)

        self.mesh.set_field_value(to_field_handle, elems, from_field_vals)
