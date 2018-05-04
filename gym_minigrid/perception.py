import math
from extendedminigrid import *
from extendedminigrid import Water

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
        if object_type is not "pattern":
            return object_type == obs.worldobj_in_front_agent(1)
        print("rentre immediate")
        return object_type == obs.worldpattern_in_front_agent(1)

    @staticmethod
    def is_near_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 2
        :param object_type: type of WorldObj
        :return: True / False
        """
        print("obj",object_type)
        if object_type != "pattern":
            print("not pattern")
            return object_type == obs.worldobj_in_front_agent(2) or \
                    object_type == obs.worldobj_in_left_agent(1) or \
                        object_type == obs.worldobj_in_right_agent(1)
        print("rentre near")
        return object_type == obs.worldpatter_is_near_agent(1)