import collections

from helpers import config_grabber as cg

from extendedminigrid import *
from state_machines.patterns.absence import *

import gym

# Size of the history collection
N = 5


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

        # Grab configuration
        self.config = cg.Configuration.grab()

        # Action shaped by the action planner
        self.shaped_action = None

        self.propsed_action = None

        # List of automata-based monitors with their states, rewards and unsafe-actions
        self.absence_monitors = []
        # Dictionary that gets populated with information by all the monitors at runtime
        self.monitor_states = {}

        # Generates automata-based monitors
        for avoid_obj in self.config.absence_monitors:
            new_absence_monitor = Absence("absence_" + avoid_obj, avoid_obj, self.on_monitoring)
            self.absence_monitors.append(new_absence_monitor)
            self.monitor_states[new_absence_monitor.name] = {}
            self.monitor_states[new_absence_monitor.name]["state"] = ""
            self.monitor_states[new_absence_monitor.name]["shaped_reward"] = 0
            self.monitor_states[new_absence_monitor.name]["unsafe_action"] = ""

    def on_monitoring(self, name, state, **kwargs):
        """
        Callback function called by the monitors
        :param state: mismatch, violation
        :param kwargs: in case of violation it returns a reward and the action causing the violation (unsafe_aciton)
        :return: None
        """
        self.monitor_states[name]["state"] = state

        if state == "mismatch":
            print(name + " mismatch!!!!")

        if state == "monitoring":
            print(name + " monitoring")

        if state == "shaping":
            if kwargs:
                print(name + " shaping")
                shaped_reward = kwargs.get('shaped_reward', 0)
                print("     shaped_reward = " + str(shaped_reward))
                self.monitor_states[name]["shaped_reward"] = shaped_reward
            else:
                print(name + " ERROR. missing action and reward")

        if state== "violation":
            if kwargs:
                print(name + " violation blocked!!")
                unsafe_action = kwargs.get('unsafe_action')
                shaped_reward = kwargs.get('shaped_reward', 0)
                self.monitor_states[name]["unsafe_action"] = unsafe_action
                self.monitor_states[name]["shaped_reward"] = shaped_reward
                print("shaped_reward=" + str(shaped_reward) + " unsafe_action=" + str(unsafe_action))
            else:
                print(name + " ERROR. missing action and reward")

    def action_planner(self, unsafe_actions):
        """
        Return a suitable action that (that is not one of the 'unsafe_action')
        :param unsafe_actions:
        :return: safe action or proposed action
        """
        if len(unsafe_actions) == 0:
            return self.propsed_action
        else:
            print("safe action: " + str(self.env.actions.wait))
            return self.env.actions.wait



    def step(self, proposed_action, reset_on_catastrophe=False):
        # To be returned to the agent
        obs, reward, done, info = None, None, None, None

        self.propsed_action = proposed_action

        # Get current observations from the environment and decode them
        agent_obs = ExGrid.decode(self.env.gen_obs()['image'])
        agent_pos = self.env.agent_pos
        agent_dir = self.env.get_dir_vec()
        current_obs = (agent_obs, agent_pos, agent_dir)

        current_obs_env = self.env

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        # Store obs/action in history
        self.proposed_history.append((current_obs, proposed_action))

        # Check observation and proposed action in all running monitors
        for monitor in self.absence_monitors:
            print("\n\n____check BEFORE action is applyed to the environment")
            monitor.check(current_obs_env, proposed_action)

        # Check for unsafe actions before sending them to the environment:
        unsafe_actions = []
        shaped_rewards = []
        for name, monitor in self.monitor_states.items():
            if monitor["state"] == "violation":
                if self.config.on_violation_reset:
                    obs = self.env.reset()
                    done = True
                    info = {}
                if monitor["unsafe_action"]:
                    unsafe_actions.append(monitor["unsafe_action"])
                shaped_rewards.append(monitor["shaped_reward"])

        # If have to reset
        if done:
            reward = sum(shaped_rewards)
            return obs, reward, done, info

        # Build action to send to the environment
        suitable_action = self.action_planner(unsafe_actions)

        # Send a suitable action to the environment
        obs, reward, done, info = self.env.step(suitable_action)

        # Notify the monitors of the new state reached in the environment and the applied action
        for monitor in self.absence_monitors:
            print("\n____verify AFTER action is applyed to the environment")
            monitor.verify(self.env, suitable_action)

        # Get the shaped rewards from the monitors in the new state
        shaped_rewards = []
        for name, monitor in self.monitor_states.items():
            shaped_rewards.append(monitor["shaped_reward"])

        # Shape the reward at the cumulative sum of all the rewards from the monitors
        reward += sum(shaped_rewards)

        # Reset monitor rewards and actions
        for name, monitor in self.monitor_states.items():
            monitor["shaped_reward"] = 0
            monitor["unsafe_action"] = ""

        # Next line is just a test to see if get_grid_coords_from_view work as expected
        #x,y = agent_pos
        #adx,ady = agent_dir
        #ExMiniGridEnv.get_grid_coords_from_view(self,x,y,adx,ady,-2,-1)

        # Return everything to the agent
        return obs, reward, done, info
