from queue import PriorityQueue
from .obs_parser import ObservationParser, StateEnum, State
from .states import CellState
from .action import Action
from typing import Tuple, List, Dict, TypeVar

Coordinates = Tuple[int, int]


class Graph:
    def __init__(self):
        """
        self.edges contains a dict with the following:
            As keys it has cellStates
            As values it has lists containing pairs of cellStates and the action taken to reach them from the key
        """

        self.edges: Dict[Tuple[Tuple[StateEnum, ...], Coordinates], List[Tuple[Tuple[Tuple[StateEnum, ...], Coordinates], Action]]] = dict()
        self.updated = dict()

    def update(self, cell_state: CellState):
        current = cell_state
        if current.tuple() not in self.edges:
            actions = current.get_available_actions()  #  Find all cell states that are connected to current with an action
            self.edges[current.tuple()] = []
            for action in actions:
                next_state = current.apply_action(action)
                self.edges[current.tuple()].append((next_state.tuple(), action))
                self.update(next_state)

    def neighbors(self, cell_state: Tuple[Tuple[StateEnum, bool]]) -> List[Tuple[Tuple[State, Coordinates], Action]]:
        if cell_state is not None:
            if (StateEnum.current_is_clear, True) in cell_state[0]:  # Walls lead nowhere thus they have no neighbours
                return self.edges[cell_state]
        return [()]

    def cost(self, start: State, goal: State) -> int:
        """
        :return: action cost between two neighbor CellStates, if they are not neighbours return -1
        """
        neighbor_list: List[Tuple[CellState, Action]] = self.edges[start]
        for state_action_tuple in neighbor_list:
            if state_action_tuple[0] is goal:
                return state_action_tuple[1].cost
        return -1

    def find_state(self, goal_states: State):
        states_total = len(goal_states)
        for node in self.edges.keys():
            states_met = 0
            for state in goal_states:
                if state in node[0]:
                    states_met += 1
            if states_met == states_total:
                return node
        return None


def reconstruct_path(came_from, goal, start):
    current = came_from[goal]
    path = []
    while current[0] != start:
        path.append(current[1].name)
        current = came_from[current[0]]
    path.append(current[1].name)
    return path


class ActionPlanner:

    def __init__(self, current_cell_state: CellState):
        self.graph = Graph()
        self.graph.update(current_cell_state)

    @staticmethod
    def heuristic(start: CellState, goal: CellState):
        """
        The heuristic distance can be calculated as the sum of the unsatisfied properties of the goal state.
        :return: int containing the amount of unsatisfied properties of the goal state present in start
        """
        counter: int = 0
        for goal_state_name, goal_state_value in goal.states.items():
            if goal_state_name in start.states:
                if start.states[goal_state_name] is not goal_state_value:
                    counter += 1
            else:
                counter += 1
        return counter

    def plan(self, start_state: State, goal_state: State):
        frontier = PriorityQueue()
        frontier.put(start_state, 0)
        came_from: Dict[State, (State, Action)] = dict()
        cost_so_far: Dict[State, int] = dict()
        came_from[start_state] = (None, None)
        cost_so_far[start_state] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal_state:
                break

            for next_state_action_tuple in self.graph.neighbors(current):
                new_cost = cost_so_far[current] + self.graph.cost(current, next_state_action_tuple[0])
                if next_state_action_tuple[0] not in cost_so_far or new_cost < cost_so_far[next_state_action_tuple[0]]:
                    cost_so_far[next_state_action_tuple[0]] = new_cost
                    priority = new_cost
                    frontier.put(next_state_action_tuple[0], priority)
                    came_from[next_state_action_tuple[0]] = (current, next_state_action_tuple[1])

        return came_from, cost_so_far


