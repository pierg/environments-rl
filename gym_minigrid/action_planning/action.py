from .obs_parser import Cell, StateEnum
from gym_minigrid.extendedminigrid import ExMiniGridEnv
from typing import Tuple, TypeVar


class Action:

    def __init__(self, name: ExMiniGridEnv.Actions, current_cell: Cell, orientation: StateEnum):
        self.name: ExMiniGridEnv.Actions = name
        self.preconditions: Tuple[Tuple[StateEnum, bool]] = tuple()
        self.effects: Tuple[Tuple[StateEnum, bool]] = tuple()
        self.cost: int = 1

        if name == ExMiniGridEnv.Actions.forward:
            if orientation == StateEnum.orientation_north and current_cell.north_cell is not None:
                self.effects = current_cell.north_cell.states
                self.preconditions = ((StateEnum.north_is_safe, True),
                                      (StateEnum.north_is_clear, True),
                                      (StateEnum.orientation_north, True))
            elif orientation == StateEnum.orientation_south and current_cell.south_cell is not None:
                self.effects = current_cell.south_cell.states
                self.preconditions = ((StateEnum.south_is_safe, True),
                                      (StateEnum.front_is_clear, True),
                                      (StateEnum.orientation_south, True))
            elif orientation == StateEnum.orientation_west and current_cell.west_cell is not None:
                self.effects = current_cell.west_cell.states
                self.preconditions = ((StateEnum.west_is_safe, True),
                                      (StateEnum.west_is_clear, True),
                                      (StateEnum.orientation_west, True))
            elif orientation == StateEnum.orientation_east and current_cell.east_cell is not None:
                self.effects = current_cell.east_cell.states
                self.preconditions = ((StateEnum.east_is_safe, True),
                                      (StateEnum.east_is_clear, True),
                                      (StateEnum.orientation_east, True))

        elif name == ExMiniGridEnv.Actions.left:
            if orientation == StateEnum.orientation_north and current_cell.north_cell is not None:
                self.preconditions = ((StateEnum.west_is_clear, True),
                                      (StateEnum.west_is_safe, True),
                                      (StateEnum.orientation_north, True))
                self.effects = ((StateEnum.orientation_west, True), (StateEnum.orientation_north, False))
            elif orientation == StateEnum.orientation_south and current_cell.south_cell is not None:
                self.preconditions = ((StateEnum.east_is_clear, True),
                                      (StateEnum.east_is_safe, True),
                                      (StateEnum.orientation_south, True))
                self.effects = ((StateEnum.orientation_east, True), (StateEnum.orientation_south, False))
            elif orientation == StateEnum.orientation_west and current_cell.west_cell is not None:
                self.preconditions = ((StateEnum.south_is_clear, True),
                                      (StateEnum.south_is_safe, True),
                                      (StateEnum.orientation_west, True))
                self.effects = ((StateEnum.orientation_south, True), (StateEnum.orientation_west, False))
            elif orientation == StateEnum.orientation_south and current_cell.east_cell is not None:
                self.preconditions = ((StateEnum.north_is_clear, True),
                                      (StateEnum.north_is_safe, True),
                                      (StateEnum.orientation_east, True))
                self.effects = ((StateEnum.orientation_north, True), (StateEnum.orientation_east, False))

        elif name == ExMiniGridEnv.Actions.right:
            if orientation == StateEnum.orientation_north:
                self.preconditions = (
                    (StateEnum.east_is_clear, True),
                    (StateEnum.east_is_safe, True),
                    (StateEnum.orientation_north, True))
                self.effects = ((StateEnum.orientation_east, True), (StateEnum.orientation_north, False))
            elif orientation == StateEnum.orientation_south:
                self.preconditions = ((StateEnum.west_is_clear, True),
                                      (StateEnum.east_is_safe, True),
                                      (StateEnum.orientation_south, True))
                self.effects = ((StateEnum.orientation_east, True), (StateEnum.orientation_south, False))
            elif orientation == StateEnum.orientation_west:
                self.preconditions = ((StateEnum.north_is_clear, True),
                                      (StateEnum.north_is_safe, True),
                                      (StateEnum.orientation_west, True))
                self.effects = ((StateEnum.orientation_north, True), (StateEnum.orientation_west, False))
            elif orientation == StateEnum.orientation_east:
                self.preconditions = ((StateEnum.south_is_clear, True),
                                      (StateEnum.south_is_safe, True),
                                      (StateEnum.orientation_east, True))
                self.effects = ((StateEnum.orientation_south, True), (StateEnum.orientation_east, False))
        
        elif name == ExMiniGridEnv.Actions.turnaround:
            self.cost = 2
            if orientation == StateEnum.orientation_north:
                self.preconditions = (
                    (StateEnum.south_is_clear, True),
                    (StateEnum.south_is_safe, True),
                    (StateEnum.orientation_north, True))
                self.effects = ((StateEnum.orientation_south, True), (StateEnum.orientation_north, False))
            elif orientation == StateEnum.orientation_south:
                self.preconditions = (
                    (StateEnum.north_is_clear, True),
                    (StateEnum.north_is_safe, True),
                    (StateEnum.orientation_south, True)
                )
                self.effects = ((StateEnum.orientation_north, True), (StateEnum.orientation_south, False))
            elif orientation == StateEnum.orientation_west:
                self.preconditions = (
                    (StateEnum.east_is_clear, True),
                    (StateEnum.east_is_safe, True),
                    (StateEnum.orientation_west, True))
                self.effects = ((StateEnum.orientation_east, True), (StateEnum.orientation_west, False))
            elif orientation == StateEnum.orientation_east:
                self.preconditions = ((StateEnum.west_is_clear, True),
                                      (StateEnum.west_is_safe, True),
                                      (StateEnum.orientation_east, True))
                self.effects = ((StateEnum.orientation_west, True), (StateEnum.orientation_east, False))

    Action = TypeVar('Action')

    @staticmethod
    def get_possible_actions(orientation: StateEnum, cell: Cell) -> Tuple[Action, ...]:
        if cell is not None:
            if cell.is_clear:
                actions = []
                for action_name in ExMiniGridEnv.Actions:
                    actions.append(Action(action_name, cell, orientation))
                return tuple(actions)

        return ()

    def __lt__(self, other):
        return self.cost < other.cost
