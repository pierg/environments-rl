import random

from configurations import config_grabber as cg

from extendedminigrid import *
from mtsa.controller import *

import gym


class SafetyEnvelope(gym.core.Wrapper):
    """
    Safety envelope for safe exploration.
    Uses controllers for avoiding unsafe actions and shaping rewards
    """

    def __init__(self, env):
        super(SafetyEnvelope, self).__init__(env)

        # Grab configuration
        self.config = cg.Configuration.grab()

        # State Machine MTSA controller
        self.controller = Controller()

        # Set controller rewards
        self.respected_reward = 0.1
        self.violated_reward = -0.1

        # Set standard rewards
        self.step_reward = self.config.rewards.standard.step
        self.goal_reward = self.config.rewards.standard.goal
        self.death_reward = self.config.rewards.standard.death

        # Counters of steps performed in an episode
        self.n_steps = 0


    def step(self, proposed_action):

        action = None

        # To be returned to the agent
        obs, reward, done, info = None, None, None, None

        self.controller.observe(self.env)

        safe_actions = self.controller.get_available_actions()

        print("available_actions: " + str(safe_actions))

        # check if the proposed action is safe
        if self.env.action_to_string(proposed_action) in safe_actions:
            action = self.env.action_to_string(proposed_action)
            print("action_to_execution: " + action)
            obs, reward, done, info = self.env.step(proposed_action)
            reward += self.respected_reward
        else:
            action = random.choice(safe_actions)
            print("action_to_execution: " + action)
            obs, reward, done, info = self.env.step(self.env.str_to_action(action))
            reward += self.violated_reward

        self.controller.act(action)

        return obs, reward, done, info
