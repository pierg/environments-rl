from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

class DangerousTile(ExMiniGridEnv):
    """
    First GOAP Environment, empty 5x5 grid with ONE dangerous Tile
    """

    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            #Max speed
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

        # Place a safety concern
        self.place_obj(self._rand_int(0, width - 2), self._rand_int(0, height - 2), SafetyHazard())

        self.mission = "get to the green goal square"

class DangerousTile8x8(DangerousTile):
    def __init__(self):
        super().__init___(size=8)

register(
    id='MiniGrid-DangTile-6x6-v0',
    entry_point='gym_minigrid.envs:DangerousTile6x6'
)

register(
    id='MiniGrid-DangTile-8x8-v0',
    entry_point='gym_minigrid.envs:DangerousTile'
)