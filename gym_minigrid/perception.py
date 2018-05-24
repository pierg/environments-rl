import math
from gym_minigrid.extendedminigrid import *
from gym_minigrid.extendedminigrid import Water

AGENT_GRID_LOCATION = 2

# Helper class to analyse agent's observations
# All the methods should return True/False

class Perception():

    @staticmethod
    def is_immediate_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 1
        :param object_type: type of WorldObj
        :param distance: number of cells from the agent (1 = the one next to the agent cell)
        :return: True / False
        """
        return object_type == obs.worldobj_in_agent(1, 0)


    @staticmethod
    def is_near_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 2
        :param object_type: type of WorldObj
        :return: True / False
        """
        return  object_type == obs.worldobj_in_agent(2, 0) or \
                object_type == obs.worldobj_in_agent(1, 1) or \
                object_type == obs.worldobj_in_agent(1, 1)

    @staticmethod
    def is_condition_satisfied(env, condition):
        """

        :param env: instance of ExMiniGridEnv
        :return:
        """
        if condition == "light-on-current-room":
            # Returns true if the lights are on in the room the agent is currently in
            return True

        elif condition == "light-switch-turned-on":
            # It looks for a light switch around its field of view and returns true if it is on
            return True

        elif condition == "door-opened-in-front":
            # Returns true if the agent is in front of an opened door
            return True

        elif condition == "door-closed-in-front":
            # Returns true if the agent is in front of an opened door
            return True

        elif condition == "deadend-in-front":
            # Returns true if the agent is in front of a deadend
            # deadend = all the tiles surrounding the agent view are 'wall' and the tiles in the middle are 'None'
            return True


