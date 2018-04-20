import math
from minigrid import Water

# Helper class to analyse agent's observations
# All the methods should return True/False
class ObsHelper():


    @staticmethod
    """ This is a helper method, classes to check for must be specified in a function, see is_water_inf_front_of_agent """
    def is_unsafe_in_front_of_agent(observation, view_size, unsafe):
        """ Returns True or False if the tile ahead is an unsafe tile for the agent
            :param observation: An observation grid to investigate
            :param view_size: The agents view size
            :param unsafe: A type that is deemed as unsafe for the agent
            :return: True / False"""
        return isinstance(observation.get((math.floor(view_size / 2)), view_size - 2), unsafe)

    @staticmethod
    def is_water_in_front_of_agent(observation, view_size):
        return ObsHelper.is_unsafe_in_front_of_agent(observation, view_size, Water)

    @staticmethod
    def is_immediate_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 1
        :param object_type: type of WorldObj
        :return: True / False
        """
        # 4 cases. the agent is facing the danger (if it performs forward it goes into the object_type)
        raise NotImplementedError

    @staticmethod
    def is_near_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 2
        :param object_type: type of WorldObj
        :return: True / False
        """
        # 12 cases
        raise NotImplementedError

    @staticmethod
    def is_ahead_of_worldobj(obs, object_type):
        """
        Return True if the cell in front of the agent contain is of type 'object_type'
        :param obs:
        :param object_type:
        :return:
        """
        # 1 case
        raise NotImplementedError
