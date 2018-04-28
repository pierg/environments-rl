import collections
from .perception import Perception

from helpers import config_grabber as cg

from .extendedminigrid import *
from .action_planning import ActionPlanner

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

        # Stores history of the last N observation / proposed_actions
        self.proposed_history = collections.deque(N * [(None, None)], N)

        # Stores history of the last N observation / applied_actions
        self.actual_history = collections.deque(N * [(None, None)], N)

        self.reset_on_catastrophe = self.config.reset_catastrofe

    def step(self, action, reset_on_catastrophe=False):
        # Get current observations from the environment and decode them
        current_obs = ExGrid.decode(self.env.gen_obs()['image'])

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
        return Perception.is_ahead_of_worldobj(observation, Water, 1) \
               and action == MiniGridEnv.Actions.forward


#######################################################################################

class ActionPlannerEnvelope(gym.core.RewardWrapper):
    """
    Action Planner Envelope
    Decides what actions to take after a safety hazard has been detected
    """

    def __init__(self, env):
        super().__init__(env)

        self.config = cg.Configuration.grab()

        self.proposed_history = collections.deque(N * [(None, None)], N)
        self.actual_history = collections.deque(N * [(None, None)], N)

    def step(self, action):
        current_obs = ExGrid.decode(self.env.gen_obs()['image'])

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        proposed_action = action
        self.proposed_history.append((current_obs, proposed_action))

        # needs some thought
        # start
        if Perception.is_ahead_of_worldobj(current_obs, Hazard, 1):
            planned_action = ActionPlanner().plan(current_obs)
            obs, reward, done, info = self.env.step(planned_action)
        else:
            obs, reward, done, info = self.env.step(proposed_action)
        # end

        return obs, reward, done, info

        # TODO add safety measurement

        # TODO add action planner
