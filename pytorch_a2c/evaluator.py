import numpy as np

import torch

from configurations import config_grabber as cg

from torch.autograd import Variable

from tools import csv_logger

import os, re, os.path

class Evaluator:

    def __init__(self, evaluation_id):
        # Getting configuration from file
        self.config = cg.Configuration.grab()

        config_file_path = os.path.abspath(__file__ + "/../../"
                                           + self.config.evaluation_directory_name + "/"
                                           + evaluation_id + ".csv")


        self.config_file_path = config_file_path

        self.is_converging = False

        dirname = os.path.dirname(config_file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Setup CSV logging
        csv_logger.create_header(config_file_path,
                                 ['N_updates',
                                  'N_timesteps',
                                  'Reward_mean',
                                  'Reward_median',
                                  'Reward_min',
                                  'Reward_max',
                                  'Reward_std',
                                  'Entropy',
                                  'Value_loss',
                                  'Action_loss',
                                  'N_violation_avg',
                                  'N_goals_avg',
                                  'N_died_avg',
                                  'N_end_avg',
                                  'N_step_goal_avg',
                                  'env_name',
                                  'envelope'])


        """
        The following variables are resetted refer to one log_interval
        """
        self.log_n_goals = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_steps_goal = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_died = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_violations = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_end = np.zeros(self.config.a2c.num_processes, dtype=float)


        # Needed to check convergence
        self.log_n_goals_avg_prev = 0.0
        self.log_n_steps_goal_avg_prev = 0.0
        self.log_n_violations_avg_prev = 0.0
        self.final_rewards_medium_prev = 0.0
        self.value_loss_prev = 0.0

    def update(self, done, info):

        for i in range(0, len(info)):
            try:
                infoevent = info[i]
                if "violation" in infoevent["event"]:
                    self.log_n_violations[i] += 1

                if "died" in infoevent["event"]:
                    self.log_n_died[i] += 1

                if "end" in infoevent["event"]:
                    self.log_n_end[i] += 1

                if "goal" in infoevent["event"]:
                    self.log_n_goals[i] += 1
                    self.log_n_steps_goal[i] += infoevent["steps_count"]
            except TypeError as e:
                print("ERROR")
                print(str(e))



    def save(self, n_updates, total_num_steps, final_rewards, dist_entropy, value_loss, action_loss, env_name = None, envelope = None):

        log_n_goals_avg_curr = np.mean(self.log_n_goals)

        if np.count_nonzero(self.log_n_goals) > 0:
            log_n_steps_goal_avg_curr = np.sum(self.log_n_steps_goal)/np.sum(self.log_n_goals)
        else:
            log_n_steps_goal_avg_curr = -100

        log_n_died_avg = np.sum(self.log_n_died)

        log_n_violations_avg_curr = np.mean(self.log_n_violations)
        log_n_end = np.mean(self.log_n_end)

        mean_rwd_curr = final_rewards.mean()
        value_lss_curr = value_loss.data[0]

        final_rewards_std = final_rewards.std()


        csv_logger.write_to_log(self.config_file_path, [n_updates,
                                                        total_num_steps,
                                                        mean_rwd_curr,
                                                        final_rewards.median(),
                                                        final_rewards.min(),
                                                        final_rewards.max(),
                                                        final_rewards_std,
                                                        dist_entropy.data[0],
                                                        value_lss_curr,
                                                        action_loss.data[0],
                                                        log_n_violations_avg_curr,
                                                        log_n_goals_avg_curr,
                                                        log_n_died_avg,
                                                        log_n_end,
                                                        log_n_steps_goal_avg_curr,
                                                        env_name,
                                                        envelope
                                                        ])

        # Check convergence
        if (abs(log_n_steps_goal_avg_curr - self.log_n_steps_goal_avg_prev) < 0.1
                and value_lss_curr < 0.01
                and mean_rwd_curr > 0.0
                and log_n_goals_avg_curr > 0.0
                and final_rewards_std < 0.001):
            self.is_converging = True

        self.log_n_goals_avg_prev = log_n_goals_avg_curr
        self.log_n_steps_goal_avg_prev = log_n_steps_goal_avg_curr
        self.log_n_violations_avg_prev = log_n_violations_avg_curr
        self.final_rewards_medium_prev = mean_rwd_curr
        self.value_loss_prev = value_lss_curr

        # Resetting all the variables until next logging interval
        self.log_n_goals = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_steps_goal = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_died = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_violations = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_n_end = np.zeros(self.config.a2c.num_processes, dtype=float)

