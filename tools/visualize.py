import numpy as np

vis = None

win1 = None
win2 = None

avg_reward = 0

X = []
Y1 = []
Y2 = []



def visdom_plot(
    total_num_steps,
    cum_reward
):
    from visdom import Visdom

    global vis
    global win1
    global win2
    global avg_reward

    if vis is None:
        vis = Visdom()
        assert vis.check_connection()

        # Close all existing plots
        vis.close()

    # Running average for curve smoothing
    # avg_reward = avg_reward * 0.9 + 0.1 * cum_reward
    avg_reward = cum_reward / total_num_steps

    X.append(total_num_steps)
    Y1.append(cum_reward)
    Y2.append(avg_reward)

    # The plot with the handle 'win' is updated each time this is called
    win1 = vis.line(
        X = np.array(X),
        Y = np.array(Y1),
        opts = dict(
            #title = 'All Environments',
            xlabel='Total number of steps',
            ylabel='Cumulative reward',
            ytickmin=0,
            #ytickmax=1,
            #ytickstep=0.1,
            #legend=legend,
            #showlegend=True,
            width=900,
            height=500
        ),
        win = win1
    )

    # The plot with the handle 'win' is updated each time this is called
    win2 = vis.line(
        X=np.array(X),
        Y=np.array(Y2),
        opts=dict(
            # title = 'All Environments',
            xlabel='Total number of episodes',
            ylabel='Average Reward',
            ytickmin=0,
            # ytickmax=1,
            # ytickstep=0.1,
            # legend=legend,
            # showlegend=True,
            width=900,
            height=500
        ),
        win=win2
    )