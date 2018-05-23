import collections

from configurations import config_grabber as cg

from .action_planning import *
from gym_minigrid.extendedminigrid import *
from gym_minigrid.monitors.patterns.absence import *
from gym_minigrid.monitors.patterns.precedence import *

import gym

# Size of the history collection
N = 5


# class SafetyEnvelope(gym.core.Wrapper):
#     """
#     Safety envelope for safe exploration.
#     The purpose is to detect dangerous actions and block them sending back a modified reward
#     """
#
#     def __init__(self, env):
#         super(SafetyEnvelope, self).__init__(env)
#         # Stores history of the last N observation / proposed_actions
#         self.proposed_history = collections.deque(N*[(None, None)], N)
#         # Stores history of the last N observation / applied_actions
#         self.actual_history = collections.deque(N * [(None, None)], N)
#
#         # Grab configuration
#         self.config = cg.Configuration.grab()
#
#         # Action shaped by the action planner
#         self.shaped_action = None
#
#         self.propsed_action = None
#
#         # List of absence-based monitors with their states, rewards and unsafe-actions
#         self.absence_monitors = []
#
#         # List of precedence-based monitors with their stats, rewards and unsafe-actions
#         self.precedence_monitors = []
#
#         # Dictionary that gets populated with information by all the monitors at runtime
#         self.monitor_states = {}
#
#         # Set reward for a normal step
#         self.normal_reward = self.config.reward.step
#
#         # Set reward for the goal
#         self.goal_reward = self.config.reward.goal
#
#         self.death_reward = self.config.reward.death
#
#         self.step_number = 0
#
#         # Generates absence-based monitors
#         if hasattr(self.config.monitors, 'absence'):
#             for avoid_obj in self.config.monitors.absence.monitored:
#                 if avoid_obj.active:
#                     new_absence_monitor = Absence("absence_" + avoid_obj.name, avoid_obj.name, self.on_monitoring,avoid_obj.reward)
#                     self.absence_monitors.append(new_absence_monitor)
#                     self.monitor_states[new_absence_monitor.name] = {}
#                     self.monitor_states[new_absence_monitor.name]["state"] = ""
#                     self.monitor_states[new_absence_monitor.name]["shaped_reward"] = 0
#                     self.monitor_states[new_absence_monitor.name]["unsafe_action"] = ""
#
#         # Generates precedence-based monitors
#         if hasattr(self.config.monitors, 'precedence'):
#             for precedence_obj in self.config.monitors.precedence.monitored:
#                 if precedence_obj.active:
#                     new_precedence_monitor = Precedence("precedence_"+precedence_obj.name,precedence_obj,self.on_monitoring,precedence_obj.reward)
#                     self.precedence_monitors.append(new_precedence_monitor)
#                     self.monitor_states[new_precedence_monitor.name] = {}
#                     self.monitor_states[new_precedence_monitor.name]["state"] = ""
#                     self.monitor_states[new_precedence_monitor.name]["shaped_reward"] = 0
#                     self.monitor_states[new_precedence_monitor.name]["unsafe_action"] = ""
#
#     def on_monitoring(self, name, state, **kwargs):
#         """
#         Callback function called by the monitors
#         :param state: mismatch, violation
#         :param kwargs: in case of violation it returns a reward and the action causing the violation (unsafe_aciton)
#         :return: None
#         """
#         self.monitor_states[name]["state"] = state
#
#         if state == "mismatch":
#             logging.warning("%s mismatch!!!!",name)
#
#         if state == "monitoring":
#             logging.info("%s monitoring",name)
#
#         if state == "shaping":
#             if kwargs:
#                 logging.info("%s shaping",name)
#                 shaped_reward = kwargs.get('shaped_reward', 0)
#                 logging.info("     shaped_reward = %s" , str(shaped_reward))
#                 self.monitor_states[name]["shaped_reward"] = shaped_reward
#             else:
#                 logging.warning("%s ERROR. missing action and reward",name)
#
#         if state== "violation":
#             if kwargs:
#                 logging.warning("%s violation blocked",name)
#                 unsafe_action = kwargs.get('unsafe_action')
#                 shaped_reward = kwargs.get('shaped_reward', 0)
#                 self.monitor_states[name]["unsafe_action"] = unsafe_action
#                 self.monitor_states[name]["shaped_reward"] = shaped_reward
#                 logging.info("shaped_reward=%s unsafe_action=%s",str(shaped_reward),str(unsafe_action))
#             else:
#                 logging.warning("%s ERROR. missing action and reward",name)
#
#     def action_planner(self, unsafe_actions):
#         """
#         Return a suitable action that (that is not one of the 'unsafe_action')
#         :param unsafe_actions:
#         :return: safe action or proposed action
#         """
#         if len(unsafe_actions) == 0:
#             return self.propsed_action
#         else:
#             logging.info("safe action : %s",str(self.env.actions.wait))
#             return self.env.actions.wait
#
#     def resetMonitors(self):
#         for monitor in self.absence_monitors:
#             monitor.initial_state = None
#         for monitor in self.precedence_monitors:
#             monitor.initial_state = None
#
#     def step(self, proposed_action, reset_on_catastrophe=False):
#         # To be returned to the agent
#         obs, reward, done, info = None, None, None, None
#         end = False
#         if self.step_number == 0:
#             self.resetMonitors()
#
#         self.step_number += 1
#
#         if self.step_number == self.env.max_steps:
#             end = True
#             self.step_number = 0
#
#         self.propsed_action = proposed_action
#
#         # Get current observations from the environment and decode them
#         agent_obs = ExGrid.decode(self.env.gen_obs()['image'])
#         agent_pos = self.env.agent_pos
#         agent_dir = self.env.get_dir_vec()
#         current_obs = (agent_obs, agent_pos, agent_dir)
#
#         current_obs_env = self.env
#         if self.config.num_processes == 1 and self.config.rendering:
#             self.env.render('human')
#
#         # Store obs/action in history
#         self.proposed_history.append((current_obs, proposed_action))
#
#         logging.info("___check BEFORE action is applyed to the environmnent")
#         # Check observation and proposed action in all running monitors
#         for monitor in self.absence_monitors:
#             monitor.check(current_obs_env, proposed_action)
#
#         for monitor in self.precedence_monitors:
#             monitor.check(current_obs_env, proposed_action)
#
#
#         # Check for unsafe actions before sending them to the environment:
#         unsafe_actions = []
#         shaped_rewards = []
#         for name, monitor in self.monitor_states.items():
#             if monitor["state"] == "violation":
#                 if self.config.on_violation_reset:
#                     obs = self.env.reset()
#                     done = True
#                     info = "violation"
#                 if monitor["unsafe_action"]:
#                     unsafe_actions.append(monitor["unsafe_action"])
#                 shaped_rewards.append(monitor["shaped_reward"])
#
#         # If have to reset
#         if done:
#             reward = sum(shaped_rewards)
#             self.step_number = 0
#             return obs, reward, done, info
#
#         logging.info("unsafe actions = %s",unsafe_actions)
#
#         # Build action to send to the environment
#         suitable_action = self.action_planner(unsafe_actions)
#         logging.info("actions possibles =%s",suitable_action)
#
#         # Send a suitable action to the environment
#         obs, reward, done, info = self.env.step(suitable_action)
#         logging.info("____verify AFTER action is applied to the environment")
#         # Notify the monitors of the new state reached in the environment and the applied action
#         for monitor in self.absence_monitors:
#             monitor.verify(self.env, suitable_action)
#
#         for monitor in self.precedence_monitors:
#             monitor.verify(self.env, suitable_action)
#
#         # Get the shaped rewards from the monitors in the new state
#         shaped_rewards = []
#         for name, monitor in self.monitor_states.items():
#             shaped_rewards.append(monitor["shaped_reward"])
#
#         # Shape the reward at the cumulative sum of all the rewards from the monitors
#         reward += sum(shaped_rewards)
#
#         # Reset monitor rewards and actions
#         for name, monitor in self.monitor_states.items():
#             monitor["shaped_reward"] = 0
#             monitor["unsafe_action"] = ""
#
#         # Check if goal reached, if yes add goal_reward
#         a,b = ExMiniGridEnv.get_grid_coords_from_view(self.env,(0,0))
#         current_cell = Grid.get(self.env.grid,a,b)
#         if current_cell is not None:
#             if current_cell.type == "goal":
#                 reward = self.goal_reward
#                 info = "goal"
#                 self.step_number = 0
#
#         # Check if normal step, if yes add normal_reward
#         if reward == 0:
#             reward = self.normal_reward
#
#         if end:
#             info = "end"
#
#         # Return everything to the agent
#         return obs, reward, done, info

