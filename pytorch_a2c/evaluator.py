import numpy as np

import torch

from configurations import config_grabber as cg

from torch.autograd import Variable

from tools import csv_logger

import os, re, os.path

class Evaluator:

    def __init__(self, algorithm, number=0):
        # Getting configuration from file
        self.config = cg.Configuration.grab()

        if self.config.envelope:
            file_name = self.config.evaluation_directory_name + "/a2c/" \
                        + "YES_" + str(algorithm) + "_" \
                        + self.config.config_name \
                        + "_"
        else:
            file_name = self.config.evaluation_directory_name + "/a2c/" \
                        + "NO_" + str(algorithm) + "_" \
                        + self.config.config_name \
                        + "_"


        while os.path.isfile(__file__ + "/../../"
                             + file_name
                             + str(number)
                             + ".csv"):
            number += 1


        config_file_path = os.path.abspath(__file__ + "/../../"
                                           + file_name
                                           + "_"
                                           + str(number)
                                           + ".csv")


        self.config_file_path = config_file_path

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
        self.log_N_goals = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_steps_goal = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_died = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_violations = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_end = np.zeros(self.config.a2c.num_processes, dtype=float)


    def update(self, done, info):

        for i in range(0, len(info)):
            try:
                infoevent = info[i]
                if "violation" in infoevent["event"]:
                    self.log_N_violations[i] += 1

                if "died" in infoevent["event"]:
                    self.log_N_died[i] += 1

                if "end" in infoevent["event"]:
                    self.log_N_end[i] += 1

                if "goal" in infoevent["event"]:
                    self.log_N_goals[i] += 1
                    self.log_N_steps_goal[i] += infoevent["steps_count"]
            except TypeError as e:
                print("ERROR")
                print(str(e))


    def save(self, n_updates, total_num_steps, final_rewards, dist_entropy, value_loss, action_loss, env_name = None, envelope = None):

        log_N_goals_avg = np.mean(self.log_N_goals)
        if np.count_nonzero(self.log_N_goals) > 0:
            log_N_steps_goal_avg = np.sum(self.log_N_steps_goal)/np.sum(self.log_N_goals)
        else:
            log_N_steps_goal_avg = -100
        log_N_died_avg = np.mean(self.log_N_died)
        log_N_violations_avg = np.mean(self.log_N_violations)
        log_N_end = np.mean(self.log_N_end)


        csv_logger.write_to_log(self.config_file_path, [n_updates,
                                                        total_num_steps,
                                                        final_rewards.mean(),
                                                        final_rewards.median(),
                                                        final_rewards.min(),
                                                        final_rewards.max(),
                                                        final_rewards.std(),
                                                        dist_entropy.data[0],
                                                        value_loss.data[0],
                                                        action_loss.data[0],
                                                        log_N_violations_avg,
                                                        log_N_goals_avg,
                                                        log_N_died_avg,
                                                        log_N_end,
                                                        log_N_steps_goal_avg,
                                                        env_name,
                                                        envelope
                                                        ])

        # Resetting all the variables until next logging interval
        self.log_N_goals = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_steps_goal = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_died = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_violations = np.zeros(self.config.a2c.num_processes, dtype=float)
        self.log_N_end = np.zeros(self.config.a2c.num_processes, dtype=float)

