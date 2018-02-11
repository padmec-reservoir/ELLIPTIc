from elliptic.Backend.DynamicCompiler import TemplateManagerBase


class PythonTemplateManager(TemplateManagerBase):

    def __init__(self) -> None:
        super().__init__(__package__, 'Templates')
