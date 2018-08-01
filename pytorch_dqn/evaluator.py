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

        file_name = self.config.evaluation_directory_name + "/" \
                + str(algorithm) + "_" \
                + self.config.config_name \
                + "_"

        while os.path.isfile(__file__ + "/../../"
                             + file_name
                             + str(iteration)
                             + ".csv"):
            iteration += 1

        config_file_path = os.path.abspath(__file__ + "/../../"
                                           + file_name
                                           + str(iteration)
                                           + ".csv")

        dirname = os.path.dirname(config_file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)


        csv_logger.create_header(config_file_path,
                                 ['n_frames',
                                  'reward_mean',
                                  'reward_median',
                                  'reward_min',
                                  'reward_max',
                                  'reward_sem',
                                  'reward_cum',
                                  'losses_mean',
                                  'n_episodes',
                                  'n_deaths',
                                  'n_goals',
                                  'n_violations'])

        self.n_frames = []
        self.reward_mean = []
        self.reward_median = []
        self.reward_min = []
        self.reward_max = []
        self.reward_sem = []
        self.reward_cum = []
        self.losses_mean = []
        self.n_episodes = []
        self.n_deaths = []
        self.n_goals = []
        self.n_violations = []

        self.last_saved_element_idx = 0

    def update(self, frame_idx, all_rewards, cum_reward, all_losses, n_episodes, n_deaths, n_goals, n_violations):
        self.n_frames.append(frame_idx)
        self.reward_mean.append(np.mean(all_rewards))
        self.reward_median.append(np.median(all_rewards))
        self.reward_min.append(np.min(all_rewards))
        self.reward_max.append(np.max(all_rewards))
        self.reward_sem.append(stats.sem(all_rewards))
        self.reward_cum.append(cum_reward)
        if self.config.visdom:
            visdom_plot("cum_rwd", self.n_frames, "n_frames", self.reward_cum, "cum_reward")
        self.losses_mean.append(np.mean(all_losses))
        self.n_episodes.append(n_episodes)
        self.n_deaths.append(n_deaths)
        self.n_goals.append(n_goals)
        if self.config.visdom:
            visdom_plot("goal", self.n_frames, "n_frames", self.n_goals, "n_goals")
        self.n_violations.append(n_violations)


    def save(self):

        idx = self.last_saved_element_idx
        while idx < len(self.n_frames):
            csv_logger.write_to_log([self.n_frames[idx],
                                     self.reward_mean[idx],
                                     self.reward_median[idx],
                                     self.reward_min[idx],
                                     self.reward_max[idx],
                                     self.reward_sem[idx],
                                     self.reward_cum[idx],
                                     self.losses_mean[idx],
                                     self.n_episodes[idx],
                                     self.n_deaths[idx],
                                     self.n_goals[idx],
                                     self.n_violations[idx]])
            idx += 1
        self.last_saved_element_idx = idx
