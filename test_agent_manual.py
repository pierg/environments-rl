#!/usr/bin/env python3

from __future__ import division, print_function

import sys
import numpy
import gym
import time
from optparse import OptionParser
from helpers import config_grabber as cg
try:
    import gym_minigrid
    from gym_minigrid.wrappers import *
    from gym_minigrid.envelopes import *
except Exception as e:
    print(e)
    pass

import gym_minigrid

def main():
    parser = OptionParser()
    parser.add_option(
        "-e",
        "--env-name",
        dest="env_name",
        help="gym environment to load",
        default='MiniGrid-MultiRoom-N6-v0'
    )
    (options, args) = parser.parse_args()


    # Getting configuration from file
    config = cg.Configuration.grab()

    # Overriding arguments with configuration file
    options.env_name = config.env_name


    # Load the gym environment
    env = gym.make(options.env_name)

    if config.monitor:
        env = SafetyEnvelope(env)


    # # Maxime: until RL code supports dict observations, squash observations into a flat vector
    # if isinstance(env.observation_space, spaces.Dict):
    #     env = FlatObsWrapper(env)

    def resetEnv():
        env.reset()
        if hasattr(env, 'mission'):
            print('Mission: %s' % env.mission)

    resetEnv()

    # Create a window to render into
    renderer = env.render('human')

    def keyDownCb(keyName):
        if keyName == 'BACKSPACE':
            resetEnv()
            return

        if keyName == 'ESCAPE':
            sys.exit(0)

        action = 0

        if keyName == 'LEFT':
            action = env.env.actions.left
        elif keyName == 'RIGHT':
            action = env.env.actions.right
        elif keyName == 'UP':
            action = env.env.actions.forward

        elif keyName == 'SPACE':
            action = env.env.actions.toggle
        elif keyName == 'PAGE_UP':
            action = env.env.actions.pickup
        elif keyName == 'PAGE_DOWN':
            action = env.env.actions.drop

        elif keyName == 'CTRL':
            action = env.env.actions.wait

        else:
            print("unknown key %s" % keyName)
            return

        obs, reward, done, info = env.step(action)

        print('step=%s, reward=%s' % (env.env.step_count, reward))

        if done:
            print('done!')
            resetEnv()

    renderer.window.setKeyDownCb(keyDownCb)

    while True:
        env.render('human')
        time.sleep(0.01)

        # If the window was closed
        if renderer.window == None:
            break

if __name__ == "__main__":
    main()
