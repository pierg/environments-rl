from gym_minigrid.extendedminigrid import *
from typing import Tuple, List, Dict
from enum import IntEnum, unique


@unique
class StateEnum(IntEnum):
    """
    State enums contain all possible states available in your world.
    If your agent carries something or is in a specific state, that state should be added here
    """

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
    current_is_goal = 14
    north_is_none = 15
    south_is_none = 16
    west_is_none = 17
    east_is_none = 18


"""
    A State is a tuple of a stateEnum and a boolean.
    for example, (east_is_clear, True) 
"""
State = Tuple[StateEnum, bool]

AGENT_GRID_LOCATION = 2


class ObservationParser:
    """"
        obs_parser takes agents observation and translates it to world states.
        Output is a current state visible to the agent
    """
    """
    Orientation:
        East = 0
        South = 1
        West = 2
        North = 3
    """

    def __init__(self, obs, orientation):
        """
        Calls all the methods that parses the current observation. We need to know the orientation
        because the observation depends on the agent's orientation. We then compensate for it and create a
        map with objective orientations. For example, the "north" of a cell will be the actual north instead of being
        linked to wherever the agent points towards.

        :param obs: Observation as created by gym_minigrid
        :param orientation: int containing information on which way the agent looks at
        """
        observation = []
        self.orientation = orientation
        #  Converts the orientation from being a list into a 2D array. Easier to work with.
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
        Parses the map by flood-filling the observation.
        The flood fill starts at the place the agent is standing because we only care about parsing to places the
        agent can reach.

        :param pos_x: Number of column the agent is located at
        :param pos_y: Number of row the agent is at
        :return: New observation containing cell classes, only filled with their own information
        """
        if self.parsed_observation[pos_x][pos_y] is None:
            cell = Cell(self.observation[pos_x][pos_y])
            cell.x = pos_x
            cell.y = pos_y
            # Check if the cell is clear and safe and set it.
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
        """
        Provides the rest of the properties to the cells in self.parsed_observation.
        :return:
        """
        for x in range(0, AGENT_VIEW_SIZE):
            for y in range(0, AGENT_VIEW_SIZE):
                if self.parsed_observation[x][y] is not None:
                    current_cell = self.parsed_observation[x][y]
                    #  Putting pointers to the neighbouring cells
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
                        if y < AGENT_VIEW_SIZE - 1:
                            current_cell.west_cell = self.parsed_observation[x][y+1]
                        if y > 0:
                            current_cell.east_cell = self.parsed_observation[x][y-1]
                        if x < AGENT_VIEW_SIZE - 1:
                            current_cell.north_cell = self.parsed_observation[x+1][y]
                        if x > 0:
                            current_cell.south_cell = self.parsed_observation[x-1][y]
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

                    #  Translates the information about the neighboring cells into states

                    states = current_cell.states
                    states[StateEnum.current_is_clear] = True if current_cell.is_clear else False
                    states[StateEnum.current_is_safe] = True if current_cell.is_safe else False
                    if current_cell.west_cell is not None:
                        states[StateEnum.west_is_none] = False
                        states[StateEnum.west_is_clear] = True if current_cell.west_cell.is_clear else False
                        states[StateEnum.west_is_safe] = True if current_cell.west_cell.is_safe else False
                    else:
                        states[StateEnum.west_is_none] = True

                    if current_cell.east_cell is not None:
                        states[StateEnum.east_is_none] = False
                        states[StateEnum.east_is_clear] = True if current_cell.east_cell.is_clear else False
                        states[StateEnum.east_is_safe] = True if current_cell.east_cell.is_safe else False
                    else:
                        states[StateEnum.east_is_none] = True

                    if current_cell.north_cell is not None:
                        states[StateEnum.north_is_none] = False
                        states[StateEnum.north_is_clear] = True if current_cell.north_cell.is_clear else False
                        states[StateEnum.north_is_safe] = True if current_cell.north_cell.is_safe else False
                    else:
                        states[StateEnum.north_is_none] = True

                    if current_cell.south_cell is not None:
                        states[StateEnum.south_is_none] = False
                        states[StateEnum.south_is_clear] = True if current_cell.south_cell.is_clear else False
                        states[StateEnum.south_is_safe] = True if current_cell.south_cell.is_safe else False
                    else:
                        states[StateEnum.south_is_none] = True

                    states[StateEnum.current_is_goal] = True if isinstance(current_cell.type, Goal) else False

    def get_current_cell(self) -> 'Cell':
        """
        This is used in helper.py to get the starting point of all the plans.
        :return: Returns the cell where the agent stands
        """
        agent_pos_x = int(AGENT_VIEW_SIZE - 1)
        agent_pos_y = int(AGENT_VIEW_SIZE / 2)
        return self.parsed_observation[agent_pos_x][agent_pos_y]


class Cell:
    """
    Helper class used to make the transition from observation to usable information.
    Contains states that are only present in the environment and doesn't store states
    of the agent like orientation or what it is carrying.
    """
    def __init__(self, cell_type):
        self.north_cell: Cell = None
        self.south_cell: Cell = None
        self.east_cell: Cell = None
        self.west_cell: Cell = None
        self.is_clear: bool = True  # These change when the cell is created
        self.is_safe: bool = True
        self.type = cell_type
        self.states: Dict[StateEnum, bool] = dict()
        self.x: int = 0
        self.y: int = 0
