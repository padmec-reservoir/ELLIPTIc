from KernelBase import KernelBase


class DimensionEntityKernelMixin(KernelBase):
    """Kernel that iterates over all entities of a given dimension.

    """
    entity_dim = -1

    @classmethod
    def check_kernel(cls):
        if cls.entity_dim == -1:
            raise ValueError(
                'Value of entity_dim not initialized in {0}'.format(
                    cls.__name__))

        super(DimensionEntityKernelMixin, cls).check_kernel()

    @classmethod
    def get_elements(cls, m):
        ents = m.get_entities_by_meshset('ROOT', cls.entity_dim)
        return ents


class MeshSetEntityKernelMixin(KernelBase):
    """Kernel that iterates over all meshsets from a tag.

    """
    meshset_tag_name = ""

    @classmethod
    def check_kernel(cls):
        if not cls.meshset_tag_name:
            raise ValueError(
                'Value of meshset_tag_name not initialized in {0}'.format(
                    cls.__name__))

        super(MeshSetEntityKernelMixin, cls).check_kernel()

    @classmethod
    def get_elements(cls, m):
        ents = m.get_entities_by_meshset('ROOT', cls.entity_dim)
        return ents
