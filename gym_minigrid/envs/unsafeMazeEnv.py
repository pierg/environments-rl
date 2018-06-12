from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

from configurations import config_grabber as cg


class UnsafeMazeEnv(ExMiniGridEnv):

    """
        Maze, looks like this:
        # # # # # # # #
        # > x   x x x #
        #   x x x     #
        #             #
        # x   x x     #
        # x       x   #
        # x   x   x G #
        # # # # # # # #
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

        self.random = self.config.action_planning.random_unsafe_obj

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
        self.grid.set(width - 2, height - 7, Unsafe())
        self.grid.set(width - 3, height - 7, Unsafe())
        self.grid.set(width - 4, height - 7, Unsafe())
        self.grid.set(width - 6, height - 7, Unsafe())

        self.grid.set(width - 6, height - 6, Unsafe())
        self.grid.set(width - 5, height - 6, Unsafe())
        self.grid.set(width - 4, height - 6, Unsafe())

        self.grid.set(width - 7, height - 4, Unsafe())
        self.grid.set(width - 5, height - 4, Unsafe())
        self.grid.set(width - 4, height - 4, Unsafe())

        self.grid.set(width - 7, height - 3, Unsafe())
        self.grid.set(width - 3, height - 3, Unsafe())

        self.grid.set(width - 7, height - 2, Unsafe())
        self.grid.set(width - 5, height - 2, Unsafe())
        self.grid.set(width - 3, height - 2, Unsafe())

        self.mission = "get to the green goal square"


class UnsafeMazeEnv8x8(UnsafeMazeEnv):
    def __init__(self):
        super().__init__(size=8)


class UnsafeMazeEnv12x12(UnsafeMazeEnv):
    def __init__(self):
        super().__init__(size=12)


register(
    id='MiniGrid-UnsafeMazeEnv-8x8-v0',
    entry_point='gym_minigrid.envs:UnsafeMazeEnv8x8'
)

register(
    id='MiniGrid-UnsafeMazeEnv-12x12-v0',
    entry_point='gym_minigrid.envs:UnsafeMazeEnv12x12'
)
