import numpy as np

vis = None
cum_rwd = None
goal = None


def visdom_plot(what, x, x_label, y, y_label):

    from visdom import Visdom

    global vis
    global cum_rwd
    global goal

    if vis is None:
        vis = Visdom()
        assert vis.check_connection()
        # Close all existing plots
        vis.close()

    if what == "cum_rwd":
        cum_rwd = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                # title = 'All Environments',
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                # ytickmax=1,
                # ytickstep=0.1,
                # legend=legend,
                # showlegend=True,
                width=900,
                height=500
            ),
            win = cum_rwd
        )

    if what == "goal":
        goal = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                # title = 'All Environments',
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                # ytickmax=1,
                # ytickstep=0.1,
                # legend=legend,
                # showlegend=True,
                width=900,
                height=500
            ),
            win = goal
        )