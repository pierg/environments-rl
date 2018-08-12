from scipy import stats
import numpy as np
from pytorch_dqn.visualize import visdom_plot

from configurations import config_grabber as cg

from tools import csv_logger

import os

"""
All the values besides 'reward_cum' refer to the interval 
between one n_frame and the next one

"""
class Evaluator:

    def __init__(self, algorithm, iteration=0):
        # Getting configuration from file
        self.config = cg.Configuration.grab()

        if self.config.controller:
            file_name = self.config.evaluation_directory_name + "/dqn/" \
                        + "NO_" + str(algorithm) + "_epi_" \
                        + self.config.config_name \
                        + "_"
        else:
            file_name = self.config.evaluation_directory_name + "/dqn/" \
                        + "YES_" + str(algorithm) + "_epi_" \
                        + self.config.config_name \
                        + "_"


        while os.path.isfile(__file__ + "/../../"
                             + file_name
                             + str(iteration)
                             + ".csv"):
            iteration += 1

        self.config_file_path = os.path.abspath(__file__ + "/../../"
                                           + file_name
                                           + str(iteration)
                                           + ".csv")

        dirname = os.path.dirname(self.config_file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)


        csv_logger.create_header(self.config_file_path,
                                 ['episode_idx',
                                  'reward_mean',
                                  'reward_median',
                                  'reward_min',
                                  'reward_max',
                                  'reward_sem',
                                  'reward_cum',
                                  'losses_mean',
                                  'n_deaths',
                                  'n_goals',
                                  'n_violations',
                                  'last_epsilon',
                                  'n_steps_goal',
                                  'expected_q_value',
                                  'times_record',
                                  'cons_times_record'])

        self.episode_idx = []
        self.reward_cum_e = []
        self.reward_mean = []
        self.reward_median = []
        self.reward_min = []
        self.reward_max = []
        self.reward_sem = []
        self.losses_mean = []
        self.n_deaths = []
        self.n_goals = []
        self.n_violations = []
        self.last_epsilon = []
        self.n_steps_goal = []
        self.expected_q_value = []
        self.times_record = []
        self.cons_times_record = []

        self.last_saved_element_idx = 0

    def update(self, episode_idx, all_rewards, reward_cum_e, all_losses, n_deaths, n_goals, n_violations, 
               last_epsilon, n_steps_goal, expected_q_value, times_record, cons_times_record):

        self.episode_idx.append(episode_idx)
        self.reward_mean.append(np.mean(all_rewards))
        # if self.config.visdom:
            # visdom_plot("avg_rwd", self.episode_idx, "episode_idx", self.reward_mean, "reward_mean")
        self.reward_median.append(np.median(all_rewards))
        self.reward_min.append(np.min(all_rewards))
        self.reward_max.append(np.max(all_rewards))
        self.reward_sem.append(stats.sem(all_rewards))
        self.reward_cum_e.append(reward_cum_e)
        # if self.config.visdom:
        #     visdom_plot("cum_rwd_e", self.episode_idx, "episode_idx", self.reward_cum_e, "cum_reward")
        self.losses_mean.append(np.mean(all_losses))
        self.n_deaths.append(n_deaths)
        self.n_goals.append(n_goals)
        # if self.config.visdom:
            # visdom_plot("goal", self.episode_idx, "episode_idx", self.n_goals, "n_goals")
        self.n_violations.append(n_violations)
        self.last_epsilon.append(last_epsilon)
        # if self.config.visdom:
        #     visdom_plot("last_epsilon", self.episode_idx, "episode_idx", self.last_epsilon, "last_epsilon")
        self.n_steps_goal.append(n_steps_goal)
        if self.config.visdom:
            visdom_plot("steps_goal", self.episode_idx, "episode_idx", self.n_steps_goal, "steps_goal")

        self.expected_q_value.append(np.mean(expected_q_value))
        if self.config.visdom:
            visdom_plot("expected_q_value", self.episode_idx, "episode_idx", self.expected_q_value, "expected_q_value")

        self.times_record.append(times_record)
        self.cons_times_record.append(cons_times_record)


    def save(self):

        idx = self.last_saved_element_idx
        while idx < len(self.episode_idx):
            csv_logger.write_to_log(self.config_file_path, [self.episode_idx[idx],
                                     self.reward_mean[idx],
                                     self.reward_median[idx],
                                     self.reward_min[idx],
                                     self.reward_max[idx],
                                     self.reward_sem[idx],
                                     self.reward_cum_e[idx],
                                     self.losses_mean[idx],
                                     self.n_deaths[idx],
                                     self.n_goals[idx],
                                     self.n_violations[idx],
                                     self.last_epsilon[idx],
                                     self.n_steps_goal[idx],
                                     self.expected_q_value[idx],
                                     self.times_record[idx],
                                     self.cons_times_record[idx]])
            idx += 1
        self.last_saved_element_idx = idx
