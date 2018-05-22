from gym_minigrid.extendedminigrid import *
from gym_minigrid.perception import Perception

AGENT_GRID_LOCATION = 2


class Evaluator:

    @staticmethod
    def evaluate(action, env, reward, done, info):

        # check goal
        if ExMiniGridEnv.worldobj_in_front_agent(env, 0) == 'goal' and action == 2:
            reward = 100
            done = True
            info = {'goal': 1}
            print('Goal!')

        # check unsafe action
        if ExMiniGridEnv.worldobj_in_front_agent(env, 0) == 'unsafe' and action == 2:
            reward = -100
            done = True
            info = {'unsafe_action': 1}
            print('Booooooo!')

        return reward, done, info
