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

        if self.config.controller:
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

        config_file_path_episodes = os.path.abspath(__file__ + "/../../"
                                           + file_name
                                           + "_epi_"
                                           + str(number)
                                           + ".csv")

        self.config_file_path = config_file_path

        self.config_file_path_episodes = config_file_path_episodes

        dirname = os.path.dirname(config_file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Setup CSV logging
        csv_logger.create_header(config_file_path,
                                 ['N_updates',
                                  'N_timesteps',
                                  'FPS',
                                  'Reward_mean',
                                  'Reward_median',
                                  'Reward_min',
                                  'Reward_max',
                                  'Reward_std',
                                  'Entropy',
                                  'Value_loss',
                                  'Action_loss',
                                  'N_episodes',
                                  'N_blocked_actions',
                                  'N_violation',
                                  'N_goals',
                                  'N_step_AVG',
                                  'N_died',
                                  'N_died_by_end',
                                  'Total_death',
                                  'N_Total_episodes',
                                  'N_break'])

        # For each episode of each processor, store the mean values of...
        csv_logger.create_header(config_file_path_episodes,
                                 ['Episode_N',
                                  'Reward_mean',
                                  'Reward_median',
                                  'Reward_min',
                                  'Reward_max',
                                  'Reward_std',
                                  'N_violation_mean',
                                  'N_steps_goal_mean',
                                  'N_goal_mean',
                                  'N_died_mean',
                                  'N_end_mean'])


        self.episode_rewards = torch.zeros([self.config.a2c.num_processes, 1])
        self.final_rewards = torch.zeros([self.config.a2c.num_processes, 1])


        # Array of num_processes element, each element is a list. Each position is the episode index
        self.episodes_rewards = np.zeros([self.config.a2c.num_processes, 1]).tolist()


        self.n_catastrophes = torch.zeros([self.config.a2c.num_processes, 1])
        self.n_episodes = torch.zeros([self.config.a2c.num_processes, 1])
        self.n_proccess_reached_goal = [0] * self.config.a2c.num_processes
        self.numberOfStepPerEpisode = [0] * self.config.a2c.num_processes
        self.numberOfStepAverage = 0
        self.N_goals = 0
        self.N_died = 0
        self.N_violation = 0
        self.N_died_by_end = 0
        self.Total_death = 0
        self.N_Total_episodes = 0
        self.N_break = 0
        self.dic_saved = {}

        self.N_violation_mean = 0.0
        self.N_died_mean = 0.0
        self.N_end_mean = 0.0
        self.N_goals_mean = 0.0

    def update(self, reward, done, info):

        reward = torch.from_numpy(np.expand_dims(np.stack(reward), 1)).float()
        self.episode_rewards += reward

        # If done then clean the history of observations.
        masks = torch.FloatTensor([[0.0] if done_ else [1.0] for done_ in done])
        self.final_rewards *= masks
        self.final_rewards += (1 - masks) * self.episode_rewards
        """
        for i, done_ in enumerate(done):
            if done_:
                # Append to
                self.episodes_rewards[i].append(self.episode_rewards.data[i])
        """

        self.episode_rewards *= masks

        N_violation = 0
        N_died = 0
        N_died_by_end = 0
        N_goal_reached = 0

        for i in range(0, len(info)):
            if len(info[i]) > 0:
                if "died" in info[i]["event"]:
                    self.n_proccess_reached_goal[i] = 0
                    N_died += 1
                    self.N_Total_episodes += 1
                elif "goal" in info[i]["event"]:
                    N_goal_reached +=1
                    self.N_Total_episodes += 1
                elif "violation" in info[i]["event"]:
                    N_violation += 1
                    self.n_proccess_reached_goal[i] = 0
                elif "end" in info[i]["event"]:
                    self.n_proccess_reached_goal[i] = 0
                    N_died_by_end += 1
                    self.N_Total_episodes += 1

        if done[i]:
            self.numberOfStepPerEpisode[i] = info[i]["steps_count"]
            self.numberOfStepAverage = 0
            for j in range(0, len(self.numberOfStepPerEpisode)):
                self.numberOfStepAverage += self.numberOfStepPerEpisode[j]
            self.numberOfStepAverage /= len(self.numberOfStepPerEpisode)

        self.N_violation_mean += N_violation / len(info)
        self.N_died_mean += N_died / len(info)
        self.N_end_mean += N_died_by_end / len(info)
        self.N_goals_mean += N_goal_reached / len(info)

    def update_old(self, reward, done, info):
        reward = torch.from_numpy(np.expand_dims(np.stack(reward), 1)).float()
        self.episode_rewards += reward

        # If done then clean the history of observations.
        masks = torch.FloatTensor([[0.0] if done_ else [1.0] for done_ in done])
        self.final_rewards *= masks
        self.final_rewards += (1 - masks) * self.episode_rewards
        self.episode_rewards *= masks

        n_catastrophes_mask = torch.FloatTensor([[1.0] if "violation" in info_ else [0.0] for info_ in info])
        n_episodes_mask = torch.FloatTensor([[1.0] if done_ else [0.0] for done_ in done])
        for i in range(0, len(done)):
            if done[i]:
                self.n_episodes = self.n_episodes + 1
                self.numberOfStepPerEpisode[i] = numberOfStepPerEpisode[i]
                self.numberOfStepAverage = 0
                for j in range(0, len(self.numberOfStepPerEpisode)):
                    self.numberOfStepAverage += self.numberOfStepPerEpisode[j]
                self.numberOfStepAverage /= len(self.numberOfStepPerEpisode)

        self.n_catastrophes += n_catastrophes_mask
        self.N_goals = 0
        for i in range(0, len(info)):
            if len(info[i]) > 0:
                if info[i][0] == "died":
                    self.n_proccess_reached_goal[i] = 0
                    self.N_died += 1
                    self.Total_death += 1
                    self.N_Total_episodes += 1
                elif info[i][0] == "goal":
                    self.n_proccess_reached_goal[i] = 1
                    self.N_Total_episodes += 1
                elif info[i][0] == "violation":
                    self.N_violation += 1
                    self.n_proccess_reached_goal[i] = 0
                elif info[i][0] == "end":
                    self.n_proccess_reached_goal[i] = 0
                    self.N_died_by_end += 1
                    self.Total_death += 1
                    self.N_Total_episodes += 1
        for i in range(0, len(self.n_proccess_reached_goal)):
            self.N_goals += self.n_proccess_reached_goal[i]
        self.n_episodes = n_episodes_mask


    def get_reward_mean(self):
        return self.final_rewards.mean()

    def get_reward_median(self):
        return self.final_rewards.median()

    def save(self, n_updates, t_start, t_end):
        total_num_steps = (n_updates + 1) * self.config.a2c.num_processes * self.config.a2c.num_steps
        csv_logger.write_to_log(self.config_file_path_episodes,[self.N_Total_episodes,
                                 self.final_rewards.mean(),
                                 self.final_rewards.median(),
                                 self.final_rewards.min(),
                                 self.final_rewards.max(),
                                 self.final_rewards.std(),
                                 self.N_violation_mean,
                                 self.numberOfStepAverage,
                                 self.N_goals_mean,
                                 self.N_died_mean,
                                 self.N_end_mean])

    def save_old(self, n_updates, t_start, t_end, dist_entropy, value_loss, action_loss):
        total_num_steps = (n_updates + 1) * self.config.a2c.num_processes * self.config.a2c.num_steps
        csv_logger.write_to_log(self.config_file_path, [n_updates,
                                                        total_num_steps,
                                                        int(total_num_steps / t_end - t_start),
                                                        self.final_rewards.mean(),
                                                        self.final_rewards.median(),
                                                        self.final_rewards.min(),
                                                        self.final_rewards.max(),
                                                        self.final_rewards.std(),
                                                        dist_entropy.data[0],
                                                        value_loss.data[0],
                                                        action_loss.data[0],
                                                        self.n_episodes.sum(),
                                                        self.n_catastrophes.sum(),
                                                        self.N_violation,
                                                        self.N_goals,
                                                        self.numberOfStepAverage,
                                                        self.N_died,
                                                        self.N_died_by_end,
                                                        self.Total_death,
                                                        self.N_Total_episodes,
                                                        self.N_break])
