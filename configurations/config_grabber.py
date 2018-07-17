import os
import json
from collections import namedtuple


class Configuration():

    @staticmethod
    def grab(filename="main"):
        """

        :return: Specific configuration file as a python object
        """
        config_file_path = os.path.abspath(__file__ + "/../../../" + "/gym-minigrid/configurations/" + filename + ".json")
        config = None
        with open(config_file_path, 'r') as jsondata:
            configdata = jsondata.read()
            config = json.loads(configdata, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return config

    @staticmethod
    def set(key, value, filename="main"):

        config_file_path = os.path.abspath(
            __file__ + "/../../../" + "/gym-minigrid/configurations/" + filename + ".json")

        with open(config_file_path, "r") as jsondata:
            data = json.load(jsondata)

        data[key] = value

        with open(config_file_path, "w") as jsondata:
            json.dump(data, jsondata, indent=4)