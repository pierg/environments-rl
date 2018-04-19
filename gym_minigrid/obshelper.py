import math
from minigrid import Water

# Helper class to analyse agent's observations
# All the methods should return True/False
class ObsHelper():


    @staticmethod
    def is_unsafe_approach(observation, view_size, unsafe, in_front_of=True, ahead=2):
        """ Returns True or False if the tile ahead is an unsafe tile for the agent

            observation: An observation grid to investigate
            view_size: The agents view size
            unsafe: A type that is deemed as unsafe for the agent
            in_front_of: Check if the tile in front of the agent, default value is true, false if you want to check a tile further away
            ahead: Number of tiles ahead of the agent, default value is 2, which is the next tile in front of the agent"""
        if in_front_of:
            return isinstance(observation.get((math.floor(view_size / ahead)), view_size - ahead), unsafe)
        return isinstance(observation.get((math.floor(view_size / ahead)), view_size - ahead), unsafe)


    @staticmethod
    def is_ahead_of_worldobj(obs, object_type, distance):
        """
        Return True if "distance" cell in front of the agent contain is of type 'object_type'
        :param obs:
        :param object_type:
        :param distance: number of cells in front (1 = the one next to the agent cell)
        :return:
        """
        raise NotImplementedError


    @staticmethod
    def is_worldobj_to_left(obs, object_type):
        """
        Returns True is "object_type" is located to the left of the agent
        :param obs:
        :param object_type:
        :return:
        """
        raise NotImplementedError


    @staticmethod
    def is_worldobj_to_right(obs, object_type):
        """
        Returns True is "object_type" is located to the left of the agent
        :param obs:
        :param object_type:
        :return:
        """
        raise NotImplementedError


    @staticmethod
    def is_immediate_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 1
        :param object_type: type of WorldObj
        :return: True / False
        """
        return ObsHelper.is_ahead_of_worldobj(obs, object_type, 1)

    @staticmethod
    def is_near_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 2
        :param object_type: type of WorldObj
        :return: True / False
        """
        # 12 cases
        if ObsHelper.is_ahead_of_worldobj(obs, object_type, 2): return True
        if ObsHelper.is_worldobj_to_left(obs, object_type): return True
        if ObsHelper.is_worldobj_to_right(obs, object_type): return False
