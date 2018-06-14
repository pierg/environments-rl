from random import randrange
import sys
from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

from configurations import config_grabber as cg


class UnsafeMazeEnv(ExMiniGridEnv):

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

        maze_creator = MazeCreator(width, height)
        print(maze_creator)
        for row in maze_creator.maze:
            for detail in row:
                x, y = detail['coords']
                if detail['bottom_wall']:
                    if self.grid.get(x, y + 1) is None:
                        print("(" + str(x) + "," + str(y+1) + ")")
                        self.grid.set(x, y + 1, Unsafe())

                if detail['right_wall']:
                    if self.grid.get(x + 1, y) is None:
                        print("(" + str(x+1) + "," + str(y) + ")")
                        self.grid.set(x + 1, y, Unsafe())


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


class MazeCreator:

    def __init__(self, width, height):
        self.n_rows = int((height - 2))
        self.n_cols = int((width - 2))
        self.directions = {'east': 0, 'south': 1, 'west': 2, 'north': 3}
        self.maze = [[None] * self.n_rows for i in range(self.n_cols)]

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                self.maze[i][j] = {'bottom_wall': True, 'right_wall': True, 'visited': False}

        currCol = randrange(self.n_cols)
        currRow = randrange(self.n_rows)

        self._make_path(currRow, currCol)

    def _make_path(self, row, column, direction=None):
        self.maze[row][column]['visited'] = True
        #self.maze[row][column]['coords'] = ((row * 2) + 1, (column * 2) + 1)
        self.maze[row][column]['coords'] = (row + 1, column + 1)
        if direction == self.directions['north']:
            self.maze[row][column]['bottom_wall'] = False
        elif direction == self.directions['south']:
            self.maze[row - 1][column]['bottom_wall'] = False
        elif direction == self.directions['west']:
            self.maze[row][column]['right_wall'] = False
        elif direction == self.directions['east']:
            self.maze[row][column-1]['right_wall'] = False

        directions = []
        if row > 0:
            directions.append(self.directions['north'])
        if row < self.n_rows - 1:
            directions.append(self.directions['south'])
        if column > 0:
            directions.append(self.directions['west'])
        if column < self.n_cols - 1:
            directions.append(self.directions['east'])

        dir_len = len(directions)
        for i in range(dir_len):
            j = randrange(dir_len)
            directions[i], directions[j] = directions[j], directions[i]

        for direction in directions:
            if direction == self.directions['north']:
                if not self.maze[row-1][column]['visited']:
                    self._make_path(row-1, column, self.directions['north'])
            elif direction == self.directions['south']:
                if not self.maze[row+1][column]['visited']:
                    self._make_path(row+1, column, self.directions['south'])
            elif direction == self.directions['east']:
                if not self.maze[row][column+1]['visited']:
                    self._make_path(row, column+1, self.directions['east'])
            elif direction == self.directions['west']:
                if not self.maze[row][column-1]['visited']:
                    self._make_path(row, column-1, self.directions['west'])

    def __str__(self):
        """Return maze table in ASCII"""

        result = '.' + self.n_cols*'_.'
        result += '\n'

        for i in range(self.n_rows):
            result += '|'

            for j in range(self.n_cols):
                if i == self.n_rows-1 or self.maze[i][j]['bottom_wall']:
                    result += '_'
                else:
                    result += ' '
                if j == self.n_cols-1 or self.maze[i][j]['right_wall']:
                    result += '|'
                else:
                    result += '.'

            result += '\n'

        return result
