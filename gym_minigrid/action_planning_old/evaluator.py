from gym_minigrid.extendedminigrid import *
from gym_minigrid.perception import Perception

AGENT_GRID_LOCATION = 2


class Evaluator:

    @staticmethod
    def evaluate(action, obs, reward, done, info):

        # check goal
        if Perception.is_ahead_of_worldobj(obs, Goal, 1) and action == 2:
            reward = 100
            done = True
            info = {'goal': 1}
            print('Goal!')

        # check unsafe action
        if Perception.is_ahead_of_worldobj(obs, Hazard, 1) and action == 2:
            reward = -100
            done = True
            info = {'unsafe_action': 1}
            print('Booooooo!')

        return reward, done, info
