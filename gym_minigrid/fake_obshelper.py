import math
from minigrid import Water

# Helper class to analyse agent's observations
# All the methods should return True/False
class ObsHelper():


    @staticmethod
    def is_immediate_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 1
        :param object_type: type of WorldObj
        :return: True / False
        """
        # 4 cases. the agent is facing the danger (if it performs forward it goes into the object_type)
        return obs == "immediate"

    @staticmethod
    def is_near_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 2
        :param object_type: type of WorldObj
        :return: True / False
        """
        # 12 cases
        return obs == "near"


    @staticmethod
    def is_ahead_of_worldobj(obs, object_type):
        """
        Return True if the cell in front of the agent contain is of type 'object_type'
        :param obs:
        :param object_type:
        :return:
        """
        return obs == "ahead"
