import numpy as np

vis = None

win1 = None
win2 = None

avg_reward = 0

X = []
Y1 = []
Y2 = []


def test_visdom():
    # Lazily import visdom so that people don't need to install visdom
    # if they're not actually using it
    from visdom import Visdom

    global vis
    global win
    global avg_reward

    vis = Visdom()
    assert vis.check_connection()

    trace = dict(x=[1, 2, 3], y=[4, 5, 6], mode="markers+lines", type='custom',
                 marker={'color': 'red', 'symbol': 104, 'size': "10"},
                 text=["one", "two", "three"], name='1st Trace')
    layout = dict(title="First Plot", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})

    vis._send({'data': [trace], 'layout': layout, 'win': 'mywin'})



def visdom_plot(
    total_num_steps,
    mean_reward
):
    # Lazily import visdom so that people don't need to install visdom
    # if they're not actually using it
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
    avg_reward = avg_reward * 0.9 + 0.1 * mean_reward

    X.append(total_num_steps)
    Y1.append(avg_reward)
    Y2.append(mean_reward)

    # The plot with the handle 'win' is updated each time this is called
    win1 = vis.line(
        X = np.array(X),
        Y = np.array(Y1),
        opts = dict(
            #title = 'All Environments',
            xlabel='Total time steps',
            ylabel='Reward per episode',
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
            xlabel='Total time steps',
            ylabel='Mean Reward',
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


if __name__ == "__main__":
    test_visdom()