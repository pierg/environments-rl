from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register
from gym_minigrid.envelopes import *

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

        self.old_front_elm = self.worldobj_in_front_agent_noDark()

        self.mission = "Clean the room"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        # Check if the agent clean a dirt
        if self.old_front_elm == "dirt" \
                and action == self.actions.toggle:
            info = {}
            reward = 0.5
        self.old_front_elm = self.worldobj_in_front_agent_noDark()


        # Check the goal of the grid
        #if hasattr(self, 'list_dirt'):
        if len(self.list_dirt) == 0:
                done = True
                reward = reward + 1
                self.step_number = 0


        return obs, reward, done, info

register(
    id='MiniGrid-CleaningEnv-8x8-v0',
    entry_point='gym_minigrid.envs:CleaningEnv'
)