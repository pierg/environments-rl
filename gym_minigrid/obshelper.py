from transitions import Machine, State

from minigrid import *
import random


# Helper class to analyse agent's observations
class ObsHelper():


    @staticmethod
    def is_water_approaching(obs):
        # Use the agent observations to determine in there is water in the second tile in front of the agent
        return False

    @staticmethod
    def is_door_in_front(obs):
        # Use the agent observations to determine in there is a door in the first tile in front of the agent
        return False