#######################################################################################


class ActionPlannerEnvelope(gym.core.Wrapper):
    """
    Action Planner Envelope
    Decides what actions to take after a safety hazard has been detected
    """

    def __init__(self, env):
        super(ActionPlannerEnvelope, self).__init__(env)

        # List of actions generated by action planner
        self.action_plan = []

        self.critical_actions = []

        self.config = cg.Configuration.grab()

        self.reward_range = (-100, 100)

        self.proposed_history = collections.deque(N * [(None, None)], N)
        self.actual_history = collections.deque(N * [(None, None)], N)

    def step(self, action):

        if self.config.action_planner:

            # proceed with the step
            obs, reward, done, info = self.env.step(action)

            # check if critical action
            if action in self.critical_actions:
                self.critical_actions = []
                return obs, -100, True, info

            # check if following the plan
            reward = self.check_plan(action)

            # observations
            obs = self.env.gen_obs()
            current_obs = ExGrid.decode(obs['image'])
            current_dir = obs['direction']

            if self.config.num_processes == 1 and self.config.rendering:
                self.env.render('human')

            # do we need this?
            # self.proposed_history.append((current_obs, action))

            if ExMiniGridEnv.worldobj_in_front_agent(self.env) == 'unsafe':
                self.action_plan = run(current_obs, current_dir, goal_safe_zone)
                self.critical_actions = [ExMiniGridEnv.Actions.forward]
                # self.critical_actions = [
                #     ExMiniGridEnv.Actions.forward,
                #     ExMiniGridEnv.Actions.pickup,
                #     ExMiniGridEnv.Actions.toggle
                # ]
                # print(self.action_plan)

            # Check if goal reached, if yes add goal_reward
            a, b = ExMiniGridEnv.get_grid_coords_from_view(self.env, (0, 0))
            current_cell = Grid.get(self.env.grid, a, b)
            if current_cell is not None:
                if current_cell.type == "goal":
                    reward = 100
                    info = "goal"
                elif current_cell.type == "unsafe":
                    reward = -100
                    info = "unsafe"
                    done = True

            self.critical_actions = []
            # print(reward)
            return obs, reward, done, info

        else:

            obs, reward, done, info = self.env.step(action)
            return obs, reward, done, info

    #################################################

    def check_plan(self, action):
        if len(self.action_plan):
            if self.action_plan.pop() != action:
                self.action_plan = []
                return -50
            else:
                return 50
        else:
            return -1
