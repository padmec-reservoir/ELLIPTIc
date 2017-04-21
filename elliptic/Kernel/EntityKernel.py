from KernelBase import KernelBase


class DimensionEntityKernel(KernelBase):
    """Kernel that iterates over all entities of a given dimension.

    """
    entity_dim = -1

    @classmethod
    def check_kernel(cls):
        if cls.entity_dim == -1:
            raise ValueError(
                'Value of entity_dim not initialized in {0}'.format(
                    cls.__name__))

        super(DimensionEntityKernel, cls).check_kernel()

    @classmethod
    def get_elements(cls, m):
        ents = m.get_entities_by_meshset('ROOT', cls.entity_dim)
        return ents


class MeshSetEntityKernel(KernelBase):
    """Kernel that iterates over all entities of a meshset.

    """
    meshset_name = ""
