
class Context:

    def __init__(self):
        self.compute_nodes = []

    def add_compute_node(self, compute_node):
        self.compute_nodes.append(compute_node)


class ComputeInterface:

    def __init__(self, context=None):
        if not context:
            self.context = Context()
        else:
            self.context = context


class MeshComputeInterface(ComputeInterface):

    def by_dim(self, dim):
        self.context.add_compute_node()

    def by_set(self):
        pass
