from .MeshComputeInterface import ContextNode


class EntitySelector:

    def __init__(self, parent):
        self.parent = parent
        self.context_node = ContextNode(parent, self.template_file)

    def get_context_node(self):
        return self.context_node

    def by_dim(self, dim):
        template_file = 'by_ent.pyx'

    def by_set(self):
        pass
