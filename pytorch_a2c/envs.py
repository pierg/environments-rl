try:
    import gym_minigrid
    from gym_minigrid.wrappers import *
    from gym_minigrid.envelopes import *
    from gym import wrappers, logger
except Exception as e:
    print(" =========== =========== IMPORT ERROR ===========")
    print(e)
    pass

import os

from configurations import config_grabber as cg


def make_env(env_id, seed, rank, force=False, resume=False, custom_message="_"):

    config = cg.Configuration.grab()

    def _thunk():
        env = gym.make(env_id)
        env.seed(seed + rank)

        if config.action_plan:
            env = ActionPlannerEnvelope(env)

        # record only the first agent
        if config.recording and rank==0:
            print("starting recording..")
            eval_folder = os.path.abspath(os.path.dirname(__file__) + "/../" + config.evaluation_directory_name)
            if config.action_plan:
                expt_dir = eval_folder + "/a2c/a2c_videos_yes/"
            else:
                expt_dir = eval_folder + "/a2c/a2c_videos_no/"

            uid = "___proc_n_" + str(rank) + " ___" + custom_message + "__++__"
            env = wrappers.Monitor(env, expt_dir, uid=uid, force=True, resume=resume)

        return env

    return _thunk
