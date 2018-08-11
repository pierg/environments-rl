try:
    import gym_minigrid
    from gym_minigrid.wrappers import *
    from gym_minigrid.envelopes import *
    from gym import wrappers, logger
except Exception as e:
    print(" =========== =========== IMPORT ERROR ===========")
    print(e)
    pass

from configurations import config_grabber as cg


def make_env(env_id, seed, rank):

    config = cg.Configuration.grab()

    def _thunk():
        env = gym.make(env_id)

        env.seed(seed + rank)

        if config.controller:
            env = SafetyEnvelope(env)

        if config.recording:
            print("starting recording..")
            eval_folder = os.path.abspath(os.path.dirname(__file__) + "/../" + config.evaluation_directory_name)
            if config.controller:
                expt_dir = eval_folder + "/a2c/a2c_videos_yes/"
            else:
                expt_dir = eval_folder + "/a2c/a2c_videos_no/"
            env = wrappers.Monitor(env, expt_dir, force=True)

        return env

    return _thunk
