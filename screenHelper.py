#!/usr/bin/env python3

from __future__ import division, print_function

import time
from optparse import OptionParser
import sys
sys.path.insert(0,'../gym-minigrid/gym_minigrid')
sys.path.insert(1,'../gym-minigrid/')
import pyscreenshot
import configurations.config_grabber as cg
try:
    import gym
    import gym_minigrid
except Exception as e:
    print(e)
    pass


def main(file="main"):
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
    config = cg.Configuration.grab(file)
    path = ""
    if "crafted" in file:
        path = "crafted/"
    elif "randoms" in file:
        path = "randoms/"
    # Overriding arguments with configuration file
    options.env_name = config.env_name

    # Load the gym environment
    env = gym.make(options.env_name)

    # Create a window to render into
    renderer = env.render('human')

    # Repeat rendering to avoid errors
    time.sleep(0.01)
    env.render('human')

    # Wait 1s and take a screen
    time.sleep(1)
    box = (renderer.window.x(),renderer.window.y(),renderer.window.x()+renderer.window.width(),renderer.window.y()+renderer.window.height())
    image = pyscreenshot.grab(box)
    time.sleep(1)

    # Save the screen
    image.save("results/screens/"+path+config.env_name+".png")



if __name__ == "__main__":
    if len(sys.argv)>1:
        print("file is :",sys.argv[1])
        main(sys.argv[1])
    else:
        print("main")
        main("main")
