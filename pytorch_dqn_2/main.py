import gym
import torch.optim as optim

from gym import wrappers

from utils.seed import set_global_seeds
from utils.atari_wrapper import wrap_deepmind, wrap_deepmind_ram



from tools.arguments import get_args

from dqn_model import DQN, DQN_RAM
from dqn_learn import OptimizerSpec, dqn_learing
from utils.gym import get_env, get_wrapper_by_name
from utils.schedule import LinearSchedule

from tools.arguments import get_args
from pytorch_dqn.evaluator_frames import Evaluator as ev_frames
from pytorch_dqn.evaluator_episodes import Evaluator as ev_epi

try:
    import gym_minigrid
    from gym_minigrid.wrappers import *
    from gym_minigrid.envelopes import *
    from configurations import config_grabber as cg
except Exception as e:
    print("IMPORT ERROR")
    print(e)
    pass

args = get_args()

cg.Configuration.set("training_mode", True)
cg.Configuration.set("debug_mode", False)

if args.norender:
    cg.Configuration.set("rendering", False)
    cg.Configuration.set("visdom", False)

config = cg.Configuration.grab()

# Initializing evaluation
evaluator_frames = ev_frames("dqn")
evaluator_episodes = ev_epi("dqn")

env = gym.make(config.env_name)
# env.seed(seed + rank)
if config.envelope:
    env = SafetyEnvelope(env)

# until RL code supports dict observations, squash observations into a flat vector
if isinstance(env.observation_space, spaces.Dict):
    env = FlatImageObs(env)



"""
TODOs: 
Better way to  tune down epsilon (when it's finding the minumum path?)

"""

BATCH_SIZE = 32
GAMMA = 0.99
REPLAY_BUFFER_SIZE = 1000000
LEARNING_STARTS = 500
# LEARNING_STARTS = 50000
LEARNING_FREQ = 4
FRAME_HISTORY_LEN = 2
TARGER_UPDATE_FREQ = 10000
LEARNING_RATE = 0.00025
ALPHA = 0.95
EPS = 0.01

def main(env, num_timesteps):

    def stopping_criterion(env):
        # notice that here t is the number of steps of the wrapped env,
        # which is different from the number of steps in the underlying env
        return get_wrapper_by_name(env, "Monitor").get_total_steps() >= num_timesteps

    optimizer_spec = OptimizerSpec(
        constructor=optim.RMSprop,
        kwargs=dict(lr=LEARNING_RATE, alpha=ALPHA, eps=EPS),
    )

    exploration_schedule = LinearSchedule(1000000, 0.1)

    dqn_learing(
        env=env,
        q_func=DQN_RAM,
        optimizer_spec=optimizer_spec,
        exploration=exploration_schedule,
        stopping_criterion=stopping_criterion,
        replay_buffer_size=REPLAY_BUFFER_SIZE,
        batch_size=BATCH_SIZE,
        gamma=GAMMA,
        learning_starts=LEARNING_STARTS,
        learning_freq=LEARNING_FREQ,
        frame_history_len=FRAME_HISTORY_LEN,
        target_update_freq=TARGER_UPDATE_FREQ,
    )

if __name__ == '__main__':
    # # Get Atari games.
    # benchmark = gym.benchmark_spec('Atari40M')

    # # Change the index to select a different game.
    # task = benchmark.tasks[3]

    # Run training
    seed = 0 # Use a seed of zero (you may want to randomize the seed!)

    env = gym.make(config.env_name)

    # env = wrap_deepmind(env)

    if config.envelope:
        env = SafetyEnvelope(env)

    # # until RL code supports dict observations, squash observations into a flat vector
    # if isinstance(env.observation_space, spaces.Dict):
    #     env = FlatImageObs(env)

    set_global_seeds(seed)
    env.seed(seed)

    expt_dir = 'tmp/gym-results'
    env = wrappers.Monitor(env, expt_dir, force=True)
    main(env, config.max_num_steps)
