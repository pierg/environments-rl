import argparse
import os
import sys
import types
import time

import numpy as np
import torch
from torch.autograd import Variable
from vec_env.dummy_vec_env import DummyVecEnv
from pathlib import Path

from envs import make_env

"""
This file is almost a copy of enjoy.py,the option are modified a bit :
    -e instead of --env-name to select the trained model you want
    -d instead of --load-dir to select the trained model directory (a2c in our case)
"""

parser = argparse.ArgumentParser(description='RL')
parser.add_argument('--seed', type=int, default=1,
                    help='random seed (default: 1)')
parser.add_argument('--num-stack', type=int, default=1,
                    help='number of frames to stack (default: 1)')
parser.add_argument('--log-interval', type=int, default=10,
                    help='log interval, one log per n updates (default: 10)')
parser.add_argument('-e', default='MiniGrid-Unsafe-6x6-v0',
                    help='environment to train on (default: MiniGrid-Unsafe-6x6-v0')
parser.add_argument('-d', default='./trained_models/a2c/',
                    help='directory to save agent logs (default: ./trained_models/a2c/)')
args = parser.parse_args()

environment = args.d+args.e+".pt"
environment = Path(environment)
if environment.exists():
    env = make_env(args.e, args.seed, 0, None)
    env = DummyVecEnv([env])

    actor_critic, ob_rms = torch.load(os.path.join(args.d, args.e + ".pt"))

    render_func = env.envs[0].render

    obs_shape = env.observation_space.shape
    obs_shape = (obs_shape[0] * args.num_stack, *obs_shape[1:])
    current_obs = torch.zeros(1, *obs_shape)
    states = torch.zeros(1, actor_critic.state_size)
    masks = torch.zeros(1, 1)

    def update_current_obs(obs):
        shape_dim0 = env.observation_space.shape[0]
        obs = torch.from_numpy(obs).float()
        if args.num_stack > 1:
            current_obs[:, :-shape_dim0] = current_obs[:, shape_dim0:]
        current_obs[:, -shape_dim0:] = obs

    render_func('human')
    obs = env.reset()
    update_current_obs(obs)

    while True:
        value, action, _, states = actor_critic.act(
            Variable(current_obs, volatile=True),
            Variable(states, volatile=True),
            Variable(masks, volatile=True),
            deterministic=True
        )
        states = states.data
        cpu_actions = action.data.squeeze(1).cpu().numpy()

        # Observation, reward and next obs
        obs, reward, done, _ = env.step(cpu_actions)

        time.sleep(0.05)

        masks.fill_(0.0 if done else 1.0)

        if current_obs.dim() == 4:
            current_obs *= masks.unsqueeze(2).unsqueeze(2)
        else:
            current_obs *= masks
        update_current_obs(obs)

        renderer = render_func('human')

        if not renderer.window:
            sys.exit(0)
else:
    print("File does not exist")