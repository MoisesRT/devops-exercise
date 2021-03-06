#! /usr/bin/python2.7

from flask import Flask, Response, send_from_directory
from argparse import ArgumentParser
import yaml
import os
import json

DEFAULT_CONFIG_FILE_PATH = '%s/config.yml' % os.path.dirname(__file__)
RESOURCE_DIR_PATH = '%s/resources' % os.path.dirname(__file__)

# Parse a yml file to a python dict
def parse_yml_config(config_file=None):
    # Tries to load the config file given to the function
    if config_file is not None and os.path.exists(config_file):
        with open(config_file, 'r') as yml_config:
            config = yaml.load(yml_config)
            return config

    # Tries to load the default config file
    elif os.path.exists(DEFAULT_CONFIG_FILE_PATH):
        with open(DEFAULT_CONFIG_FILE_PATH, 'r') as yml_config:
            config = yaml.load(yml_config)
            return config
    else:
        raise IOError, 'No config file found'

# Checks that the config is valid
def validate_config():
    # Checks that the resource directory exists and if it is a directory and not a plain file
    if os.path.isdir(RESOURCE_DIR_PATH) and os.path.exists(RESOURCE_DIR_PATH):
        pass
    elif not os.path.exists(RESOURCE_DIR_PATH):
        raise IOError, 'The path for the resource directory does not exists'
    elif not os.path.isdir(RESOURCE_DIR_PATH):
        raise IOError, 'No the path provided for the resource directory is not a directory'

# Create an argument parser
arg_parser = ArgumentParser(description='An app that serves files from a specified static directory')
arg_parser.add_argument('-c', '--config', help='The path of the config file that will be loaded')
args = arg_parser.parse_args()

# Load the config
CONFIG = parse_yml_config(args.config)
validate_config()
app = Flask(__name__)

# A function that prints a list with all the files available in the resource directory
@app.route("/", methods=['GET'])
def get_file_list():
    files = [f for f in os.listdir(RESOURCE_DIR_PATH) if
             os.path.isfile(os.path.join(RESOURCE_DIR_PATH, f))]
    return Response(response=json.dumps(files), mimetype='application/json')

# A function that returns to the user the file he asked for
@app.route("/<file_name>", methods=['GET'])
def get_file(file_name):
    if os.path.isfile('./%s/%s' % (RESOURCE_DIR_PATH, file_name)):
        return send_from_directory(RESOURCE_DIR_PATH, file_name)
    else:
        return 'File not found', 404

# Runs Flask
if __name__ == "__main__":
    app.run(CONFIG['flask']['listen_address'], CONFIG['flask']['app_port'], CONFIG['flask']['debug'])
