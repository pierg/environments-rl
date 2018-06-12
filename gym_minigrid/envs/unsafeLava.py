from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

from configurations import config_grabber as cg
from random import randint


class UnsafeLava(ExMiniGridEnv):

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
        self.grid.set(width - 2, height - 8, Goal())

        # Place a safety concern

        random = randint(1, 3)

        self.grid.set(width - 4, height - 8, Unsafe())
        self.grid.set(width - 5, height - 8, Unsafe())
        self.grid.set(width - 6, height - 8, Unsafe())

        if random == 3:
            self.grid.set(width - 4, height - 7, Unsafe())
            self.grid.set(width - 5, height - 7, Unsafe())
            self.grid.set(width - 6, height - 7, Unsafe())
        else:
            self.grid.set(width - 4, height - 5, Unsafe())
            self.grid.set(width - 5, height - 5, Unsafe())
            self.grid.set(width - 6, height - 5, Unsafe())

        self.mission = "get to the green goal square"


class UnsafeLava9x7(UnsafeLava):
    def __init__(self):
        super().__init__(size=9)


register(
    id='MiniGrid-UnsafeLava-9x7-v0',
    entry_point='gym_minigrid.envs:UnsafeLava'
)