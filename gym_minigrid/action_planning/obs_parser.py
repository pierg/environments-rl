from gym_minigrid.extendedminigrid import *
from typing import Tuple, List
from enum import IntEnum


class StateEnum(IntEnum):
    orientation_east = 0
    orientation_south = 1
    orientation_west = 2
    orientation_north = 3
    north_is_safe = 4
    north_is_clear = 5
    south_is_safe = 6
    south_is_clear = 7
    east_is_safe = 8
    east_is_clear = 9
    west_is_safe = 10
    west_is_clear = 11
    current_is_clear = 12
    current_is_safe = 13
    front_is_safe = 14
    front_is_clear = 15
    left_is_safe = 16
    left_is_clear = 17
    right_is_safe = 18
    right_is_clear = 19


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
        agent_pos_x = int(AGENT_VIEW_SIZE - 1)
        agent_pos_y = int(AGENT_VIEW_SIZE / 2)
        self.parse_observation(agent_pos_x, agent_pos_y)
        self.map_cells()

    def parse_observation(self, pos_x: int, pos_y: int):
        """
        Creates a map by flood-filling the observation
        :return: 2D tuple with cells representing the world
        """
        if self.parsed_observation[pos_x][pos_y] is None:
            cell = Cell(self.observation[pos_x][pos_y])
            # Check if the cell is clear and safe and set it, needs improvement
            if isinstance(cell.type, WorldObj) and isinstance(cell.type, Wall):
                cell.is_clear = False
            if isinstance(cell.type, WorldObj) and isinstance(cell.type, Unsafe):
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
                    if self.orientation == StateEnum.orientation_north:
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.south_cell = self.parsed_observation[x+1][y]
                        if x > 0:
                            current_cell.north_cell = self.parsed_observation[x-1][y]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.east_cell = self.parsed_observation[x][y+1]
                        if y > 0:
                            current_cell.west_cell = self.parsed_observation[x][y-1]
                    elif self.orientation == StateEnum.orientation_south:
                        if x > 0:
                            current_cell.west_cell = self.parsed_observation[x-1][y]
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.east_cell = self.parsed_observation[x+1][y]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.north_cell = self.parsed_observation[x][y+1]
                        if y > 0:
                            current_cell.south_cell = self.parsed_observation[x][y-1]
                    elif self.orientation == StateEnum.orientation_west:
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.east_cell = self.parsed_observation[x+1][y]
                        if x > 0:
                            current_cell.west_cell = self.parsed_observation[x-1][y]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.north_cell = self.parsed_observation[x][y+1]
                        if y > 0:
                            current_cell.south_cell = self.parsed_observation[x][y-1]
                    elif self.orientation == StateEnum.orientation_east:
                        if x > 0:
                            current_cell.east_cell = self.parsed_observation[x-1][y]
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.west_cell = self.parsed_observation[x+1][y]
                        if y > 0:
                            current_cell.north_cell = self.parsed_observation[x][y-1]
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.south_cell = self.parsed_observation[x][y+1]

                    states = dict()
                    states[StateEnum.current_is_clear] = True if current_cell.is_clear else False
                    states[StateEnum.current_is_safe] = True if current_cell.is_safe else False
                    if current_cell.west_cell is not None:
                        states[StateEnum.west_is_clear] = True if current_cell.west_cell.is_clear else False
                        states[StateEnum.west_is_safe] = True if current_cell.west_cell.is_safe else False
                    if current_cell.east_cell is not None:
                        states[StateEnum.east_is_clear] = True if current_cell.east_cell.is_clear else False
                        states[StateEnum.east_is_safe] = True if current_cell.east_cell.is_safe else False
                    if current_cell.north_cell is not None:
                        states[StateEnum.north_is_clear] = True if current_cell.north_cell.is_clear else False
                        states[StateEnum.north_is_safe] = True if current_cell.north_cell.is_safe else False
                    if current_cell.south_cell is not None:
                        states[StateEnum.south_is_clear] = True if current_cell.south_cell.is_clear else False
                        states[StateEnum.south_is_safe] = True if current_cell.south_cell.is_safe else False
                    current_cell.states = tuple(states.items())

    def get_current_cell(self) -> 'Cell':
        agent_pos_x = int(AGENT_VIEW_SIZE - 1)
        agent_pos_y = int(AGENT_VIEW_SIZE / 2)
        return self.parsed_observation[agent_pos_x][agent_pos_y]


class Cell:
    def __init__(self, cell_type):
        self.north_cell: Cell = None
        self.south_cell: Cell = None
        self.east_cell: Cell = None
        self.west_cell: Cell = None
        self.is_clear: bool = True  # These change when the cell is created
        self.is_safe: bool = True
        self.type = cell_type
        self.states: Tuple[Tuple[StateEnum, bool]] = tuple()
