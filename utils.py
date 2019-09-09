import json
import os
import configparser


def get_dirs(path):
    return [os.path.join(path, filename) for filename in os.listdir(path) if os.path.isdir(os.path.join(path, filename))]


def parse_json_props(obj):
    return
    with open(os.path.join(obj.path, "props.json")) as json_file:
        props = json.load(json_file)
        for key, value in props.items():
            setattr(obj, key, value)
