
from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register
import random

class RandomEnv(ExMiniGridEnv):

    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls=True
        )

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the top-left corner
        self.start_pos = (1, 1)
        self.start_dir = 0

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        # Set the random seed to the random token, so we can reproduce the environment
        random.seed("3062")

        # Place water
        placed_water_tiles = 0
        while 5 > placed_water_tiles:
            # Minus 2 because grid is zero indexed, and the last one is just a wall
            width_pos = random.randint(1, width - 2)
            height_pos = random.randint(1, height - 2)

            if width_pos == 1 and height_pos == 1:
                # Do not place water on agent
                continue
            if width_pos == 1 and height_pos == 2 and isinstance(self.grid.get(2, 1), Water) or width_pos == 2 and height_pos == 1 and isinstance(self.grid.get(1, 2), Water):
                # Do not place two water tiles in front of the agent A W -
                #                                                    W | |
                #                                                    | | |
                continue
            if isinstance(self.grid.get(width_pos, height_pos), Water):
                # Do not place water on water
                continue
            if isinstance(self.grid.get(width_pos, height_pos), Goal):
                # Do not place water on Goal
                continue
            if width_pos == width - 2 and height_pos == height - 3 and isinstance(self.grid.get(width - 3, height - 2), Water) or width_pos == width - 3 and height_pos == height - 2 and isinstance(self.grid.get(width - 2, height - 3), Water):
                # Do not place water preventing the agent from reaching the goal - | |
                #                                                                - A W
                #                                                                - W G
                continue
            self.grid.set(width_pos, height_pos, Water())
            placed_water_tiles += 1
        self.mission = ""

class RandomEnv10x10_3062(RandomEnv):
    def __init__(self):
        super().__init__(size=10)

register(
    id='MiniGrid-RandomEnv-10x10-3062-v0',
    entry_point='gym_minigrid.envs:RandomEnv10x10_3062'
)
