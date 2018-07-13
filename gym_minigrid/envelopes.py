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

        self.safe_actions = None


    def step(self, proposed_action):

        if proposed_action == "observe":
            self.controller.observe(self.env)
            self.safe_actions = self.controller.get_available_actions()
            print("available_actions: " + str(self.safe_actions))
        else:
            if self.config.num_processes == 1 and self.config.rendering:
                self.env.render('human')

            # check if the proposed action is safe
            if self.env.action_to_string(proposed_action) in self.safe_actions:
                action = self.env.action_to_string(proposed_action)
                print("action_to_execution: " + action)
                obs, reward, done, info = self.env.step(proposed_action)
                reward += self.respected_reward
            else:
                if 'observation' in self.safe_actions:
                    print("MISMATCH! No available actions from these observations in the MTSA model")
                    print("Going back to S01M1")
                    action = "to_S0M1"
                    obs, reward, done, info = self.env.step(proposed_action)
                else:
                    action = random.choice(self.safe_actions)
                    print("the proposed action is not safe! Choosing a random safe action...")
                    print("action_to_execution: " + action)
                    obs, reward, done, info = self.env.step(self.env.str_to_action(action))
                    reward += self.violated_reward

            self.controller.act(action)

            return obs, reward, done, info
