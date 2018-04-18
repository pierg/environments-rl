
# Helper class to analyse agent's observations
# All the methods should return True/False
class ObsHelper():


    @staticmethod
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
    def is_door_closed_ahead(obs):
        # Use the agent observations to determine if there is a door in the first tile in front of the agent
        return False

    @staticmethod
    def is_empty_ahead(obs):
        # Use the agent observations to determine if there is an empty cell in front of the agent
        # (the door is already open)
        return False


    @staticmethod
    def is_light_on(obs):
        # Return true if the space ahead of the agent is visible to the agent
        return True
