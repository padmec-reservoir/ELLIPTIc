
class IOPreprocessorMixin(object):
    """ Preprocessor that must have defined input_file and
    output_file arguments.
    """
    @property
    def input_file(self):
        return self._input_file

    @input_file.setter
    def input_file(self, input_file):
        if not input_file:
            raise Exception("Input file cannot be empty")
        self._input_file = input_file

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, output_file):
        if not output_file:
            raise Exception("output file cannot be empty")
        self._output_file = output_file


class ConfigFilePreprocessorMixin(object):
    """ Preprocessor that must have a defined config_file argument.
    """
    @property
    def configs(self):
        return self._configs

    @configs.setter
    def configs(self, configs):
        if not configs:
            raise Exception("Config file cannot be empty")
        self._configs = configs
