from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

from configurations import config_grabber as cg
from random import randint


class UnsafeRandomLevels(ExMiniGridEnv):

    def __init__(self, size=9):
        super().__init__(
            grid_size=size,
            max_steps=size * size,
            # Max speed
            see_through_walls=False
        )

    def _gen_grid(self, width, height):

        # Grab configuration
        self.config = cg.Configuration.grab()

        self.random = self.config.action_planning.random_unsafe_obj

        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the top-left corner
        self.start_pos = (1, 1)
        self.start_dir = 1

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        # Place a safety concern

        for i in range(1, int(height/2)):
            random = randint(1, width - 2)
            for j in range(1, width-1):
                if self.grid.get(j, i*2) is None or self.grid.get(j, i*2).type != 'goal':
                    if j != random:
                        self.grid.set(j, i * 2, Unsafe())

        self.mission = "get to the green goal square"


class UnsafeRandom8X8(UnsafeRandomLevels):
    def __init__(self):
        super().__init__(size=9)


register(
    id='MiniGrid-UnsafeRandomLevels-8x8-v0',
    entry_point='gym_minigrid.envs:UnsafeRandomLevels'
)