from elliptic.Kernel.MeshComputeInterface.Expression.Expression import ExpressionBase


class DeclareVariable(ExpressionBase):

    def __init__(self, var_name, var_type="double"):
        super().__init__()

        self.var_name = var_name
        self.var_type = var_type

        self.name = "DeclareVariable\n" + var_type + ' ' + var_name

    def render(self, template_manager, child, backend_builder) -> str:
        template_file = backend_builder.declare_variable()
        template = template_manager.get_template(template_file)

        rendered_template = template.render(var_name=self.var_name,
                                            var_type=self.var_type,
                                            child=child)

        return rendered_template


class CreateField(ExpressionBase):

    def __init__(self, name, size=1):
        super().__init__()

        self.field_name = name
        self.field_size = size

        self.name = "CreateField" + '\n' + name

    def render(self, template_manager, child, backend_builder) -> str:
        template_file = backend_builder.create_field()
        template = template_manager.get_template(template_file)

        rendered_template = template.render(name=self.field_name,
                                            size=self.field_size,
                                            child=child)

        return rendered_template

    def var_name(self):
        return self.field_name + "_TAG"


class DeclareExistingField(ExpressionBase):

    def __init__(self, name):
        super().__init__()

        self.field_name = name

        self.name = "DeclareExistingField" + '\n' + name

    def render(self, template_manager, child, backend_builder) -> str:
        template_file = backend_builder.get_field()
        template = template_manager.get_template(template_file)

        rendered_template = template.render(name=self.field_name,
                                            child=child)

        return rendered_template

    def var_name(self):
        return self.field_name + "_TAG"