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
                                  'N_violation_avg',
                                  'N_goals_avg',
                                  'N_died_avg',
                                  'N_end_avg',
                                  'N_step_goal_avg',
                                  'env_name',
                                  'controller'])


        self.epi_rewards = torch.zeros([self.config.a2c.num_processes, 1])
        self.fin_rewards = torch.zeros([self.config.a2c.num_processes, 1])

        self.log_N_goals = torch.zeros([self.config.a2c.num_processes, 1])

        self.log_N_died = torch.zeros([self.config.a2c.num_processes, 1])

        self.log_N_violations = torch.zeros([self.config.a2c.num_processes, 1])

        self.log_N_end = torch.zeros([self.config.a2c.num_processes, 1])

        self.log_N_steps_goal = torch.zeros([self.config.a2c.num_processes, 1])




    def update(self, reward, done, info):

        reward = torch.from_numpy(np.expand_dims(np.stack(reward), 1)).float()
        self.epi_rewards += reward
        masks = torch.FloatTensor([[0.0] if done_ else [1.0] for done_ in done])
        self.fin_rewards *= masks
        self.fin_rewards += (1 - masks) * self.epi_rewards
        self.epi_rewards *= masks


        for i in range(0, len(info)):
            if len(info[i]) > 0:
                if "violation" in info[i]["event"]:
                    self.N_violation += info[i]["event"].count("violation")
                if "died" in info[i]["event"]:
                    self.n_proccess_reached_goal[i] = 0
                    self.N_died += 1
                elif "end" in info[i]["event"]:
                    self.n_proccess_reached_goal[i] = 0
                    self.N_died_by_end += 1
                elif "goal" in info[i]["event"]:
                    goals = torch.from_numpy(np.expand_dims(np.stack(info["g"]), 1)).float()
                    self.epi_N_goals += reward
                    masks = torch.FloatTensor([[0.0] if done_ else [1.0] for done_ in done])
                    self.log_N_goals *= masks
                    self.log_N_goals += (1 - masks) * self.epi_N_goals
                    self.epi_N_goals *= masks


        goals = torch.from_numpy(np.expand_dims(np.stack(info[""]), 1)).float()
        self.epi_N_goals += reward
        masks = torch.FloatTensor([[0.0] if done_ else [1.0] for done_ in done])
        self.log_N_goals *= masks
        self.log_N_goals += (1 - masks) * self.epi_N_goals
        self.epi_N_goals *= masks

        steps_to_goals = torch.from_numpy(np.expand_dims(np.stack(reward), 1)).float()
        self.epi_N_steps_goal += reward
        masks = torch.FloatTensor([[0.0] if done_ else [1.0] for done_ in done])
        self.log_N_steps_goal *= masks
        self.log_N_steps_goal += (1 - masks) * self.epi_N_steps_goal
        self.epi_N_steps_goal *= masks

        #if an episode is done: incremente the number of total episode and send the step average of the episode
        for i in range(0, len(done)):
            if done[i]:
                self.n_episodes = self.n_episodes + 1
                self.numberOfStepPerEpisode[i] = info[i]["steps_count"]
                self.numberOfStepAverage = 0
                for j in range(0, len(self.numberOfStepPerEpisode)):
                    self.numberOfStepAverage += self.numberOfStepPerEpisode[j]
                self.numberOfStepAverage /= len(self.numberOfStepPerEpisode)

                self.N_Total_episodes += 1

        # check all the info
        for i in range(0, len(info)):
            if len(info[i]) > 0:
                if "violation" in info[i]["event"]:
                    self.N_violation += info[i]["event"].count("violation")
                if "died" in info[i]["event"]:
                    self.n_proccess_reached_goal[i] = 0
                    self.N_died += 1
                elif "end" in info[i]["event"]:
                    self.n_proccess_reached_goal[i] = 0
                    self.N_died_by_end += 1
                elif "goal" in info[i]["event"]:
                    self.N_goals +=1



    def get_reward_mean(self):
        return self.fin_rewards.mean()

    def get_reward_median(self):
        return self.fin_rewards.median()


    def save(self, n_updates, t_start, t_end, dist_entropy, value_loss, action_loss, env_name = None, controller = None):
        total_num_steps = (n_updates + 1) * self.config.a2c.num_processes * self.config.a2c.num_steps
        csv_logger.write_to_log(self.config_file_path, [n_updates,
                                                        total_num_steps,
                                                        int(total_num_steps / t_end - t_start),
                                                        self.fin_rewards.mean(),
                                                        self.fin_rewards.median(),
                                                        self.fin_rewards.min(),
                                                        self.fin_rewards.max(),
                                                        self.fin_rewards.std(),
                                                        dist_entropy.data[0],
                                                        value_loss.data[0],
                                                        action_loss.data[0],
                                                        self.N_violation / self.N_process,
                                                        self.N_goals / self.N_process,
                                                        self.N_died / self.N_process,
                                                        self.N_died_by_end / self.N_process,
                                                        self.numberOfStepAverage,
                                                        env_name,
                                                        controller
                                                        ])
