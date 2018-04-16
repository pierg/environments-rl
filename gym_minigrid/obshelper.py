
# Helper class to analyse agent's observations
class ObsHelper():


    @staticmethod
    def is_water_approaching(obs):
        # Use the agent observations to determine if there is water in the second tile in front of the agent
        # obs = obs
        return True

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
