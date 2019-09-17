import json
import os
import configparser
import pickle


def get_dirs(path):
    return [os.path.join(path, filename) for filename in os.listdir(path) if
            os.path.isdir(os.path.join(path, filename))]


def parse_json_props(obj):
    return
    with open(os.path.join(obj.path, "props.json")) as json_file:
        props = json.load(json_file)
        for key, value in props.items():
            setattr(obj, key, value)

def write_json(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))
        f.close()

def save_object(obj, path):
    with open(path) as f:
        pickle.dump(obj, f)


def load_object(path):
    with open(path) as f:
        return pickle.load(f)

