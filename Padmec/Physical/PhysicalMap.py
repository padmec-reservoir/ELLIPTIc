# coding=utf-8
from Physical import PhysicalBase


class PhysicalMap(object):
    """Class responsible for managing initial values, boundary conditions,
    physical properties, etc..."""
    def __init__(self):
        self.physical_values = {}

    def __setitem__(self, id, value):
        """Adds a new physical value associated with an ID"""
        if isinstance(value, PhysicalBase):
            self.physical_values[id] = value
        else:
            raise ValueError("The physical value must inherit from Physical.")

    def __getitem__(self, id):
        return self.physical_values[id]

    def __contains__(self, id):
        """Checks if the physical ID was defined"""
        return id in self.physical_values

    def tags(self):
        """Returns all tags and associated physical values"""
        return self.physical_values.iteritems()
