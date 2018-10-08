import collections

from configurations import config_grabber as cg

from extendedminigrid import *
from monitors.patterns.precedence import *
from monitors.patterns.absence import *
from monitors.patterns.universality import *
from monitors.patterns.response import *
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

        # Dictionary that contains all the type of monitors you can use
        dict_monitors = {'precedence': Precedence,
                         'response': Response,
                         'universality': Universality,
                         'absence': Absence}

        for monitor_types in self.config.monitors:
            for monitors in monitor_types:
                for monitor in monitors:
                    if monitor.active:
                        if hasattr(monitor, 'conditions'):
                            new_monitor = dict_monitors[monitor.type](monitor.type + "_" + monitor.name,
                                                                      monitor.conditions, self._on_monitoring,
                                                                      monitor.rewards, self.perception, monitor.context)
                        self.meta_monitor.append(new_monitor)
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
        for monitor in self.meta_monitor:
            print(monitor)
        self._reset_monitors()

    def _on_monitoring(self, name, state, **kwargs):
        """
        Callback function called by the monitors
        :param state: mismatch, violation
        :param kwargs: in case of violation it returns a reward and the action causing the violation (unsafe_aciton)
        :return: None
        """

        # if self.monitor_states[name] == ""

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
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.done))
                    safe_action = self.env.actions.done
                if unsafe_action[1] == "turn_right":
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.right))
                    safe_action = self.env.actions.right
                if unsafe_action[1] == "toggle":
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.toggle))
                    safe_action = self.env.actions.toggle
                if unsafe_action[1] == "turn_left":
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.left))
                    safe_action = self.env.actions.left
                if unsafe_action[1] == "forward":
                    logging.info("action_planner() -> safe action : %s", str(self.env.actions.forward))
                    safe_action = self.env.actions.forward
        return safe_action

    def _reset_monitors(self):
        """
        Reset all monitors initial state to avoid mismatch errors on environment reset
        """
        for monitor in self.meta_monitor:
            monitor.reset()



    def step(self, proposed_action):
        if self.config.debug_mode: print("proposed_action = " + self.env.action_to_string(proposed_action))

        # To be returned to the agent
        obs, reward, done, info = None, None, None, None

        list_violations = []

        self.propsed_action = proposed_action

        self.perception.update(self.env.gen_obs_decoded())

        current_obs_env = self.env

        # Rendering
        if self.config.a2c.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        active_monitors = []

        # Active the monitors according to the context:
        for monitor in self.meta_monitor:
            active = monitor.activate_contextually()
            if active:
                active_monitors.append(monitor)


        for monitor in active_monitors:
            monitor.check(current_obs_env, proposed_action)


        # Check for unsafe actions before sending them to the environment:
        unsafe_actions = []
        shaped_rewards = []
        for name, monitor in self.monitor_states.items():
            if monitor["state"] == "violation" or monitor["state"] == "precond_violated" or monitor["state"] == "postcond_violated" :
                list_violations.append(name)
                if "unsafe_action" in monitor:
                    # Add them only if the monitor is in enforcing mode
                    if monitor["mode"] == "enforcing":
                        unsafe_actions.append((monitor["unsafe_action"], monitor["action_planner"]))
                        if self.config.debug_mode: print("VIOLATION:\t" + name + "\tunsafe_action: " +
                            self.env.action_to_string(monitor["unsafe_action"]) +
                            "\taction_planner: " +
                            monitor["action_planner"])
                shaped_rewards.append(monitor["shaped_reward"])

        # logging.info("unsafe actions = %s", unsafe_actions)

        # Build action to send to the environment
        suitable_action = self._action_planner(unsafe_actions)
        # logging.info("actions possibles = %s", suitable_action)

        # Send a suitable action to the environment
        obs, reward, done, info = self.env.step(suitable_action)
        if info:
            for i in range(len(list_violations)):
                info["event"].append("violation")

        # logging.info("____verify AFTER action is applied to the environment")
        # Notify the monitors of the new state reached in the environment and the applied action
        for monitor in active_monitors:
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

        if done:
            self._reset_monitors()

        logging.info("\n\n\n")

        return obs, reward, done, info


class LightSafetyEnvelope(gym.core.Wrapper):
    """
    Safety envelope for safe exploration.
    Uses monitors for avoiding unsafe actions and shaping rewards
    """

    def __init__(self, env):
        super(LightSafetyEnvelope, self).__init__(env)

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