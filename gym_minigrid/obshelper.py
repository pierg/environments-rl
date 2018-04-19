import math
from minigrid import Water

# Helper class to analyse agent's observations
# All the methods should return True/False
class ObsHelper():


    @staticmethod
    def is_unsafe_approach(observation, view_size, unsafe, in_front_of=True, ahead=2):
        """ Returns True or False if the tile ahead is an unsafe tile for the agent

            :param observation: An observation grid to investigate
            :param view_size: The agents view size
            :param unsafe: A type that is deemed as unsafe for the agent
            :param in_front_of: Check if the tile in front of the agent, default value is true, false if you want to check a tile further away
            :param ahead: Number of tiles ahead of the agent, default value is 2, which is the next tile in front of the agent
            :return: True / False"""
        if in_front_of:
            return isinstance(observation.get((math.floor(view_size / ahead)), view_size - ahead), unsafe)
        return isinstance(observation.get((math.floor(view_size / ahead)), view_size - ahead), unsafe)

    @staticmethod
    def is_water_in_front_of_agent(observation, view_size):
        return ObsHelper.is_unsafe_approach(observation, view_size, Water)

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
