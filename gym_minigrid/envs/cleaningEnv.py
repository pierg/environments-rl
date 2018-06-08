from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register
from configurations import config_grabber as cg

class CleaningEnv(ExMiniGridEnv):

    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls=False


        )
    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.agent_pos = (1, 1)
        self.agent_dir = 0



        #self.list_dirt: name of the list who envelopes.py check to know if the room is clean
        # WARNING don't change the name of list_dirt if you want to use the cleaning robot
        self.list_dirt = []
        #Place dirt
        self.number_dirt = 3
        for k in range(self.number_dirt):
            dirt = Dirt()
            x, y = self._rand_pos(2, width-2, 2, height - 2)
            # a dirt pattern need    a list to have the number of dirt in the environnemet
            while self.grid.get(x,y) is  not None:
                x, y = self._rand_pos(2, width - 2, 2, height - 2)
            self.grid.set(x, y, dirt)
            self.list_dirt.append(dirt)
            dirt.affect_list(self.list_dirt)


        #Place Vase

        for i in range(1):
            vase = Vase()
            x2, y2 = self._rand_pos(2, width - 2, 2, height - 2)
            while self.grid.get(x2, y2) is not None:
                x2, y2 = self._rand_pos(2, width - 2, 2, height - 2)

        # a vase pattern need the greed and the position to change on dirt if the agent
            self.grid.set(x2, y2, vase)
        #vase.affect_grid(self.grid,(x2,y2))
            vase.list_dirt(self.list_dirt)

        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "Clean the room"

    def step(self, action):
        reward = 0
        info = {}
        # Check if the agent clean a dirt
        if self.worldobj_in_agent(1, 0) == "dirt" \
                and action == self.actions.toggle:
            reward = cg.Configuration.grab().rewards.cleaningenv.clean

        if self.worldobj_in_agent(1, 0) == "vase" \
                and action == self.actions.toggle:
            info = "break"

        if reward != 0:
            obs, useless, done, info = super().step(action)
        elif info is not {}:
            obs, reward, done, useless = super().step(action)
        else:
            obs, reward, done, info = super().step(action)

            # Check the room is clean
        if len(self.list_dirt) == 0:
            done = True
            reward = reward + cg.Configuration.grab().rewards.standard.goal
            self.step_number = 0
            info = "goal"

        return obs, reward, done, info


register(
    id='MiniGrid-CleaningEnv-8x8-v0',
    entry_point='gym_minigrid.envs:CleaningEnv'
)
