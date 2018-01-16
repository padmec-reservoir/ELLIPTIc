from .Selector import Selector


class Dilute(Selector):

    def __init__(self):
        super().__init__()


class ByEnt(Dilute):

    def __init__(self, dim):
        super().__init__()

        self.dim = dim
        self.name = f"By Ent({dim})"

    def render(self, template_manager, child, backend_builder) -> str:
        template_file = backend_builder.by_ent()
        template = template_manager.get_template(template_file)

        rendered_template = template.render(dim=self.dim,
                                            child=child)

        return rendered_template
