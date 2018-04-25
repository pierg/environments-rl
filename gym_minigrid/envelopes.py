import collections
from perception import Perception

from helpers import config_grabber as cg

from extendedminigrid import *
from state_machines.patterns.absence import *

# Size of the history collection
N = 5

# Negative reward when trying to enter a catastrophic area
NEGATIVE_REWARD_CATASTROPHE = -2

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

        self.reset_on_catastrophe = self.config.reset_catastrofe

        # Grab configuration
        self.config = cg.Configuration.grab()

        # State of all the monitors after they have been checked
        self.monitor_states = {}

        self.shaped_reward = None
        self.unsafe_actions = []

        # Action shaped by the action planner
        self.shaped_action = None

        # List of automata-based monitors
        self.monitors = []

        # Generates automata-based monitors
        for cell_type in self.config.automata.absence:
            self.monitors.append(Absence("absence_" + cell_type, cell_type, self.on_monitoring))


    def on_monitoring(self, type, **kwargs):
        """
        Callback function called by the monitors
        :param type:
        :param kwargs:
        :return:
        """
        if type == "mismatch":
            print("Mismatch between state machine and observations!!!")

        if type=="violation":
            if kwargs:
                print("Violation Blocked!!!!")
                self.shaped_reward = kwargs.get('shaped_reward', 0)
                self.unsafe_actions.append(kwargs.get('unsafe_action'))
                print("shaped_reward=" + str(shaped_reward) + " unsafe_action=" + str(unsafe_action))
            else:
                print("ERROR. missing action and reward")


    def step(self, proposed_action, reset_on_catastrophe=False):
        # Get current observations from the environment and decode them
        current_obs = ExGrid.decode(self.env.gen_obs()['image'])

        if self.config.num_processes == 1 and self.config.rendering:
            self.env.render('human')

        # Store obs/action in history
        self.proposed_history.append((current_obs, proposed_action))

        # Check observation and proposed action in all running monitors
        for monitor in self.monitors:
            monitor.check(current_obs, proposed_action)

        if self.monitor_state == "violation":
            if self.config.on_catastrofe == "reset":
                obs = self.env.reset()
                reward = self.shaped_reward
                done = True
                info = {'violation': 1}
            elif self.config.on_catastrofe == "keep_going":
                safe_action = self.env.wait
                obs, reward, done, info = self.env.step(safe_action)
                reward = self.shaped_reward
                info = {'violation': 1}
            else:
                print(self.config.on_violation + " not implemented")
                raise NotImplementedError
        else:
            obs, reward, done, info = self.env.step(proposed_action)


        self.actual_history.append((current_obs, safe_action))

        # Apply the agent action to the environment or a safety action
        mod_reward = reward


        return obs, mod_reward, done, info

    def monitor(self, observation, proposed_action):
        """

        :param observation:
        :param proposed_action:
        :return:
        """
        # Block if the agent is in front of the water and want to go forward
        return Perception.is_ahead_of_worldobj(observation, Water, 1) \
               and proposed_action == MiniGridEnv.Actions.forward


