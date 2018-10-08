try:
    import os
    import gym_minigrid
    from gym_minigrid.wrappers import *
    from gym_minigrid.envelopes_light import *
    from gym import wrappers, logger
except Exception as e:
    print(" =========== =========== IMPORT ERROR ===========")
    print(e)
    pass

from configurations import config_grabber as cg


def make_env(env_id, seed, rank, evaluation_id, force=False, resume=False, custom_message="_"):

    config = cg.Configuration.grab()

    def _thunk():
        env = gym.make(env_id)
        env.seed(seed + rank)

        if config.envelope:
            env = SafetyEnvelope(env)

        # record only the first agent
        if config.recording and rank==0:
            print("starting recording..")
            eval_folder = os.path.abspath(os.path.dirname(__file__) + "/../" + config.evaluation_directory_name)
            if config.envelope:
                expt_dir = eval_folder + "/" + evaluation_id + "_videos"
            else:
                expt_dir = eval_folder + "/" + evaluation_id + "_videos"

            uid = "___proc_n_" + str(rank) + " ___" + custom_message + "__++__"
            env = wrappers.Monitor(env, expt_dir, uid=uid, force=force, resume=resume)

        return env

    return _thunk
