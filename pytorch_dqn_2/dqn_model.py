import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, in_channels=4, num_actions=18):
        """
        Initialize a deep Q-learning network as described in
        https://storage.googleapis.com/deepmind-data/assets/papers/DeepMindNature14236Paper.pdf
        Arguments:
            in_channels: number of channel of input.
                i.e The number of most recent frames stacked together as describe in the paper
            num_actions: number of action-value to output, one-to-one correspondence to action in game.
        """
    #     super(DQN, self).__init__()
    #     self.conv1 = nn.Conv2d(in_channels, 32, kernel_size=8, stride=4)
    #     self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
    #     self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
    #     self.fc4 = nn.Linear(7 * 7 * 64, 512)
    #     self.fc5 = nn.Linear(512, num_actions)
    #
    # def forward(self, x):
    #     x = F.relu(self.conv1(x))
    #     x = F.relu(self.conv2(x))
    #     x = F.relu(self.conv3(x))
    #     x = F.relu(self.fc4(x.view(x.size(0), -1)))
    #     return self.fc5(x)
    def __init__(self, num_inputs, num_actions):
        super(DQN, self).__init__()

        self.layers = nn.Sequential(
            nn.Linear(num_inputs, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions)
        )

    def forward(self, x):
        return self.layers(x)


class DQN_2(nn.Module):
    def __init__(self, num_inputs, num_actions):
        super(DQN, self).__init__()

        self.layers = nn.Sequential(
            nn.Linear(num_inputs, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions)
        )

    def forward(self, x):
        return self.layers(x)

    # def act(self, state, epsilon):
    #     if random.random() > epsilon:
    #         state = Variable(torch.FloatTensor(state).unsqueeze(0), volatile=True)
    #         q_value = self.forward(state)
    #         action = q_value.max(1)[1].data[0]
    #     else:
    #         action = random.randrange(env.action_space.n)
    #     return action


class DQN_RAM(nn.Module):
    def __init__(self, in_features=4, num_actions=18):
        """
        Initialize a deep Q-learning network for testing algorithm
            in_features: number of features of input.
            num_actions: number of action-value to output, one-to-one correspondence to action in game.
        """
        super(DQN_RAM, self).__init__()
        self.fc1 = nn.Linear(in_features, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, num_actions)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        return self.fc4(x)
