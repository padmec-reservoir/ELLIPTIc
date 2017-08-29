from KernelBase import KernelBase


class DimensionEntityKernelMixin(KernelBase):
    """Kernel that iterates over all entities of a given dimension.

    """
    entity_dim = -1

    def get_elements(self):
        ents = self.mesh.dimension_entities(self.entity_dim)
        return ents


class MeshSetEntityKernelMixin(DimensionEntityKernelMixin):
    """Kernel that iterates over all meshsets from a tag.

    """
    meshset_tag_name = ""

    def get_elements(self):
        ents = self.mesh.get_entities_by_meshset(
            self.meshset_tag_name, self.entity_dim)
        return ents
