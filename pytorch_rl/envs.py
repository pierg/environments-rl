try:
    import gym_minigrid
    from gym_minigrid.wrappers import *
    from gym_minigrid.envelopes import *
except Exception as e:
    print(" =========== =========== IMPORT ERROR ===========")
    print(e)
    pass

from configurations import config_grabber as cg


def make_env(env_id, seed, rank, log_dir):

    config = cg.Configuration.grab()

    def _thunk():
        env = gym.make(env_id)

        env.seed(seed + rank)

        if config.monitors:
            env = ActionPlannerEnvelope(env)

        # Maxime: until RL code supports dict observations, squash observations into a flat vector
        if isinstance(env.observation_space, spaces.Dict):
            env = FlatObsWrapper(env)

        return env

    return _thunk
