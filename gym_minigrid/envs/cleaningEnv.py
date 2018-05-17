from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

class CleaningEnv(ExMiniGridEnv):

    def __init__(self, size=12):
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

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        #Place dirt
        dirt = Dirt()
        x, y = self._rand_pos(2, width-2, 2, height - 2)
        # a dirt pattern need the grid and the position of the object to clean the case ( pass to Dirt at None )
        dirt.get_grid(self.grid,(x,y))
        self.grid.set(x, y, dirt)

        #Place Vase
        x2, y2 = self._rand_pos(2, width - 2, 2, height - 2)
        while (x2,y2) == (x,y) :
            x2, y2 = self._rand_pos(2, width - 2, 2, height - 2)
        vase = Vase()
        # a vase pattern need the greed and the position to change on dirt if the agent
        vase.grid(self.grid,(x2,y2))
        self.grid.set(x2, y2, vase)

        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "Clean all dirt"

register(
    id='MiniGrid-CleaningEnv-12x12-v0',
    entry_point='gym_minigrid.envs:CleaningEnv'
)