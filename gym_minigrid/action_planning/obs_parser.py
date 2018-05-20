from .states import *
from gym_minigrid.extendedminigrid import *
from typing import Tuple
""""
    obs_parser takes agents observation and translates it to world states.
    Output is a current state visible to the agent
"""

AGENT_GRID_LOCATION = 2


class ObservationParser:

    """
    Orientation:
        East = 0
        South = 1
        West = 2
        North = 3
    """

    def __init__(self, obs, orientation):
        observation = []
        self.orientation = orientation
        for x in range(0, AGENT_VIEW_SIZE):
            current_row = [None] * AGENT_VIEW_SIZE
            for y in range(0, AGENT_VIEW_SIZE):
                current_row[y] = obs.grid[(x*AGENT_VIEW_SIZE) + y]
            observation.append(tuple(current_row))
        self.observation = tuple(observation)

        self.parsed_observation: List[List[Cell]] = [[None] * AGENT_VIEW_SIZE for i in range(AGENT_VIEW_SIZE)]
        agent_pos_x = int(AGENT_VIEW_SIZE / 2)
        agent_pos_y = int(AGENT_VIEW_SIZE - 1)
        self.parse_observation(agent_pos_x, agent_pos_y)
        self.map_cells()

    def parse_observation(self, pos_x: int, pos_y: int):
        """
        Creates a map by flood-filling the observation
        :return: 2D tuple with cells representing the world
        """
        if self.parsed_observation[pos_x][pos_y] is None:
            cell = Cell(self.observation[pos_x][pos_y])
            cell.x = pos_x
            cell.y = pos_y
            # Check if the cell is clear and safe and set it, needs improvement
            if isinstance(cell.type, WorldObj) and isinstance(cell.type, Wall):
                cell.is_clear = False
            if isinstance(cell.type, WorldObj) and isinstance(cell.type, Hazard):
                cell.is_safe = False

            self.parsed_observation[pos_x][pos_y] = cell

            # If the tile is a wall, don't expand
            if cell.is_clear:

                if pos_y > 0:
                    self.parse_observation(pos_x, pos_y - 1)
                if pos_y < AGENT_VIEW_SIZE - 1:
                    self.parse_observation(pos_x, pos_y + 1)
                if pos_x > 0:
                    self.parse_observation(pos_x - 1, pos_y)
                if pos_x < AGENT_VIEW_SIZE - 1:
                    self.parse_observation(pos_x + 1, pos_y)

    def map_cells(self):
        for x in range(0, AGENT_VIEW_SIZE):
            for y in range(0, AGENT_VIEW_SIZE):
                if self.parsed_observation[x][y] is not None:
                    current_cell = self.parsed_observation[x][y]
                    if self.orientation == Orientation.north:
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.south_cell = self.parsed_observation[x+1][y]
                        if x > 0:
                            current_cell.north_cell = self.parsed_observation[x-1][y]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.east_cell = self.parsed_observation[x][y+1]
                        if y > 0:
                            current_cell.west_cell = self.parsed_observation[x][y-1]
                    elif self.orientation == Orientation.south:
                        if x > 0:
                            current_cell.west_cell = self.parsed_observation[x-1][y]
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.east_cell = self.parsed_observation[x+1][y]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.north_cell = self.parsed_observation[x][y+1]
                        if y > 0:
                            current_cell.south_cell = self.parsed_observation[x][y-1]
                    elif self.orientation == Orientation.west:
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.east_cell = self.parsed_observation[x+1][y]
                        if x > 0:
                            current_cell.west_cell = self.parsed_observation[x-1][y]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.north_cell = self.parsed_observation[x][y+1]
                        if y > 0:
                            current_cell.south_cell = self.parsed_observation[x][y-1]
                    elif self.orientation == Orientation.east:
                        if x > 0:
                            current_cell.east_cell = self.parsed_observation[x-1][y]
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.west_cell = self.parsed_observation[x+1][y]
                        if y > 0:
                            current_cell.north_cell = self.parsed_observation[x][y-1]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.south_cell = self.parsed_observation[x][y+1]

                    states = dict()
                    states[StateNameEnum.current_is_clear] = True if current_cell.is_clear else False
                    states[StateNameEnum.current_is_safe] = True if current_cell.is_safe else False
                    if current_cell.west_cell is not None:
                        states[StateNameEnum.west_is_clear] = True if current_cell.west_cell.is_clear else False
                        states[StateNameEnum.west_is_safe] = True if current_cell.west_cell.is_safe else False
                    if current_cell.east_cell is not None:
                        states[StateNameEnum.east_is_clear] = True if current_cell.east_cell.is_clear else False
                        states[StateNameEnum.east_is_safe] = True if current_cell.east_cell.is_clear else False
                    if current_cell.north_cell is not None:
                        states[StateNameEnum.north_is_clear] = True if current_cell.north_cell.is_clear else False
                        states[StateNameEnum.north_is_safe] = True if current_cell.north_cell.is_clear else False
                    current_cell.states = tuple(states)


class Cell:
    def __init__(self, cell_type):
        self.north_cell: Cell = None
        self.south_cell: Cell = None
        self.east_cell: Cell = None
        self.west_cell: Cell = None
        self.is_clear: bool = True  # These change when the cell is created
        self.is_safe: bool = True
        self.type = cell_type
        self.states: Tuple[StateNameEnum, bool]
        self.x = int
        self.y = int
