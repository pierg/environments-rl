import numpy as np

vis = None
cum_rwd_f = None
goal_f = None
avg_rwd_f = None
last_epsilon_f = None
steps_goal = None

cum_rwd_e = None


def visdom_plot(what, x, x_label, y, y_label, where='main'):
    from visdom import Visdom

    global vis
    global cum_rwd_f
    global goal_f
    global avg_rwd_f
    global last_epsilon_f
    global steps_goal

    global cum_rwd_e

    if vis is None:
        vis = Visdom(env=where)
        vis.close()
    else:
        vis = Visdom(env=where)

    assert vis.check_connection()

    # if vis is None:
    #     vis = Visdom(env=where)
    #     assert vis.check_connection()
    #     # Close all existing plots
    #     vis.close()

    if what == "cum_rwd":
        cum_rwd_f = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                width=300,
                height=250
            ),
            win=cum_rwd_f
        )

    if what == "steps_goal":
        steps_goal = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                width=300,
                height=250
            ),
            win=steps_goal
        )


    if what == "cum_rwd_e":
        cum_rwd_e = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                width=300,
                height=250
            ),
            win=cum_rwd_e
        )

    if what == "avg_rwd":
        avg_rwd_f = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                width=300,
                height=250
            ),
            win=avg_rwd_f
        )

    if what == "goal":
        goal_f = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                width=300,
                height=250
            ),
            win=goal_f
        )

    if what == "last_epsilon":
        last_epsilon_f = vis.line(
            X=np.array(x),
            Y=np.array(y),
            opts=dict(
                xlabel=x_label,
                ylabel=y_label,
                ytickmin=0,
                width=300,
                height=250
            ),
            win=last_epsilon_f
        )
