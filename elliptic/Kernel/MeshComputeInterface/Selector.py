from .MeshComputeInterface import ContextNode


class EntitySelector:

    def __init__(self, parent):
        self.parent = parent
        self.context_node = ContextNode(parent)

        self.__called = False

    def _get_context_node(self):
        return self.context_node

    def by_dim(self, dim):
        template_file = 'by_ent.pyx.etp'
        options = {

        }

        if self.__called:
            # TODO
            raise NotImplementedError
        else:
            self.__called = True

            self.context_node.set_template_file(template_file)
            self.context_node.set_options(**options)

    def by_set(self):
        # TODO
        raise NotImplementedError
