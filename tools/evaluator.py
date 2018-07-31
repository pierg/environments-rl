import numpy as np

import torch

from configurations import config_grabber as cg

from tools import csv_logger

import os


class Evaluator:

    def __init__(self, number=0):
        # Getting configuration from file
        self.config = cg.Configuration.grab()

        while os.path.isfile(self.config.evaluation_directory_name + "/"
                             + self.config.config_name
                             + "_"
                             + str(number)
                             + ".csv"):
            number += 1
        config_file_path = os.path.abspath(__file__ + "/../../"
                                           + self.config.evaluation_directory_name + "/"
                                           + self.config.config_name
                                           + "_"
                                           + str(number)
                                           + ".csv")

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
                                  'N_goal_reached',
                                  'N_step_AVG',
                                  'N_death',
                                  'N_saved',
                                  'N_death_by_end',
                                  'Total_death',
                                  'N_Total_episodes',
                                  'N_break',
                                  'Info_saved'])

        # Evaluation variables
        # self.shortest_path = config.shortest_path

        self.episode_rewards = torch.zeros([self.config.num_processes, 1])
        self.final_rewards = torch.zeros([self.config.num_processes, 1])

        self.n_catastrophes = torch.zeros([self.config.num_processes, 1])
        self.n_episodes = torch.zeros([self.config.num_processes, 1])
        self.n_proccess_reached_goal = [0] * self.config.num_processes
        self.numberOfStepPerEpisode = [0] * self.config.num_processes
        self.numberOfStepAverage = 0
        self.N_goal_reached = 0
        self.N_death = 0
        self.N_violation = 0
        self.N_death_by_end = 0
        self.Total_death = 0
        self.N_saved = 0
        self.N_Total_episodes = 0
        self.N_break = 0
        self.dic_saved = {}
        self.Info_saved = ""

    def update(self, reward, done, info, numberOfStepPerEpisode):
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
        self.N_goal_reached = 0
        for i in range(0, len(info)):
            if len(info[i]) > 0:
                if info[i][0] == "died":
                    self.n_proccess_reached_goal[i] = 0
                    self.N_death += 1
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
                    self.N_death_by_end += 1
                    self.Total_death += 1
                    self.N_Total_episodes += 1
                elif info[i][0] == "saved":
                    self.N_saved += 1
                    for element in info[i][1].values():
                        if element in self.dic_saved:
                            self.dic_saved[element] = self.dic_saved[element] + 1
                        else:
                            self.dic_saved[element] = 1
                elif info[i][0] == "break":
                    self.N_break += 1
        for i in range(0, len(self.n_proccess_reached_goal)):
            self.N_goal_reached += self.n_proccess_reached_goal[i]
        self.n_episodes = n_episodes_mask
        self.Info_saved = ""
        for i in self.dic_saved:
            self.Info_saved += "{}_{}_".format(i, self.dic_saved[i])

    def get_reward_mean(self):
        return self.final_rewards.mean()

    def get_reward_median(self):
        return self.final_rewards.median()

    def save(self, n_updates, t_start, t_end, dist_entropy, value_loss, action_loss):
        total_num_steps = (n_updates + 1) * self.config.num_processes * self.config.num_steps
        csv_logger.write_to_log([n_updates,
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
                                 self.N_goal_reached,
                                 self.numberOfStepAverage,
                                 self.N_death,
                                 self.N_saved,
                                 self.N_death_by_end,
                                 self.Total_death,
                                 self.N_Total_episodes,
                                 self.N_break,
                                 self.Info_saved])
