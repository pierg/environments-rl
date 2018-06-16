from queue import PriorityQueue

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

        self.random = self.config.action_planning.random_unsafe_obj

        self._create_grid(width, height)

    def _create_grid(self, width, height):
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
            self.create_random(width, height)

        else:
            self.grid.set(width - 4, height - 2, Unsafe())
            self.grid.set(width - 4, height - 3, Unsafe())
            self.grid.set(width - 4, height - 5, Unsafe())
            self.grid.set(width - 4, height - 6, Unsafe())
            self.grid.set(width - 4, height - 7, Unsafe())

            if not self.exists_safe_path((1, 1), (width-2, height-2)):
                print("No path found")

        self.mission = "get to the green goal square"

    def create_random(self, width, height):
        i = 0
        taken_cell = [(1, 1), (width - 2, height - 2)]

        while i < self.random:
            w = randint(1, width - 2)
            h = randint(1, height - 2)

            if (w, h) not in taken_cell:
                self.grid.set(w, h, Unsafe())
                taken_cell.append([w, h])
                i += 1

        if not self.exists_safe_path((1, 1), (width-2, height-2)):
            #print("No path found")
            self.grid = None
            self._create_grid(width, height)

    def exists_safe_path(self, start, finish):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == finish:
                return True
                break

            neighbors = []
            if current[0] > 0:
                if self.grid.get(current[0] - 1, current[1]) is None or\
                        self.grid.get(current[0] - 1, current[1]).type == 'goal':

                    neighbors.append((current[0]-1, current[1]))

            if current[1] > 0:
                if self.grid.get(current[0], current[1]-1) is None or\
                        self.grid.get(current[0], current[1]-1).type == 'goal':

                    neighbors.append((current[0], current[1]-1))

            if current[0] < self.grid.height - 1:
                if self.grid.get(current[0]+1, current[1]) is None or\
                        self.grid.get(current[0]+1, current[1]).type == 'goal':

                    neighbors.append((current[0]+1, current[1]))

            if current[1] < self.grid.width - 1:
                if self.grid.get(current[0], current[1]+1) is None or\
                        self.grid.get(current[0], current[1] + 1).type == 'goal':

                    neighbors.append((current[0], current[1]+1))

            for next in neighbors:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + abs(finish[0] - next[0]) + abs(finish[1] - next[1])
                    frontier.put(next, priority)
                    came_from[next] = current
        return False


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