import os
import json
from collections import namedtuple


class Configuration():

    @staticmethod
    def grab(filename="main"):
        """

        :return: Specific configuration file as a python object
        """
        # Assumption: baby-ai-game repo folder is located in the same folder containing gym-minigrid repo folder
        config_file_path = os.path.abspath(__file__ + "/../../../" + "/gym-minigrid/configurations/" + filename + ".json")
        config = None
        with open(config_file_path, 'r') as jsondata:
            configdata = jsondata.read()
            config = json.loads(configdata, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return config

