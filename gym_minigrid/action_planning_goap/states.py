from .obs_parser import Cell, StateEnum, State
from .action import Action
from typing import Dict, Tuple, List
from gym_minigrid.extendedminigrid import ExMiniGridEnv
import copy


class CellState:
    """
        CellState puts together the Cell with the orientation of the agent.
        In some sense it is more dynamic than the Cell because it changes
        depending on what the agent does.
    """

    def __init__(self, current_cell: Cell, orientation: StateEnum):
        """
        Creates a cellState, which is a cell with all the states that the agent might have
        :param current_cell: The cell being created as a cellState
        :param orientation:  The orientation of the agent as a StateEnum
        """
        self.states = dict(current_cell.states)
        self.cell = current_cell
        self.states[StateEnum.orientation_west] = False
        self.states[StateEnum.orientation_east] = False
        self.states[StateEnum.orientation_north] = False
        self.states[StateEnum.orientation_south] = False
        self.states[orientation] = True

    @staticmethod
    def get_orientation(states: Dict[StateEnum, bool]) -> StateEnum:
        if states[StateEnum.orientation_north]:
            return StateEnum.orientation_north
        elif states[StateEnum.orientation_south]:
            return StateEnum.orientation_south
        elif states[StateEnum.orientation_east]:
            return StateEnum.orientation_east
        elif states[StateEnum.orientation_west]:
            return StateEnum.orientation_west

    def get_available_actions(self) -> Tuple[Action, ...]:
        """
        Returns all possible actions that can take place in the current cellState
        :return: Actions whose prerequisites match the current cellState
        """
        resulting_worldstate = copy.deepcopy(self.states)
        possible_actions = Action.get_all_actions(self.get_orientation(self.states), self.cell)

        available_actions = []
        for action in possible_actions:

            preconditions_total = len(action.preconditions)
            preconditions_met = 0
            for precondition in action.preconditions:
                for state in resulting_worldstate.items():
                    if precondition == state:
                        preconditions_met += 1
            if preconditions_met == preconditions_total:
                available_actions.append(action)

        return tuple(available_actions)

    def apply_action(self, action: Action) -> 'CellState':
        """
        Applies an action to the current cellState and returns the result.
        An action is applied by first seeing if the action's preconditions exist in the current cellState
        And then cloning the current cellState but changing the states according to the action's effects.
        :param action: Action to be executed
        :return: Changed cellState
        """
        # First check if this worldstate has the preconditions for the action
        preconditions_met = 0
        for precondition_name, precondition_value in action.preconditions:
            if precondition_name in self.states and \
                    self.states[precondition_name] == precondition_value:
                preconditions_met += 1
            else:
                raise KeyError('Tried to apply action when preconditions where not met: ' + action.name.value)

        if action.name == ExMiniGridEnv.Actions.forward:
            orientation = self.get_orientation(self.states)
            if orientation == StateEnum.orientation_north and self.cell.north_cell is not None:
                return CellState(self.cell.north_cell, orientation)
            elif orientation == StateEnum.orientation_south and self.cell.south_cell is not None:
                return CellState(self.cell.south_cell, orientation)
            elif orientation == StateEnum.orientation_east and self.cell.east_cell is not None:
                return CellState(self.cell.east_cell, orientation)
            elif orientation == StateEnum.orientation_west and self.cell.west_cell is not None:
                return CellState(self.cell.west_cell, orientation)
            else:
                return CellState(self.cell, orientation)

        else:
            resulting_state = copy.deepcopy(self.states)
            # Create new cellState containing effects of action
            for effect_name, effect_value in action.effects:
                resulting_state[effect_name] = effect_value

            return CellState(self.cell, self.get_orientation(resulting_state))

    def tuple(self) -> Tuple[Tuple[StateEnum, ...], Tuple[int, int]]:
        """
        Returns the dict of states as a tuple, to be used when you need a hashable cellState
        :return: Tuple containing the individual states and coordinates of the cell
        """
        return tuple(self.states.items()), (self.cell.x, self.cell.y)
        #  return tuple(self.states.items())
