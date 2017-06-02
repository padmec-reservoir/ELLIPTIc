
class ConfigFilePreprocessorMixin(object):
    """ Preprocessor that must have a defined config_file argument.
    """
    @property
    def configs(self):
        return self._configs

    @configs.setter
    def configs(self, configs):
        if not configs:
            raise ValueError("Config file cannot be empty")
        try:
            configs['General']
        except KeyError:
            raise ValueError("Config file must have a [General] section")
        try:
            self.input_file = configs['General']['input-file']
            self.output_file = configs['General']['output-file']
        except KeyError:
            raise ValueError("Config file must have valid input-file and "
                             "output-file options under the [Config] section")
        self._configs = configs
