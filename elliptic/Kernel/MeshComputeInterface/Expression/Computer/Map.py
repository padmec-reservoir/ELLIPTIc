from .Computer import Computer


class Map(Computer):

    def __init__(self, function: str, **fkwargs):
        super().__init__()

        self.function = function
        self.fkwargs = fkwargs

        fkwargs_str = ""
        for k, v in fkwargs.items():
            fkwargs_str = fkwargs_str + '\n' + k + "=" + str(v)
        self.name = "Map " + function + fkwargs_str

    def render(self, template_manager, child, backend_builder) -> str:
        template_file = backend_builder.map()
        template = template_manager.get_template(template_file)

        rendered_template = template.render(function=self.function,
                                            fargs=self.fkwargs.items(),
                                            child=child)

        return rendered_template
