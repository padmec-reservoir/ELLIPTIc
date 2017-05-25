from PreprocessorMixins import IOPreprocessorMixin, ConfigFilePreprocessorMixin


class Preprocessor(IOPreprocessorMixin, ConfigFilePreprocessorMixin):

    INFO = """
    Reads a gmsh file and converts its physical entities to a format that
    is understandable by ELLIPTIc.
    """

    def __init__(self, input_file, output_file, configs):
        self.input_file = input_file
        self.output_file = output_file
        self.configs = configs
