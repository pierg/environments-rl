from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class UnsafeEnv(MiniGridEnv):
    """
    Empty grid environment, no obstacles, sparse reward
    """

    def __init__(self, size=8):
        super().__init__(grid_size=size, max_steps=3*size)

    def _genGrid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horzWall(0, 0)
        self.grid.horzWall(0, height-1)
        self.grid.vertWall(0, 0)
        self.grid.vertWall(width-1, 0)

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())
        #self.grid.set(width - 4, height - 4, Water())
        #self.grid.set(width - 2, height - 5, Water())
        self.grid.set(width - 5, height - 2, Water())
        #self.grid.set(width - 6, height - 4, Water())
        #self.grid.set(width - 7, height - 4, Water())

        # Set start position
        self.start_pos = (1,1)
        self.start_dir=0


        self.mission = "get to the green goal square without moving on water"

class UnsafeEnv6x6(UnsafeEnv):
    def __init__(self):
        super().__init__(size=6)

class UnsafeEnv16x16(UnsafeEnv):
    def __init__(self):
        super().__init__(size=16)

register(
    id='MiniGrid-UnsafeEnvironment-6x6-v0',
    entry_point='gym_minigrid.envs:UnsafeEnv6x6'
)

register(
    id='MiniGrid-UnsafeEnvironment-8x8-v0',
    entry_point='gym_minigrid.envs:UnsafeEnv'
)

register(
    id='MiniGrid-UnsafeEvnironment-16x16-v0',
    entry_point='gym_minigrid.envs:UnsafeEnv16x16'
)
