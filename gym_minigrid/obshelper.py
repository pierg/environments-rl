import math
from minigrid import AGENT_VIEW_SIZE
from minigrid import  Water

AGENT_GRID_LOCATION = 2

# Helper class to analyse agent's observations
# All the methods should return True/False

class ObsHelper():


    """ This is a helper method,
        classes to check for must be specified in a function,
        see is_water_inf_front_of_agent """
    @staticmethod
    def is_unsafe_in_front_of_agent(observation, view_size, unsafe):
        """ Returns True or False if the tile ahead is an unsafe tile for the agent
            :param observation: An observation grid to investigate
            :param view_size: The agents view size
            :param unsafe: A type that is deemed as unsafe for the agent
            :return: True / False"""
        x = (math.floor(view_size / AGENT_GRID_LOCATION))
        y = view_size - AGENT_GRID_LOCATION
        type = observation.get(x, y)
        return isinstance(type, unsafe)

    """ Use this to check for water in front of the agent"""
    @staticmethod
    def is_water_in_front_of_agent(observation, view_size):
        return ObsHelper.is_unsafe_in_front_of_agent(observation, view_size, Water)

    @staticmethod
    def testObs(observation, view_size, unsafe, in_front_of=True, ahead=2):
        x = math.floor(view_size / ahead)
        y = view_size - ahead
        type = observation.get(x, y)
        result = isinstance(type, unsafe)
        if result:
            return True
        else:
            return False


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
        if ObsHelper.is_worldobj_to_right(obs, object_type): return True
        return False
