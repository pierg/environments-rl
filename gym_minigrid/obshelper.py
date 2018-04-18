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
    def is_immediate_to_worldobj(object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 1
        :param object_type: type of WorldObj
        :return: True / False
        """
        # 4 cases. the agent is facing the danger (if it performs forward it goes into the object_type)
        return True

    @staticmethod
    def is_near_to_worldobj(object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 2
        :param object_type: type of WorldObj
        :return: True / False
        """
        # 12 cases
        return True

    @staticmethod
    def is_water_in_front_of_agent(observation, view_size):
        return ObsHelper.is_unsafe_approach(observation, view_size, Water)

    def is_facing_water(obs):
        # Use the agent observations to determine if there is water in the first tile in front of the agent
        # for testing we return true/false according to the string passed as parameter
        return obs == 'facing_water'

    @staticmethod
    def is_near_water(obs):
        # Use the agent observations to determine if there is water in from the second
        # tile on around its observation
        # for testing we return true/false according to the string passed as parameter
        return obs == 'near_water'

    @staticmethod
    def is_inside_water(obs):
        # for testing we return true/false according to the string passed as parameter
        return obs == 'inside_water'

    @staticmethod
    def is_door_closed_ahead(observation):
        # Use the agent observations to determine if there is a door in the first tile in front of the agent
        return False

    @staticmethod
    def is_empty_ahead(observation):
        # Use the agent observations to determine if there is an empty cell in front of the agent
        # (the door is already open)
        return False


    @staticmethod
    def is_light_on(observation):
        # Return true if the space ahead of the agent is visible to the agent
        return True
