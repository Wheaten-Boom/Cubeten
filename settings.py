import json
import os

with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as config_file:
    config = json.load(config_file)


def get_settings():
    return config


def set_settings(configuration):
    global config
    config = configuration
