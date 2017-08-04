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

    def __init__(self, mesh):
        """Initializes the property memory storage.

        """
        super(PropertyKernelMixin, self).__init__(mesh)

        if not self.property_name:
            self.property_name = self.__class__.__name__

        self.mesh.create_double_tag(
            self.property_name, self.num_values)

    def set_property_value(self, vals):
        """Sets the associated property.

        Parameters
        ----------
        vals: iterable
            Iterable of (elem, value) values.

        """
        for elem, value in vals:
            self.mesh.set_tag_value(self.property_name, [elem], [value])
