from .MeshComputeInterface import ComputeBase


class Entity(ComputeBase):

    def where(self, **kwargs):
        template_file = 'where.pyx.etp'
        options = {
            "conditions": []
        }
        for condition, value in kwargs.items():
            options['conditions'].append((condition, value))

        context_node = self.context_node_class()

        self.set_template(context_node, template_file, options)
        self.current_node_group.add_node(context_node)

        child_node_group = self.node_group_class()
        context_node.set_child_node_group(child_node_group)

        next_compute = Entity(child_node_group)
        return next_compute


class EntitySelector(ComputeBase):

    def by_dim(self, dim):
        template_file = 'by_ent.pyx.etp'
        options = {
            "dim": dim
        }

        context_node = self.context_node_class()

        self.set_template(context_node, template_file, options)
        self.current_node_group.add_node(context_node)

        child_node_group = self.node_group_class()
        context_node.set_child_node_group(child_node_group)

        next_compute = Entity(child_node_group)
        return next_compute

    def by_set(self):
        # TODO
        raise NotImplementedError
