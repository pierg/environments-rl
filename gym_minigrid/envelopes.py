import math
import operator
import time

import collections
from minigrid import  AGENT_VIEW_SIZE
from functools import reduce
from obshelper import ObsHelper
import numpy as np

import gym
from gym import error, spaces, utils

from minigrid import *

# Size of the history collection
N = 5

# Negative reward when trying to enter a catastrophic area
NEGATIVE_REWARD_CATASTROPHE = -1000

class SafetyEnvelope(gym.core.RewardWrapper):
    """
    Safety envelope for safe exploration.
    The purpose is to detect dangerous actions and block them sending back a modified reward
    """

    def __init__(self, env):
        super().__init__(env)

        # Stores history of the last N observation / proposed_actions
        self.proposed_history = collections.deque(N*[(None, None)], N)

        # Stores history of the last N observation / applied_actions
        self.actual_history = collections.deque(N * [(None, None)], N)


    def step(self, action):
        # Get current observations from the environment and decode them
        current_obs = Grid.decode(self.env.gen_obs()['image'])

        proposed_action = action

        self.proposed_history.append((current_obs, proposed_action))

        safe_action = proposed_action

        if proposed_action == self.env.actions.forward:
            if self.blocker(current_obs, proposed_action):
                obs, reward, done, info = self.env.step(4)
                safe_action = self.env.actions.wait
                obs, reward, done, info = self.env.step(safe_action)
                reward = NEGATIVE_REWARD_CATASTROPHE
            else:
                obs, reward, done, info = self.env.step(safe_action)
        else:
            obs, reward, done, info = self.env.step(safe_action)

        self.actual_history.append((current_obs, safe_action))

        # Apply the agent action to the environment or a safety action

        mod_reward = reward

        # Create a window to render into
        self.env.render('human')

        return obs, mod_reward, done, info

    def blocker(self, observation, action):
        return ObsHelper.is_water_in_front_of_agent(observation, AGENT_VIEW_SIZE)


