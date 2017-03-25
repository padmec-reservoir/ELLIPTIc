# coding=utf-8
from Physical import PhysicalBase


class PhysicalMap(object):
    """Class responsible for managing initial values, boundary conditions,
    physical properties, etc...

    Example
    -------
    >>> physical = PhysicalMap()
    >>> physical[101] = Physical.Dirichlet(1.0)
    >>> physical[102] = Physical.Dirichlet(-1.0)
    >>> physical[103] = Physical.Symmetric()
    """
    def __init__(self):
        self.physical_values = {}

    def __setitem__(self, id, value):
        """Adds a new physical value associated with an `id`.

        Parameters
        ----------
        id: int
            ID associated with a physical groupd from the mesh.
        value: padpy.Physical.Physical.PhysicalBase
            A Physical instance to be associated with the given `id`."""
        if isinstance(value, PhysicalBase):
            self.physical_values[id] = value
        else:
            raise ValueError("The physical value must inherit from Physical.")

    def __getitem__(self, id):
        """Gets the Physical instance associated with the given `id`.

        """
        return self.physical_values[id]

    def __contains__(self, id):
        """Checks if the physical `id` was defined.

        """
        return id in self.physical_values
