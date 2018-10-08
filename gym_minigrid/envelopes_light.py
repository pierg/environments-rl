
from configurations import config_grabber as cg

from extendedminigrid import *
from perception import Perception

import gym



class SafetyEnvelope(gym.core.Wrapper):
    """
    Safety envelope for safe exploration.
    Uses monitors for avoiding unsafe actions and shaping rewards
    """

    def __init__(self, env):
        super(SafetyEnvelope, self).__init__(env)

        # Grab configuration
        self.config = cg.Configuration.grab()

        # Action proposed by the agent
        self.propsed_action = None

        # Action proposed by the monitor
        self.shaped_action = None

        # List of all monitors with their states, rewards and unsafe-actions
        self.meta_monitor = []

        # Dictionary that gets populated with information by all the monitors at runtime
        self.monitor_states = {}

        # Perceptions of the agent, it gets updated at each step with the current observations
        self.perception = Perception(env.gen_obs_decoded())

        # Set rewards
        self.step_reward = self.config.rewards.standard.step
        self.goal_reward = self.config.rewards.standard.goal
        self.death_reward = self.config.rewards.standard.death

    def step(self, proposed_action):
        if self.config.debug_mode: print("proposed_action = " + self.env.action_to_string(proposed_action))
        self.perception.update(self.env.gen_obs_decoded())

        # Rendering
        if self.config.a2c.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        n_violations = 0
        shaped_reward = 0
        safe_action = proposed_action

        # Checking waterAbsence
        if self.perception.is_condition_satisfied("stepping-on-water", proposed_action):
            n_violations += 1
            shaped_reward -= 0.1
            safe_action = self.env.actions.done

        # Checking lightUniversally
        if not self.perception.is_condition_satisfied("light-on-current-room"):
            n_violations += 1
            shaped_reward -= 0.1
            safe_action = self.env.actions.done

        # Checking lightPrecedence
        if (self.perception.is_condition_satisfied("entering-a-room", proposed_action)
                and not self.perception.is_condition_satisfied("light-switch-turned-on")):
            n_violations += 1
            shaped_reward -= 0.1
            safe_action = self.env.actions.right

        # Checking openDoorResponse
        if (self.perception.is_condition_satisfied("door-closed-in-front")
                and proposed_action != self.env.actions.toggle):
            n_violations += 1
            shaped_reward -= 0.1
            safe_action = self.env.actions.toggle


        # Checking switchOffResponse
        if (self.perception.is_condition_satisfied("light-switch-in-front-off")
                and proposed_action != self.env.actions.toggle):
            n_violations += 1
            shaped_reward -= 0.1
            safe_action = self.env.actions.toggle


        # Send a suitable action to the environment
        obs, reward, done, info = self.env.step(safe_action)

        # Shape the reward at the cumulative sum of all the rewards from the monitors
        reward += shaped_reward

        for i in range(n_violations):
            info["event"].append("violation")


        return obs, reward, done, info