# coding=utf-8
from .PhysicalBase import PhysicalBase


class PhysicalMap(object):
    """Class responsible for managing initial values, boundary conditions,
    physical properties, etc...

    Example
    -------
    >>> physical = PhysicalMap()
    >>> physical.register(Physical.Dirichlet)
    >>> physical.register(Physical.Neumann)
    >>> physical.register(Physical.Diffusivity)

    >>> physical["INLET"] = Physical.Dirichlet
    >>> physical["OUTLET"] = Physical.Dirichlet
    >>> physical["WALL"] = Physical.Neumann
    >>> physical["DIFFUSIVITY"] = Physical.Diffusivity

    """
    def __init__(self):
        self.physical_names = {}
        self.physical_types = {}
        self.resolved = False

    def __setitem__(self, physical_name, physical_type):
        """Adds a new physical type associated with a `physical_name`.

        Parameters
        ----------
        physical_name: str
            Name associated with a physical groupd from the mesh.
        physical_type: elliptic.Physical.PhysicalBase.PhysicalBase subclass
            A Physical type to be associated with the given `physical_name`.

        """
        if self.resolved:
            raise ValueError("Physical map has already been resolved.")

        if issubclass(physical_type, PhysicalBase):
            physical_type_inst = self.physical_types[physical_type]
            self.physical_names[physical_name] = physical_type_inst
        else:
            raise ValueError("The physical value must inherit from Physical.")

    def __getitem__(self, physical_name):
        """Gets the Physical instance associated with the given `physical_name`.

        """
        return self.physical_names[physical_name]

    def __contains__(self, physical_name):
        """Checks if the given `physical_name` was defined.

        """
        return physical_name in self.physical_names

    def __iter__(self):
        for key, value in self.physical_names.items():
            yield key, value

    def register(self, physical_type):
        """Registers an instance of the given `physical_type`.

        """
        if self.resolved:
            raise ValueError("Physical map has already been resolved.")

        if physical_type not in self.physical_types:
            self.physical_types[physical_type] = physical_type()
        else:
            raise ValueError("The given physical_type has already been "
                             "registered.")

    def query(self, physical_type):
        """Queries the instance of the given `physical_type`.

        Parameters
        ----------
        physical_type: elliptic.Physical.PhysicalBase.PhysicalBase subclass
            A Physical type to be associated with the given `physical_name`.

        Returns
        -------
        elliptic.Physical.PhysicalBase.PhysicalBase
        """
        return self.physical_types[physical_type]

    def resolve(self):
        if self.resolved:
            raise ValueError("Physical map has already been resolved.")

        self.resolved = True
