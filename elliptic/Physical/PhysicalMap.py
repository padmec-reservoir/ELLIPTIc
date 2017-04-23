# coding=utf-8
from PhysicalBase import PhysicalBase


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

    def __setitem__(self, physical_id, value):
        """Adds a new physical value associated with a `physical_id`.

        Parameters
        ----------
        physical_id: int
            ID associated with a physical groupd from the mesh.
        value: elliptic.Physical.PhysicalBase.PhysicalBase
            A Physical instance to be associated with the given `physical_id`.

        """
        if isinstance(value, PhysicalBase):
            self.physical_values[id] = value
        else:
            raise ValueError("The physical value must inherit from Physical.")

    def __getitem__(self, physical_id):
        """Gets the Physical instance associated with the given `physical_id`.

        """
        return self.physical_values[physical_id]

    def __contains__(self, physical_id):
        """Checks if the given `physical_id` was defined.

        """
        return physical_id in self.physical_values
