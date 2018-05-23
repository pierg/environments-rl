from .planner import ObservationParser, ActionPlanner, reconstruct_path, CellState, State, StateEnum
import copy


def run(current_obs, direction, goal):
    goals = create_goals(goal, [])

    print(goals)

    parser = ObservationParser(current_obs, direction)
    current_cell = parser.get_current_cell()
    current_cell_state = CellState(current_cell, direction)
    planner = ActionPlanner(current_cell_state)

    goal_cell = None
    while goal_cell is None and goals:
        goal_cell = planner.graph.find_state(goals.pop())
    if goal_cell is None:
        raise ValueError('Goal state not found in graph!')
        # return []
    if goal_cell == current_cell_state.tuple():
        raise ValueError('Trying to create a plan for the current state!')
    came_from, cost_so_far = planner.plan(current_cell_state.tuple(), goal_cell)
    action_stack = reconstruct_path(came_from, goal_cell, current_cell_state.tuple())
    return action_stack


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


