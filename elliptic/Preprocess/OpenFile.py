
class Preprocessor(object):
    """Opens a file defined in the input-file option under the [General]
    section of the config file.
    """
    def __init__(self, configs):
        self.configs = configs
        self.input_file = configs['General']['input-file']

    def run(self, moab):
        self.moab = moab
        try:
            self.moab.load_file(self.input_file)
        except Exception as e:
            print "Error reading input file"
            print e
            exit()

    @property
    def input_file(self):
        return self._input_file

    @input_file.setter
    def input_file(self, filename):
        if not filename:
            raise ValueError("Must have a input_file option "
                             "under the [General] section in the config "
                             "file.")

        self._input_file = filename
