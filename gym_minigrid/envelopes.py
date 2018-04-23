
import collections
from obshelper import ObsHelper

from helpers import config_grabber as cg

from minigrid import *

# Size of the history collection
N = 5

# Negative reward when trying to enter a catastrophic area
NEGATIVE_REWARD_CATASTROPHE = -2

class SafetyEnvelope(gym.core.RewardWrapper):
    """
    Safety envelope for safe exploration.
    The purpose is to detect dangerous actions and block them sending back a modified reward
    """


    def __init__(self, env, reset_on_catastrophe=False):
        super().__init__(env)

        # Grab configuration
        self.config = cg.Configuration.grab()

        # Stores history of the last N observation / proposed_actions
        self.proposed_history = collections.deque(N*[(None, None)], N)

        # Stores history of the last N observation / applied_actions
        self.actual_history = collections.deque(N * [(None, None)], N)

        self.reset_on_catastrophe = reset_on_catastrophe

    def step(self, action, reset_on_catastrophe=False):
        # Get current observations from the environment and decode them
        current_obs = Grid.decode(self.env.gen_obs()['image'])

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        proposed_action = action

        self.proposed_history.append((current_obs, proposed_action))

        safe_action = proposed_action

        if self.blocker(current_obs, proposed_action):
            if self.reset_on_catastrophe:
                obs = self.env.gen_obs()
                reward = NEGATIVE_REWARD_CATASTROPHE
                done = True
                info = {'catastrophe': 1}
            else:
                safe_action = MiniGridEnv.Actions.wait
                obs, reward, done, info = self.env.step(safe_action)
                reward = NEGATIVE_REWARD_CATASTROPHE
                info = {'catastrophe': 1}
        else:
            obs, reward, done, info = self.env.step(safe_action)



        self.actual_history.append((current_obs, safe_action))

        # Apply the agent action to the environment or a safety action
        mod_reward = reward

        return obs, mod_reward, done, info

    def blocker(self, observation, action):
        # Specifies all the cases when the blocker has to be triggered..

        # Block if the agent is in front of the water and want to go forward
        return ObsHelper.is_ahead_of_worldobj(observation, Water, 1) \
               and action == MiniGridEnv.Actions.forward


