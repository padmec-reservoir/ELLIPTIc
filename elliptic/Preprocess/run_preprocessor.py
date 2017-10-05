import argparse
import importlib

import configobj

from pymoab import core


def validate_config(configs):
    if not configs:
        print("Error: Please provide a valid config file.")
        exit()

    if not configs['General']:
        print("Error: Config file must have a [General] section")
        exit()

    if not configs['General']['output-file']:
        print ("Config file must have a valid output-file option under the "
               "[Config] section")
        exit()


def parse_config(config_file):
    if not config_file:
        return None

    try:
        configs = configobj.ConfigObj(
            config_file, file_error=True, raise_errors=True)
    except configobj.ConfigObjError as e:
        print("Error reading config file:")
        print(e)
        exit()
    except IOError as e:
        print("Error reading config file:")
        print(e)
        exit()

    validate_config(configs)

    return configs


def read_args():
    parser = argparse.ArgumentParser(
        description="Runs the provied preprocessor on a given input file.",
        usage="Preprocess [-h] [--info] config-file",
        prog="Preprocess")

    parser.add_argument(
        'config_file',
        type=str,
        help='Config file to feed the preprocessor',
        default=None)

    args = parser.parse_args()

    return args


def build_preprocessor_pipeline(module_names, configs):
    if not isinstance(module_names, list):
        print ("The pipeline option must be a list. Try appending a comma at "
               "the end of the preprocessor list.")

    preprocessor_pipeline = []
    for module_name in module_names:
        try:
            preprocessor_module = importlib.import_module(module_name)
        except ImportError:
            print("Error importing the preprocessor module {0}.".format(
                module_name))
            exit()

        preprocessor_pipeline.append(
            preprocessor_module.Preprocessor(configs))

    return preprocessor_pipeline


def export_file(moab, output_file):
    moab.write_file(output_file)


def run_preprocessor_pipeline(preprocessor_pipeline):
    moab = core.Core()
    for preprocessor in preprocessor_pipeline:
        preprocessor.run(moab)

    return moab


def run_preprocessor():
    args = read_args()

    configs = parse_config(args.config_file)
    preprocessor_pipeline = []

    if configs['Preprocessor']:
        module_names = configs['Preprocessor']['pipeline']
        if module_names:
            preprocessor_pipeline = build_preprocessor_pipeline(
                module_names, configs)
        else:
            print ("Error: Please provide a preprocessor pipeline in your "
                   "config file.")
    else:
        print ("Error: Please provide a Preprocessor section in your config "
               "file.")

    moab = run_preprocessor_pipeline(preprocessor_pipeline)

    export_file(moab, configs['General']['output-file'])


if __name__ == "__main__":
    run_preprocessor()
