from configurations import config_grabber as cg

from .action_planning_goap import *
from gym_minigrid.extendedminigrid import *
from gym_minigrid.minigrid import Goal
from gym_minigrid.monitors.patterns.response import *

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

        self.goap = self.config.action_planning.active
        if self.goap:

            # ---------------------- ACTION PLANNER START ----------------------#
            # List of actions generated by action planner
            self.action_plan = []

            self.action_plan_size = 0

            self.plan_tracker = 0

            self.counts = {}

            # List of unsafe actions an agent might do at current step. Will reset when step is finished
            self.critical_actions = []

            self.step_number = 0

            self.actions = ExMiniGridEnv.Actions

            self.action_space = spaces.Discrete(len(self.actions))

            self.last_cell = {0: (0, 0), 1: (0, 0), 2: (0, 1)}

            self.goal_cell = None

            self.secondary_goals = []

            for goal in self.config.action_planning.secondary_goals:
                if goal == 'goal_safe_zone':
                    self.secondary_goals.append(goal_safe_zone)
                elif goal == 'goal_turn_around':
                    self.secondary_goals.append(goal_turn_around)
                elif goal == 'goal_safe_east':
                    self.secondary_goals.append(goal_safe_east)
                elif goal == 'goal_clear_west':
                    self.secondary_goals.append(goal_clear_west)

            self.secondary_goals = tuple(self.secondary_goals)

    def step(self, action):

        # To be returned to the agent
        obs, reward, done, info = None, None, None, None

        # ---------------------- ACTION PLANNER START ----------------------#
        if self.goap:
            if self.config.num_processes == 1 and self.config.rendering:
                self.env.render('human')

            # proceed with the step
            obs, reward, done, info = self.env.step(action)

            if self.step_number == 0:
                self.reset_planner()

            self.step_number += 1
            reward = self.config.action_planning.reward.step

            # check if episode is finished
            if self.step_number == self.env.max_steps:
                info = "end"
                done = True
                self.step_number = 0
                return obs, reward, done, info

            # observations
            obs = self.env.gen_obs()
            current_obs = ExGrid.decode(obs['image'])
            current_dir = obs['direction']

            ##### PLANNER START

            if self.config.action_planning.active:

                # check if following the plan
                reward, info = self.check_plan(action, info)

                # activate planner
                # if ExMiniGridEnv.worldobj_in_front_agent(self.env) == 'unsafe':
                for obj in current_obs.grid:
                    if isinstance(obj, Goal):
                        if (self.goal_cell is not None and goal_green_square[0] not in self.goal_cell[0]) or\
                                not self.action_plan:
                            self.action_plan, self.goal_cell = run(current_obs, current_dir, (goal_green_square,))
                            self.action_plan_size = len(self.action_plan)
                            self.critical_actions = [ExMiniGridEnv.Actions.forward]
                            info = "plan_created"
                            # print(self.action_plan)
                            break

                if not self.action_plan and self.secondary_goals:
                        self.action_plan, self.goal_cell = run(current_obs, current_dir, self.secondary_goals)
                        self.action_plan_size = len(self.action_plan)

                self.critical_actions = []

            ##### PLANNER END

            if len(self.action_plan) == 0 and action == ExMiniGridEnv.Actions.forward:
                reward = reward + 2
            if ExMiniGridEnv.worldobj_in_agent(self.env, 1, 0) == 'wall' and action == ExMiniGridEnv.Actions.forward:
                reward = reward - 5

            a, b = ExMiniGridEnv.get_grid_coords_from_view(self.env, (0, 0))

            # if self.last_cell == (a, b):
            # Stay in the same cell
            #     reward = reward - 2
            # self.last_cell = (a, b)

            if self.last_cell[0] == (a, b) and self.last_cell[1] == (a, b) and self.last_cell[2] == (a, b):
                return obs, self.config.action_planning.reward.unsafe, done, info
            current_cell = Grid.get(self.env.grid, a, b)
            self.last_cell[self.step_number % 3] = (a, b)

            # Try

            if current_cell is not None:
                if current_cell.type == "goal":
                    done = True
                    if info == "plan_finished":
                        reward = self.config.action_planning.reward.goal
                        info = "goal+plan_finished+end"
                    else:
                        reward = self.config.action_planning.reward.goal
                        info = "goal+end"
                elif current_cell.type == "unsafe":
                    reward = self.config.action_planning.reward.unsafe
                    info = "violation"

            if done:
                self.step_number = 0
                return obs, reward, done, info

            # #  STIMULUS for exploration
            env = self.unwrapped
            tup = ((int(env.agent_pos[0]), int(env.agent_pos[1])), env.agent_dir, action)

            # Get the count for this key
            preCnt = 0
            if tup in self.counts:
                preCnt = self.counts[tup]

            # Update the count for this key
            newCnt = preCnt + 1
            self.counts[tup] = newCnt

            if reward == self.config.action_planning.reward.step:
                bonus = 1 / math.sqrt(newCnt)
                reward += bonus

            return obs, reward, done, info
        # ---------------------- ACTION PLANNER END ----------------------#


    # GOAP Helpers

    def check_plan(self, action, info):
        if len(self.action_plan):
            next_action_in_plan = self.action_plan.pop()
            if next_action_in_plan != action:
                if self.plan_tracker > 0:
                    info = "plan_followed:" + str(self.plan_tracker) + "," + str(self.action_plan_size)
                    # print("plan_followed: " + str(self.plan_tracker) + " " + str(self.action_plan_size))
                multiplier = 0
                i = self.plan_tracker

                while i > 0:
                    multiplier = multiplier + (self.config.action_planning.reward.off_plan * i)
                    i -= 1
                self.reset_planner()
                return multiplier, info
            else:
                self.plan_tracker += 1
                # print("plan_tracker: " + str(self.plan_tracker))
                if self.plan_tracker == self.action_plan_size:
                    self.reset_planner()
                    #print("plan_finished 2")
                    return self.config.action_planning.reward.on_plan, "plan_finished"
                else:
                    return self.config.action_planning.reward.on_plan * self.plan_tracker, info
        else:
            return self.config.action_planning.reward.step, info

    def reset_planner(self):
        self.action_plan = []
        self.action_plan_size = 0
        self.plan_tracker = 0

