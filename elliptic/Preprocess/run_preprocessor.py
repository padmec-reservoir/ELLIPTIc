import argparse
import importlib
import configobj


def parse_config(config_file):
    if not config_file:
        return None

    try:
        config = configobj.ConfigObj(
            config_file, file_error=True, raise_errors=True)
    except configobj.ConfigObjError as e:
        print "Error reading config file:"
        print e
        exit()
    except IOError as e:
        print "Error reading config file:"
        print e
        exit()

    if not config:
        print ("Error: Please provide a valid config file.")
        exit()

    return config


def read_args():
    parser = argparse.ArgumentParser(
        description="Runs the provied preprocessor on a given input file.",
        usage="Preprocess [-h] [--info] preprocessor [config-file]",
        prog="Preprocess")
    parser.add_argument(
        'preprocessor',
        type=str,
        help='Preprocessor module to be used',
        default=None)

    parser.add_argument(
        'config_file',
        type=str,
        help='Config file to feed the preprocessor',
        default=None)

    parser.add_argument(
        '--info',
        action='store_true',
        help='Displays info regarding the given preprocessor')

    args = parser.parse_args()

    return args


def run_preprocessor():
    args = read_args()

    try:
        preprocessor_module = importlib.import_module(args.preprocessor)
    except ImportError:
        print "Error: Preprocessor module not found."
        exit()

    if args.info:
        print preprocessor_module.Preprocessor.INFO
        exit()

    configs = parse_config(args.config_file)

    preprocessor = preprocessor_module.Preprocessor(configs)

    preprocessor.run()


if __name__ == "__main__":
    run_preprocessor()
