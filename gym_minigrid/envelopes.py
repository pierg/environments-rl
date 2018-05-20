
import collections

from helpers import config_grabber as cg

from unsafe import *

# Size of the history collection
N = 5

# Negative reward when trying to enter a catastrophic area
NEGATIVE_REWARD_CATASTROPHE = -2

class SafetyEnvelope(gym.core.RewardWrapper):
    """
    Safety envelope for safe exploration.
    The purpose is to detect dangerous actions and block them sending back a modified reward
    """
    def __init__(self, env):
        super().__init__(env)

        # Grab configuration
        self.config = cg.Configuration.grab()

        self.reward_water = int(self.config.reward_water)

        # Stores history of the last N observation / proposed_actions
        self.proposed_history = collections.deque(N*[(None, None)], N)

        # Stores history of the last N observation / applied_actions
        self.actual_history = collections.deque(N * [(None, None)], N)

        self.number_of_catastrophes = 0

    def step(self, action):
        # Get current observations from the environment and decode them
        current_obs = UnsafeGrid.decode(self.env.gen_obs()['image'])

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        proposed_action = action

        self.proposed_history.append((current_obs, proposed_action))

        safe_action = proposed_action

        info = {}

        if self.blocker(proposed_action):
            if self.config.blocker:
                # Change action to wait
                safe_action = UnsafeMiniGridEnv.Actions.wait
                obs, reward, done, info = self.env.step(safe_action)
                reward = self.reward_water
            else:
                obs, reward, done, info = self.env.step(safe_action)
                done = True
            # An unction that is unsafe for the robot was performed
            self.number_of_catastrophes = self.number_of_catastrophes + 1
            info = {'catastrophe': True}
        else:
            obs, reward, done, info = self.env.step(safe_action)

        self.actual_history.append((current_obs, safe_action))

        # Apply the agent action to the environment or a safety action
        mod_reward = reward

        return obs, mod_reward, done, info

    def blocker(self, action):
        """
        A blocker that prevents unsafe actions from occuring
        :param action: the action proposed by the agent
        :return: true or false if the suggested action was blocked
        """
        if action == UnsafeMiniGridEnv.Actions.forward:
            world_obj = self.env.world_object_type_in_front_of_agent()
            return isinstance(world_obj, Water)
        return False


