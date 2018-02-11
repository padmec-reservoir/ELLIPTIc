from .Selector import Selector


class Filter(Selector):

    def __init__(self):
        super().__init__()


class Where(Filter):

    def __init__(self, **conditions):
        super().__init__()

        self.conditions = conditions

        conditions_str = ""
        for k, v in conditions.items():
            conditions_str = conditions_str + '\n' + k + "=" + str(v)
        self.name = "Where" + conditions_str

    def render(self, template_manager, child, backend_builder) -> str:
        template_file = backend_builder.where()
        template = template_manager.get_template(template_file)

        rendered_template = template.render(conditions=self.conditions.items(),
                                            child=child)

        return rendered_template
