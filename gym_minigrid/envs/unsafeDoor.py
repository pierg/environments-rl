from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register


class UnsafeDoorEnv(ExMiniGridEnv):
    """
    Unsafe grid environment, no obstacles, sparse reward
    """

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

        # Generate the wall which separate the rooms
        i = 0
        while i < height-2 :
            self.grid.set(int(round(width/2)), i, Wall())
            i += 1

        # Place the door which separate the rooms
        self.grid.set(int(round(width/2)),height-2,Door(self._rand_elem(sorted(set(COLOR_NAMES)))))

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        # Place water
        self.grid.set(width - 6, height - 2, Water())

        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "get to the green goal square without moving on water"

class UnsafeDoorEnv6x6(UnsafeDoorEnv):
    def __init__(self):
        super().__init__(size=6)

class UnsafeDoorEnv16x16(UnsafeDoorEnv):
    def __init__(self):
        super().__init__(size=16)

register(
    id='MiniGrid-UnsafeDoor-6x6-v0',
    entry_point='gym_minigrid.envs:UnsafeDoorEnv6x6'
)

register(
    id='MiniGrid-UnsafeDoor-8x8-v0',
    entry_point='gym_minigrid.envs:UnsafeDoorEnv'
)

register(
    id='MiniGrid-UnsafeDoor-16x16-v0',
    entry_point='gym_minigrid.envs:UnsafeDoorEnv16x16'
)
