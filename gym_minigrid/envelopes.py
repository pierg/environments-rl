import collections

from configurations import config_grabber as cg

from extendedminigrid import *
from monitors.properties.avoid import *
from monitors.patterns.precedence import *
from monitors.patterns.absence import *
from monitors.patterns.universality import *
from monitors.patterns.response import *

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
        self.monitors = []

        # Dictionary that gets populated with information by all the monitors at runtime
        self.monitor_states = {}

        # Set rewards
        self.step_reward = self.config.rewards.standard.step
        self.goal_reward = self.config.rewards.standard.goal
        self.death_reward = self.config.rewards.standard.death

        # Counters of steps performed in an episode
        self.n_steps = 0

        # Dictionary that contains all the type of monitors you can use
        dict_monitors = {'avoid': Avoid,
                         'precedence': Precedence,
                         'response': Response,
                         'universality': Universality,
                         'absence': Absence}

        for monitor_types in self.config.monitors:
            for monitors in monitor_types:
                for monitor in monitors:
                    if monitor.active:
                        # Monitors with condition(s) (Absence / Precedence / Response / Universality)
                        if hasattr(monitor, 'conditions'):
                            new_monitor = dict_monitors[monitor.type](monitor.type + "_" + monitor.name,
                                                                      monitor.conditions, self._on_monitoring,
                                                                      monitor.rewards)
                        # Monitors without condition (Avoid)
                        else:
                            for j in ExMiniGridEnv.Actions:
                                if monitor.act_to_avoid == str(j):
                                    action_to_avoid = j
                            new_monitor = dict_monitors[monitor.type](monitor.type + "_" + monitor.obj_to_avoid,
                                                                      monitor.obj_to_avoid,
                                                                      action_to_avoid,
                                                                      self._on_monitoring, monitor.rewards)
                        self.monitors.append(new_monitor)
                        self.monitor_states[new_monitor.name] = {}
                        self.monitor_states[new_monitor.name]["state"] = ""
                        self.monitor_states[new_monitor.name]["shaped_reward"] = 0
                        self.monitor_states[new_monitor.name]["unsafe_action"] = ""
                        self.monitor_states[new_monitor.name]["mode"] = monitor.mode
                        if hasattr(monitor, 'action_planner'):
                            self.monitor_states[new_monitor.name]["action_planner"] = monitor.action_planner
                        else:
                            self.monitor_states[new_monitor.name]["action_planner"] = "wait"

        print("Active monitors:")
        for monitor in self.monitors:
            print(monitor)

    def _on_monitoring(self, name, state, **kwargs):
        """
        Callback function called by the monitors
        :param state: mismatch, violation
        :param kwargs: in case of violation it returns a reward and the action causing the violation (unsafe_aciton)
        :return: None
        """
        self.monitor_states[name]["state"] = state

        if state == "mismatch":
            logging.error("%s mismatch between agent's observations and monitor state!", name)

        if state == "monitoring":
            logging.info("%s is monitoring...", name)

        if state == "shaping":
            if kwargs:
                shaped_reward = kwargs.get('shaped_reward', 0)
                logging.info("%s is shaping... (shaped_reward = %s)", name, str(shaped_reward))
                self.monitor_states[name]["shaped_reward"] = shaped_reward
            else:
                logging.error("%s is in shaping error. missing action and reward", name)

        if state == "violation":
            if kwargs:
                unsafe_action = kwargs.get('unsafe_action')
                shaped_reward = kwargs.get('shaped_reward', 0)
                self.monitor_states[name]["unsafe_action"] = unsafe_action
                self.monitor_states[name]["shaped_reward"] = shaped_reward
                #logging.warning("%s is in violation...(shaped_reward=%s, unsafe_action=%s)",
                 #               name, str(shaped_reward), str(unsafe_action))
                logging.info("%s is in violation...(shaped_reward=%s, unsafe_action=%s)",
                               name, str(shaped_reward), str(unsafe_action))
            else:
                logging.error("%s is in violation error. missing action and reward", name)

    def _action_planner(self, unsafe_actions):
        """
        Return a suitable action that (that is not one of the 'unsafe_action')
        :param unsafe_actions: list of actions that would bring one or more monitors in a fail state
        :return: safe action proposed by the action planner or proposed action in case unsafe_actions is empty
        """
        safe_action = None
        if len(unsafe_actions) == 0:
            safe_action = self.propsed_action
        else:
            for unsafe_action in unsafe_actions:
                if unsafe_action[1] == "wait":
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.wait))
                    safe_action = self.env.actions.wait
                if unsafe_action[1] == "turn_right":
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.right))
                    safe_action = self.env.actions.right
                if unsafe_action[1] == "toggle_light":
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.toggle))
                    safe_action = self.env.actions.toggle
        return safe_action

    def _reset_monitors(self):
        """
        Reset all monitors initial state to avoid mismatch errors on environment reset
        """
        for monitor in self.monitors:
            monitor.reset()

    def step(self, proposed_action):

        # To be returned to the agent
        obs, reward, done, info = None, None, None, None

        saved = False
        end = False
        list_monitor = {}
        if self.n_steps == 0:
            self._reset_monitors()

        self.n_steps += 1

        if self.n_steps == self.env.max_steps:
            end = True
            self.n_steps = 0

        self.propsed_action = proposed_action

        current_obs_env = self.env

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        # logging.info("___check BEFORE action is applyed to the environmnent")

        # Check observation and proposed action in all running monitors
        for monitor in self.monitors:
            monitor.check(current_obs_env, proposed_action)
            if monitor.state == "violated":
                saved = True
                list_monitor[len(list_monitor)] = monitor.name

        # Check for unsafe actions before sending them to the environment:
        unsafe_actions = []
        shaped_rewards = []
        for name, monitor in self.monitor_states.items():
            if monitor["state"] == "violation":
                if self.config.on_violation_reset:
                    obs = self.env.reset()
                    done = True
                    info = ("violation", self.monitor_states)
                if monitor["unsafe_action"]:
                    # Add them only if the monitor is in enforcing mode
                    if monitor["mode"] == "enforcing":
                        unsafe_actions.append((monitor["unsafe_action"], monitor["action_planner"]))
                shaped_rewards.append(monitor["shaped_reward"])

        # If have to reset
        if done:
            reward = sum(shaped_rewards)
            self.n_steps = 0
            self._reset_monitors()
            return obs, reward, done, info

        # logging.info("unsafe actions = %s", unsafe_actions)

        # Build action to send to the environment
        suitable_action = self._action_planner(unsafe_actions)
        # logging.info("actions possibles = %s", suitable_action)

        # Send a suitable action to the environment
        obs, reward, done, info = self.env.step(suitable_action)
        if info:
            info = (info, self.monitor_states)

        # logging.info("____verify AFTER action is applied to the environment")
        # Notify the monitors of the new state reached in the environment and the applied action
        for monitor in self.monitors:
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

        # Check if goal reached, if yes add goal_reward
        a, b = ExMiniGridEnv.get_grid_coords_from_view(self.env, (0, 0))
        current_cell = Grid.get(self.env.grid, a, b)
        if current_cell is not None:
            if current_cell.type == "goal":
                reward = self.goal_reward
                info = ("goal", self.monitor_states)
                self.n_steps = 0

        # Check if normal step, if yes add normal_reward
        if reward == 0:
            reward = self.step_reward

        if saved and suitable_action != ExMiniGridEnv.Actions.wait:
            saved = False

        if end:
            info = ("end", self.monitor_states)
            reward += self.death_reward
        elif not info and saved:
            info = ("saved", list_monitor)
        # Return everything to the agent
        if done:
            self._reset_monitors()

        logging.info("\n\n\n")

        return obs, reward, done, info
