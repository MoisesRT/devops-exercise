from flask import Flask, Response, send_from_directory

import yaml
import os
import json
import argparse


def parse_yml_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as yml_config:
            config = yaml.load(yml_config)
            return config

CONFIG = parse_yml_config(os.path.abspath('./config.yml'))
app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_file_list():
    files = [f for f in os.listdir(CONFIG['app']['resources_dir_path']) if
             os.path.isfile(os.path.join(CONFIG['app']['resources_dir_path'], f))]
    return Response(response=json.dumps(files), mimetype='application/json')


@app.route("/<file_name>", methods=['GET'])
def get_file(file_name):
    return send_from_directory(CONFIG['app']['resources_dir_path'], file_name)


if __name__ == "__main__":
    app.run(CONFIG['flask']['listen_address'], CONFIG['flask']['app_port'], debug=CONFIG['flask']['debug'])
