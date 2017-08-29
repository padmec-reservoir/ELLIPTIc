
class PhysicalBase(object):
    """Defines the interface for physical properties.
    """
    def __init__(self):
        self.phys_tags = []

    def add_tag(self, phys_tag):
        self.phys_tags.append(phys_tag)

    def __iter__(self):
        return self.phys_tags.__iter__()
