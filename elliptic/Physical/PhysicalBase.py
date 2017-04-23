

class PhysicalBase(object):
    """Defines the interface for physical properties.

    A subclass should override the `value` property getter and setter
    accordingly.
    """
    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, v):
        raise NotImplementedError
