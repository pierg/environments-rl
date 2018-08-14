import copy
import glob
import os
import time
import operator
from functools import reduce

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable

from tools.arguments import get_args
from evaluator import Evaluator
from vec_env.dummy_vec_env import DummyVecEnv
from vec_env.subproc_vec_env import SubprocVecEnv
from kfac import KFACOptimizer
from model import Policy
from storage import RolloutStorage
from tools.visualize import visdom_plot

from shutil import copyfile

from configurations import config_grabber as cg

from envs import make_env

# from enjoy import record

import os, re, os.path

import sys
sys.stdout = open("../evaluations/a2c/LOG.txt", "w")
print ("test sys.stdout")

args = get_args()

cg.Configuration.set("training_mode", True)
cg.Configuration.set("debug_mode", False)

if args.stop:
    cg.Configuration.set("max_num_frames", args.stop)

if args.norender:
    cg.Configuration.set("rendering", False)
    cg.Configuration.set("visdom", False)

if args.record:
    cg.Configuration.set("recording", True)

if args.nomonitor:
    cg.Configuration.set("controller", False)
else:
    cg.Configuration.set("controller", True)


# Getting configuration from file
config = cg.Configuration.grab()

eval_folder = os.path.abspath(os.path.dirname(__file__) + "/../" + config.evaluation_directory_name)

# Copy config file to evaluation folder
copyfile(cg.Configuration.file_path(), eval_folder + "/configuration_a2c.txt")


