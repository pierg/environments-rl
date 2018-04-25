import collections
from perception import Perception

from helpers import config_grabber as cg

from extendedminigrid import *

# Size of the history collection
N = 5

# Negative reward when trying to enter a catastrophic area
NEGATIVE_REWARD_CATASTROPHE = -2

class SafetyEnvelope(gym.core.Wrapper):
    """
    Safety envelope for safe exploration.
    The purpose is to detect dangerous actions and block them sending back a modified reward
    """

    def __init__(self, env):
        super(SafetyEnvelope, self).__init__(env)
        # Stores history of the last N observation / proposed_actions
        self.proposed_history = collections.deque(N*[(None, None)], N)
        # Stores history of the last N observation / applied_actions
        self.actual_history = collections.deque(N * [(None, None)], N)

        self.reset_on_catastrophe = self.config.reset_catastrofe

        # Grab configuration
        self.config = cg.Configuration.grab()

        # Reward safety action set by the monitor in case of violation
        self.shaped_reward = None
        self.shaped_action = None


    def step(self, action, reset_on_catastrophe=False):
        # Get current observations from the environment and decode them
        current_obs = ExGrid.decode(self.env.gen_obs()['image'])

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        # Store obs/action in history
        proposed_action = action
        self.proposed_history.append((current_obs, proposed_action))

        if self.monitor(current_obs, proposed_action):
            if self.config.on_catastrofe == "reset":
                obs = self.env.reset()
                reward = self.shaped_reward
                done = True
                info = {'catastrophe': 1}
            elif self.config.on_catastrofe == "keep_going":
                safe_action = self.env.wait
                obs, reward, done, info = self.env.step(safe_action)
                reward = NEGATIVE_REWARD_CATASTROPHE
                info = {'catastrophe': 1}
            else:
                print(self.config.on_catastrofe + " not implemented")
                raise NotImplementedError
        else:
            obs, reward, done, info = self.env.step(proposed_action)



        self.actual_history.append((current_obs, safe_action))

        # Apply the agent action to the environment or a safety action
        mod_reward = reward


        return obs, mod_reward, done, info

    def monitor(self, observation, proposed_action):
        """

        :param observation:
        :param proposed_action:
        :return:
        """



        # Block if the agent is in front of the water and want to go forward
        return Perception.is_ahead_of_worldobj(observation, Water, 1) \
               and proposed_action == MiniGridEnv.Actions.forward


