from ..Expression import ExpressionBase


class Manager(ExpressionBase):

    def __init__(self):
        super().__init__()


class PutField(Manager):

    def __init__(self, field_name):
        super().__init__()

        self.field_name = field_name

        self.name = "PutField " + '\n' + field_name

    def render(self, template_manager, child, backend_builder) -> str:
        template_file = backend_builder.put_field()
        template = template_manager.get_template(template_file)

        rendered_template = template.render(field_name=self.field_name,
                                            child=child)

        return rendered_template
