import gym

import torch
import torch.nn as nn
import torch.optim as optim
import torch.autograd as autograd

import matplotlib.pyplot as plt

from tools.arguments import get_args
from pytorch_dqn.evaluator_frames import Evaluator as ev_frames
from pytorch_dqn.evaluator_episodes import Evaluator as ev_epi

try:
    import gym_minigrid
    from gym_minigrid.wrappers import *
    from gym_minigrid.envelopes import *
    from configurations import config_grabber as cg
except Exception as e:
    print(" =========== =========== IMPORT ERROR ===========")
    print(e)
    pass

args = get_args()

cg.Configuration.set("training_mode", True)
cg.Configuration.set("debug_mode", False)

if args.norender:
    cg.Configuration.set("rendering", False)

config = cg.Configuration.grab()

# Initializing evaluation
evaluator_frames = ev_frames("dqn")
evaluator_episodes = ev_epi("dqn")


env = gym.make(config.env_name)
# env.seed(seed + rank)
if config.controller:
    env = SafetyEnvelope(env)

# until RL code supports dict observations, squash observations into a flat vector
if isinstance(env.observation_space, spaces.Dict):
    env = FlatImageObs(env)

from collections import deque


USE_CUDA = torch.cuda.is_available()
Variable = lambda *args, **kwargs: autograd.Variable(*args, **kwargs).cuda() if USE_CUDA else autograd.Variable(*args, **kwargs)

class ReplayBuffer(object):
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        state = np.expand_dims(state, 0)
        next_state = np.expand_dims(next_state, 0)

        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        state, action, reward, next_state, done = zip(*random.sample(self.buffer, batch_size))
        return np.concatenate(state), action, reward, np.concatenate(next_state), done

    def __len__(self):
        return len(self.buffer)


epsilon_start = 1.0
epsilon_final = 0.00
epsilon_decay_frame = 500
epsilon_decay_episodes = 10

epsilon_by_frame = lambda frame_idx: epsilon_final + (epsilon_start - epsilon_final) * math.exp(-1. * frame_idx / epsilon_decay_frame)
epsilon_by_episodes = lambda episode_idx: epsilon_final + (epsilon_start - epsilon_final) * math.exp(-1. * episode_idx / epsilon_decay_episodes)

# plt.plot([epsilon_by_frame(i) for i in range(10000)])
plt.plot([epsilon_by_episodes(i) for i in range(10000)])
# plt.savefig('epsilon_by_episodes.png')

class DQN(nn.Module):
    def __init__(self, num_inputs, num_actions):
        super(DQN, self).__init__()

        self.layers = nn.Sequential(
            nn.Linear(env.observation_space.shape[1], 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, env.action_space.n)
        )

    def forward(self, x):
        return self.layers(x)

    def act(self, state, epsilon):
        if random.random() > epsilon:
            state = Variable(torch.FloatTensor(state).unsqueeze(0), volatile=True)
            q_value = self.forward(state)
            action = q_value.max(1)[1].data[0]
        else:
            action = random.randrange(env.action_space.n)
        return action



model = DQN(env.observation_space.shape[0], env.action_space.n)
optimizer = optim.Adam(model.parameters())
replay_buffer = ReplayBuffer(1000)


def compute_td_loss(batch_size):
    state, action, reward, next_state, done = replay_buffer.sample(batch_size)

    state = Variable(torch.FloatTensor(np.float32(state)))
    next_state = Variable(torch.FloatTensor(np.float32(next_state)), volatile=True)
    action = Variable(torch.LongTensor(action))
    reward = Variable(torch.FloatTensor(reward))
    done = Variable(torch.FloatTensor(done))

    q_values = model(state)
    next_q_values = model(next_state)

    q_value = q_values.gather(1, action.unsqueeze(1)).squeeze(1)
    next_q_value = next_q_values.max(1)[0]
    expected_q_value = reward + gamma * next_q_value * (1 - done)

    loss = (q_value - Variable(expected_q_value.data)).pow(2).mean()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss

max_num_frames = config.dqn.max_num_frames
batch_size = 32
gamma = 0.99

losses = []
all_episodes_rewards = []
episode_reward = 0

# Used for evaluations
cum_reward = 0

# Frames evauators
# All values below  refer to the logging interval 'results_log_interval'
all_rewards_f = []
all_losses_f = []
n_episodes_f = 0
n_deaths_f = 0
n_goals_f = 0
n_violations_f = 0

# Episodes evaluators
all_rewards_e = []
cum_reward_e = 0
all_losses_e = []
n_deaths_e = 0
n_goals_e = 0
n_violations_e = 0

state = env.reset()

episode_idx = 0

print("\nTraining started...")
for frame_idx in range(1, max_num_frames + 1):

    # Render grid
    if config.rendering:
        env.render('human')

    # epsilon = epsilon_by_frame(frame_idx)
    epsilon = epsilon_by_episodes(episode_idx)
    action = model.act(state, epsilon)

    next_state, reward, done, info = env.step(action)
    replay_buffer.push(state, action, reward, next_state, done)

    state = next_state
    episode_reward += reward

    # Evaluation
    cum_reward += reward
    cum_reward_e += reward
    all_rewards_f.append(reward)
    all_rewards_e.append(reward)
    if "died" in info:
        n_deaths_f += 1
        n_deaths_e += 1
    if "goal" in info:
        n_goals_f += 1
        n_goals_e += 1
    if "violation" in info:
        n_violations_f += 1
        n_violations_e += 1

    if done:
        state = env.reset()
        all_episodes_rewards.append(episode_reward)
        episode_reward = 0
        n_episodes_f += 1
        episode_idx += 1

        evaluator_episodes.update(episode_idx, all_rewards_e, cum_reward_e, all_losses_e, n_deaths_e, n_goals_e, n_violations_e, epsilon)
        evaluator_episodes.save()

        # Resetting episodes evaluators
        all_rewards_e = []
        cum_reward_e = 0
        all_losses_e = []
        n_deaths_e = 0
        n_goals_e = 0
        n_violations_e = 0



    if len(replay_buffer) > batch_size:
        loss = compute_td_loss(batch_size)
        losses.append(loss.data[0])
        all_losses_f.append(loss.data[0])
        all_losses_e.append(loss.data[0])

    if frame_idx % config.dqn.results_log_interval == 0:
        evaluator_frames.update(frame_idx, all_rewards_f, cum_reward, all_losses_f, n_episodes_f, n_deaths_f, n_goals_f, n_violations_f, epsilon)

        print("...n_frame | n_episodes | n_goals | epsilon:\t" + str(frame_idx) + "\t" + str(episode_idx) + "\t" + str(n_goals_f) + "\t" + str(epsilon))

        # Resetting values
        all_rewards_f = []
        all_losses_f = []
        n_episodes_f = 0
        n_deaths_f = 0
        n_goals_f = 0
        n_violations_f = 0
        evaluator_frames.save()

print("...Trained finished!\n")
