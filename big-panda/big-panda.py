#! /usr/bin/python2.7

from flask import Flask
from argparse import ArgumentParser
import yaml
import os

DEFAULT_CONFIG_FILE_PATH = '%s/config.yml' % os.path.dirname(__file__)

# Parse a yml file to a python dict
def parse_yml_config(config_file=None):
    if config_file is not None and os.path.exists(config_file):
        with open(config_file, 'r') as yml_config:
            config = yaml.load(yml_config)
            return config
    elif os.path.exists(DEFAULT_CONFIG_FILE_PATH):
        with open(DEFAULT_CONFIG_FILE_PATH, 'r') as yml_config:
            config = yaml.load(yml_config)
            return config
    else:
        raise IOError, 'No config file found'

# Initialize the argument parser
arg_parser = ArgumentParser(description='An app that returns the amount of GET request it served')
arg_parser.add_argument('-c', '--config', help='The path of the config file that will be loaded')
args = arg_parser.parse_args()

app = Flask(__name__)

CONFIG = parse_yml_config(args.config)
# Initialize the count of requests
count = 0

# Returns the number of GET requests
@app.route("/", methods=['GET'])
def count_get_requests():
    global count
    count += 1
    return str(count)

# Runs Flask
if __name__ == "__main__":
    app.run(CONFIG['flask']['listen_address'], CONFIG['flask']['app_port'], CONFIG['flask']['debug'])
