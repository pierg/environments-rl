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


import os


import json
from collections import namedtuple

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

        # Assumption: baby-ai-game repo folder is located in the same folder containing gym-minigrid repo folder
        config_file_path = os.path.abspath(__file__ + "/../../../" + "/baby-ai-game/configurations/main.json")
        with open(config_file_path, 'r') as jsondata:
            configdata = jsondata.read()
            self.config = json.loads(configdata,
                                     object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

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

        for i in current_obs.grid:
            if i is not None:
                print("WAIT!")

        self.proposed_history.append((current_obs, proposed_action))

        safe_action = proposed_action

        if proposed_action == MiniGridEnv.Actions.forward:
            if self.blocker(current_obs):
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
        else:
            obs, reward, done, info = self.env.step(safe_action)

        self.actual_history.append((current_obs, safe_action))

        # Apply the agent action to the environment or a safety action

        mod_reward = reward


        return obs, mod_reward, done, info

    def blocker(self, observation):
        return ObsHelper.testObs(observation, AGENT_VIEW_SIZE, Water)


