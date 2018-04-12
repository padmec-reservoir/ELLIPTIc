from jinja2 import Environment, PackageLoader, Template


class TemplateManagerBase:
    """Class for abstracting interactions with the `jinja2` templating package.

    Example:
        Creating a template manager that uses the `Templates` folder found
        inside the current package when searching for template files.

        >>> class MyTemplateManager(TemplateManagerBase):
        >>>     def __init__(self) -> None:
        >>>         super().__init__(__package__, 'Templates')

    Parameters:
        package: The path to a python package containing the templates folder.
        templates_folder: The name of the templates folder.
    """

    def __init__(self, package: str, templates_folder: str) -> None:
        self.jinja2_env = Environment(
            loader=PackageLoader(package, templates_folder))

    def get_template(self, template_file: str) -> Template:
        """Returns the template object corresponding to the given template file.

        Parameters:
            template_file: The template file.
        """
        return self.jinja2_env.get_template(template_file)

    def render(self, template_file: str, **kwargs: str) -> str:
        """Returns the rendered template, passing in `kwargs` as template arguments.

        Parameters:
            template_file: The template file.
            kwargs: The arguments to be passed to the template.
        """
        template = self.get_template(template_file)
        return template.render(**kwargs)