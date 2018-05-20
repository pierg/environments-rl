from .obs_parser import *
from gym_minigrid.extendedminigrid import ExMiniGridEnv, Orientation
from typing import Tuple, TypeVar


class Action:

    def __init__(self, name: ExMiniGridEnv.Actions, orientation: Orientation, current_cell):
        self.name: ExMiniGridEnv.Actions = name
        self.preconditions: Tuple[Tuple[StateNameEnum, bool]] = current_cell.states
        self.effects: Tuple[Tuple[StateNameEnum, bool]]
        self.cost: int = 1

        if name == ExMiniGridEnv.Actions.forward:
            if orientation == Orientation.north:
                self.effects = current_cell.north_cell.states
            if orientation == Orientation.south:
                self.effects = current_cell.south_cell.states
            if orientation == Orientation.west:
                self.effects = current_cell.west_cell.states
            if orientation == Orientation.east:
                self.effects = current_cell.east_cell.states

        if name == ExMiniGridEnv.Actions.left:
            if orientation == Orientation.north:
                self.effects = current_cell.west_cell.states
            if orientation == Orientation.south:
                self.effects = current_cell.east_cell.states
            if orientation == Orientation.west:
                self.effects = current_cell.south_cell.states
            if orientation == orientation.east:
                self.effects = current_cell.north_cell.states

        if name == ExMiniGridEnv.Actions.right:
            if orientation == Orientation.north:
                self.effects = current_cell.east_cell.states
            if orientation == orientation.south:
                self.effects = current_cell.west_cell.states
            if orientation == orientation.west:
                self.effects = current_cell.north_cell.states
            if orientation == orientation.east:
                self.effects = current_cell.south_cell.states

    Action = TypeVar('Action')

    @staticmethod
    def get_possible_actions(orientation: Orientation, cell) -> Tuple[Action, ...]:
        actions = []
        for action_name in ExMiniGridEnv.Actions:
            actions.append(Action(action_name, orientation, cell))
        return tuple(actions)
