import collections
from perception import Perception

from helpers import config_grabber as cg

from extendedminigrid import *
from state_machines.patterns.absence import *

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
            print(name + "Mismatch between state machine and observations!!!")

        if state == "monitoring":
            print(name + " All good")

        if state== "shaping":
            if kwargs:
                print(name + " Monitor activated...")
                shaped_reward = kwargs.get('shaped_reward', 0)
                print("shaped_reward=" + str(shaped_reward))
                self.monitor_states[name]["shaped_reward"] = shaped_reward
            else:
                print(name + " ERROR. missing action and reward")

        if state== "violation":
            if kwargs:
                print(name + " Violation Blocked!!!!")
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
        return self.env.actions.wait



    def step(self, proposed_action, reset_on_catastrophe=False):
        # Get current observations from the environment and decode them
        current_obs = ExGrid.decode(self.env.gen_obs()['image'])
        # To be returned to the agent
        obs, reward, done, info = None, None, None, None
        self.propsed_action = proposed_action

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        # Store obs/action in history
        self.proposed_history.append((current_obs, proposed_action))

        # Check observation and proposed action in all running monitors
        for monitor in self.absence_monitors:
            monitor.check(current_obs, proposed_action)

        # Simply all shaped reward from all the monitors
        shaped_rewards = []
        unsafe_actions = []

        for name, monitor in self.monitor_states.items():
            if monitor["state"] == "violation":
                if self.config.on_violation == "reset":
                    obs = self.env.reset()
                    done = True
                    info = {}
                    shaped_rewards.append(monitor["shaped_reward"])
            else:
                if monitor["unsafe_action"]:
                    unsafe_actions.append(monitor["unsafe_action"])
                shaped_rewards.append(monitor["shaped_reward"])

        # If any violation occurred
        if done:
            reward = sum(shaped_rewards)
            return obs, reward, done, info

        # Build action to send to the environment and reward to send back to the agent
        suitable_action = self.action_planner(unsafe_actions)

        # Send it to the environment
        obs, reward, done, info = self.env.step(suitable_action)

        # Check for mismatch with the observations received from the environment in all the monitors
        for monitor in self.absence_monitors:
            monitor.verify(obs)

        # Shape the reward
        reward += sum(shaped_rewards)

        # Return everything to the agent
        return obs, reward, done, info
