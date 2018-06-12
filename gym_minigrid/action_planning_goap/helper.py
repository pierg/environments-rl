from .planner import ObservationParser, ActionPlanner, reconstruct_path, CellState
from .goals import *
import copy


def run(current_obs, direction, goals):
    """
    Runs the planner
    :param current_obs: obs as created by decoding the grid
    :param direction: Direction to which the agent points
    :param goals: List of goals, the lower the index the highest priority
    :return: plan containing the actions
    """
    parser = ObservationParser(current_obs, direction)
    current_cell = parser.get_current_cell()
    current_cell_state = CellState(current_cell, direction)
    planner = ActionPlanner(current_cell_state)

    goal_cell = None

    for goal in goals:

        if goal == goal_turn:
            if direction == StateEnum.orientation_east.value:
                goal_cell = planner.graph.find_state(((StateEnum.orientation_west, True),))
                break
            elif direction == StateEnum.orientation_west.value:
                goal_cell = planner.graph.find_state(((StateEnum.orientation_east, True),))
                break
            elif direction == StateEnum.orientation_north.value:
                goal_cell = planner.graph.find_state(((StateEnum.orientation_south, True),))
                break
            elif direction == StateEnum.orientation_south.value:
                goal_cell = planner.graph.find_state(((StateEnum.orientation_north, True),))
                break

        goal_list = create_goals(goal, [])
        while goal_cell is None and goal_list:
            goal_cell = planner.graph.find_state(goal_list.pop())
            if goal_cell == current_cell_state.tuple():
                goal_cell = None
        if goal_cell is not None:
            break

    if goal_cell is None:
        #  raise ValueError('No goal found in graph!')
        return [], None


    if goal_cell == current_cell_state.tuple():
        raise ValueError('Trying to create a plan for the current state!')
    came_from, cost_so_far = planner.plan(current_cell_state.tuple(), goal_cell)
    action_stack = reconstruct_path(came_from, goal_cell, current_cell_state.tuple())

    return (action_stack, goal_cell)


def create_goals(states, result):

    if tuple(states) not in result:
        if states:
            result.append(tuple(states))
        for state in states:
            states_copy = copy.copy(states)
            states_copy.remove(state)
            create_goals(states_copy, result)
        result.sort(key=len)
        return result

    if not states:
        result.sort(key=len)
        return result