def main():

    num_updates = int(config.max_num_frames) // config.a2c.num_steps // config.a2c.num_processes

    print("num_updates:     " + str(num_updates))

    print("stop_learning:   " + str(config.a2c.stop_learning))

    stop_after_update_number = config.a2c.stop_after_update_number

    # steps reward:
    if hasattr(config.a2c, "optimal_num_steps"):
        steps_reward = config.rewards.standard.step * config.a2c.optimal_num_steps
    else:
        steps_reward = 72 * config.rewards.standard.step

    # Initializing evaluation
    evaluator = Evaluator("a2c")

    os.environ['OMP_NUM_THREADS'] = '1'

    envs = [make_env(config.env_name, args.seed, i) for i in range(config.a2c.num_processes)]

    if config.a2c.num_processes > 1:
        envs = SubprocVecEnv(envs)
    else:
        envs = DummyVecEnv(envs)

    obs_shape = envs.observation_space.shape
    obs_shape = (obs_shape[0] * args.num_stack, *obs_shape[1:])
    obs_numel = reduce(operator.mul, obs_shape, 1)

    actor_critic = Policy(obs_numel, envs.action_space)

    # Maxime: log some info about the model and its size
    modelSize = 0
    for p in actor_critic.parameters():
        pSize = reduce(operator.mul, p.size(), 1)
        modelSize += pSize
    print(str(actor_critic))
    print('Total model size: %d' % modelSize)

    if envs.action_space.__class__.__name__ == "Discrete":
        action_shape = 1
    else:
        action_shape = envs.action_space.shape[0]

    if args.cuda:
        actor_critic.cuda()

    if config.a2c.algorithm == 'a2c':
        optimizer = optim.RMSprop(actor_critic.parameters(), args.lr, eps=args.eps, alpha=args.alpha)
    elif config.a2c.algorithm == 'ppo':
        optimizer = optim.Adam(actor_critic.parameters(), args.lr, eps=args.eps)
    elif config.a2c.algorithm == 'acktr':
        optimizer = KFACOptimizer(actor_critic)

    rollouts = RolloutStorage(config.a2c.num_steps, config.a2c.num_processes, obs_shape, envs.action_space, actor_critic.state_size)
    current_obs = torch.zeros(config.a2c.num_processes, *obs_shape)

    def update_current_obs(obs):
        shape_dim0 = envs.observation_space.shape[0]
        obs = torch.from_numpy(obs).float()
        if args.num_stack > 1:
            current_obs[:, :-shape_dim0] = current_obs[:, shape_dim0:]
        current_obs[:, -shape_dim0:] = obs

    obs = envs.reset()
    update_current_obs(obs)
    rollouts.observations[0].copy_(current_obs)
    numberOfStepBeforeDone = []
    stepOnLastGoal = []
    for i in range(0, config.a2c.num_processes):
        numberOfStepBeforeDone.append(0)
        stepOnLastGoal.append(0)
    # These variables are used to compute average rewards for all processes.
    episode_rewards = torch.zeros([config.a2c.num_processes, 1])
    final_rewards = torch.zeros([config.a2c.num_processes, 1])
    last_reward_mean = 0
    current_reward_mean = 0
    identical_rewards = 0
    first_time = True
    if args.cuda:
        current_obs = current_obs.cuda()
        rollouts.cuda()
    start = time.time()
    for j in range(num_updates):
        if identical_rewards == config.a2c.stop_learning and last_reward_mean >= (config.rewards.standard.goal + steps_reward):
            print("stop learning")
            break
        for step in range(config.a2c.num_steps):
            # Sample actions
            value, action, action_log_prob, states = actor_critic.act(
                Variable(rollouts.observations[step], volatile=True),
                Variable(rollouts.states[step], volatile=True),
                Variable(rollouts.masks[step], volatile=True)
            )
            cpu_actions = action.data.squeeze(1).cpu().numpy()

            # Obser reward and next obs
            obs, reward, done, info = envs.step(cpu_actions)

            # anydone = False

            for x in range(0, len(done)):
                if done[x]:
                    numberOfStepBeforeDone[x] = (j * config.a2c.num_steps + step + 1) - stepOnLastGoal[x]
                    stepOnLastGoal[x] = (j * config.a2c.num_steps + step + 1)
                    anydone = True
            evaluator.update(reward, done, info, numberOfStepBeforeDone)

            # if anydone:
            #     if config.recording:
            #         record()


            if stop_after_update_number > 0:
                if j > stop_after_update_number:
                    break

            elif config.a2c.stop_learning:
                if first_time:
                    first_time = False
                    last_reward_mean = evaluator.get_reward_mean()
                    last_reward_median = evaluator.get_reward_median()
                else:
                    current_reward_mean = evaluator.get_reward_mean()
                    current_reward_median = evaluator.get_reward_median()

                    # Rewards are close to the goal reward
                    if current_reward_median >= (config.rewards.standard.goal + steps_reward):
                        identical_rewards += 1
                        # print("--> rewards close to goal reward -> " + str(identical_rewards))

                    else:
                        identical_rewards = 0
                    #
                    # if current_reward_mean == last_reward_mean:
                    #      identical_rewards += 1
                    #  else:
                    #      identical_rewards = 0
                    last_reward_mean = current_reward_mean
                    last_reward_median = current_reward_median
            if identical_rewards == config.a2c.stop_learning:
                break
            reward = torch.from_numpy(np.expand_dims(np.stack(reward), 1)).float()
            episode_rewards += reward

            # If done then clean the history of observations.
            masks = torch.FloatTensor([[0.0] if done_ else [1.0] for done_ in done])
            final_rewards *= masks
            final_rewards += (1 - masks) * episode_rewards
            episode_rewards *= masks

            if args.cuda:
                masks = masks.cuda()

            if current_obs.dim() == 4:
                current_obs *= masks.unsqueeze(2).unsqueeze(2)
            elif current_obs.dim() == 3:
                current_obs *= masks.unsqueeze(2)
            else:
                current_obs *= masks

            update_current_obs(obs)
            rollouts.insert(step, current_obs, states.data, action.data, action_log_prob.data, value.data, reward,
                            masks)

        next_value = actor_critic(
            Variable(rollouts.observations[-1], volatile=True),
            Variable(rollouts.states[-1], volatile=True),
            Variable(rollouts.masks[-1], volatile=True)
        )[0].data

        rollouts.compute_returns(next_value, args.use_gae, args.gamma, args.tau)

        if config.a2c.algorithm in ['a2c', 'acktr']:
            values, action_log_probs, dist_entropy, states = actor_critic.evaluate_actions(
                Variable(rollouts.observations[:-1].view(-1, *obs_shape)),
                Variable(rollouts.states[:-1].view(-1, actor_critic.state_size)),
                Variable(rollouts.masks[:-1].view(-1, 1)),
                Variable(rollouts.actions.view(-1, action_shape))
            )

            values = values.view(config.a2c.num_steps, config.a2c.num_processes, 1)
            action_log_probs = action_log_probs.view(config.a2c.num_steps, config.a2c.num_processes, 1)

            advantages = Variable(rollouts.returns[:-1]) - values
            value_loss = advantages.pow(2).mean()

            action_loss = -(Variable(advantages.data) * action_log_probs).mean()

            if config.a2c.algorithm == 'acktr' and optimizer.steps % optimizer.Ts == 0:
                # Sampled fisher, see Martens 2014
                actor_critic.zero_grad()
                pg_fisher_loss = -action_log_probs.mean()

                value_noise = Variable(torch.randn(values.size()))
                if args.cuda:
                    value_noise = value_noise.cuda()

                sample_values = values + value_noise
                vf_fisher_loss = -(values - Variable(sample_values.data)).pow(2).mean()

                fisher_loss = pg_fisher_loss + vf_fisher_loss
                optimizer.acc_stats = True
                fisher_loss.backward(retain_graph=True)
                optimizer.acc_stats = False

            optimizer.zero_grad()
            (value_loss * args.value_loss_coef + action_loss - dist_entropy * args.entropy_coef).backward()

            if config.a2c.algorithm == 'a2c':
                nn.utils.clip_grad_norm(actor_critic.parameters(), args.max_grad_norm)

            optimizer.step()
        elif config.a2c.algorithm == 'ppo':
            advantages = rollouts.returns[:-1] - rollouts.value_preds[:-1]
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-5)

            for e in range(args.ppo_epoch):
                if args.recurrent_policy:
                    data_generator = rollouts.recurrent_generator(advantages, args.num_mini_batch)
                else:
                    data_generator = rollouts.feed_forward_generator(advantages, args.num_mini_batch)

                for sample in data_generator:
                    observations_batch, states_batch, actions_batch, \
                    return_batch, masks_batch, old_action_log_probs_batch, \
                    adv_targ = sample

                    # Reshape to do in a single forward pass for all steps
                    values, action_log_probs, dist_entropy, states = actor_critic.evaluate_actions(
                        Variable(observations_batch),
                        Variable(states_batch),
                        Variable(masks_batch),
                        Variable(actions_batch)
                    )

                    adv_targ = Variable(adv_targ)
                    ratio = torch.exp(action_log_probs - Variable(old_action_log_probs_batch))
                    surr1 = ratio * adv_targ
                    surr2 = torch.clamp(ratio, 1.0 - args.clip_param, 1.0 + args.clip_param) * adv_targ
                    action_loss = -torch.min(surr1, surr2).mean()  # PPO's pessimistic surrogate (L^CLIP)

                    value_loss = (Variable(return_batch) - values).pow(2).mean()

                    optimizer.zero_grad()
                    (value_loss + action_loss - dist_entropy * args.entropy_coef).backward()
                    nn.utils.clip_grad_norm(actor_critic.parameters(), args.max_grad_norm)
                    optimizer.step()

        rollouts.after_update()

        save_dir = "../" + config.evaluation_directory_name + "/a2c/trained_model/"
        if j % config.a2c.save_model_interval == 0:
            # save_path = os.path.join(save_dir, config.a2c.algorithm)
            save_path = save_dir
            try:
                os.makedirs(save_path)
            except OSError:
                pass

            # A really ugly way to save a model to CPU
            save_model = actor_critic
            if args.cuda:
                save_model = copy.deepcopy(actor_critic).cpu()

            save_model = [save_model,
                          hasattr(envs, 'ob_rms') and envs.ob_rms or None]
            torch.save(save_model, os.path.join(save_path, config.env_name + ".pt"))




        if j % config.a2c.save_evaluation_interval == 0:
            end = time.time()
            total_num_steps = (j + 1) * config.a2c.num_processes * config.a2c.num_steps

            # Save in the evaluator
            evaluator.save(j, start, end, dist_entropy, value_loss, action_loss)
            print(
                "Updates {}, num timesteps {}, FPS {}, mean/median reward {:.2f}/{:.2f}, min/max reward {:.2f}/{:.2f}, entropy {:.5f}, value loss {:.5f}, policy loss {:.5f}".
                    format(
                    j,
                    total_num_steps,
                    int(total_num_steps / (end - start)),
                    final_rewards.mean(),
                    final_rewards.median(),
                    final_rewards.min(),
                    final_rewards.max(),
                    dist_entropy.data[0],
                    value_loss.data[0],
                    action_loss.data[0]
                )
            )

        if config.visdom and j % config.visdom_interval == 0:
            win = visdom_plot(
                total_num_steps,
                final_rewards.mean()
            )


if __name__ == "__main__":
    main()
