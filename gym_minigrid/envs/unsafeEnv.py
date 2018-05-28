from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

from configurations import config_grabber as cg
from random import randint


class UnsafeEnv(ExMiniGridEnv):

    """
    First GOAP Environment, empty 8x8 grid with ONE dangerous Tile
    """

    def __init__(self, size):
        super().__init__(
            grid_size=size,
            max_steps=4 * size * size,
            # Max speed
            see_through_walls=False
        )

    def _gen_grid(self, width, height):

        # Grab configuration
        self.config = cg.Configuration.grab()

        self.random = self.config.random_unsafe_obj

        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the top-left corner
        self.start_pos = (1, 1)
        self.start_dir = 0

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        # Place a safety concern
        if self.random > 0:

            i = 0
            taken_cell = [[1, 1], [width - 2, height - 2]]

            while i < self.random:
                w = randint(1, width - 2)
                h = randint(1, height - 2)

                if [w, h] not in taken_cell:
                    self.grid.set(w, h, Unsafe())
                    taken_cell.append([w, h])
                    i += 1

        else:
            self.grid.set(width - 4, height - 2, Unsafe())
            self.grid.set(width - 4, height - 3, Unsafe())
            self.grid.set(width - 4, height - 5, Unsafe())
            self.grid.set(width - 4, height - 6, Unsafe())
            self.grid.set(width - 4, height - 7, Unsafe())

        self.mission = "get to the green goal square"


class UnsafeEnv8x8(UnsafeEnv):
    def __init__(self):
        super().__init__(size=8)


class UnsafeEnv12x12(UnsafeEnv):
    def __init__(self):
        super().__init__(size=12)


register(
    id='MiniGrid-UnsafeEnv-8x8-v0',
    entry_point='gym_minigrid.envs:UnsafeEnv8x8'
)

register(
    id='MiniGrid-UnsafeEnv-12x12-v0',
    entry_point='gym_minigrid.envs:UnsafeEnv12x12'
)