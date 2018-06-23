from queue import PriorityQueue
from .obs_parser import ObservationParser, StateEnum, State
from .states import CellState
from .action import Action
from typing import Tuple, List, Dict, TypeVar
from .goals import goal_green_square

Coordinates = Tuple[int, int]

State = Tuple[StateEnum, ...]
CellState_tuple = Tuple[State, Coordinates]


class Graph:
    """
    Graph creates a graph where every node is a cellState and every action is an edge
    Just like GOAP wants us to do.
    """
    def __init__(self):
        """
        self.edges contains a dict with the following:
            As keys it has tupled cellStates (Nodes)
            As values it has the cellStates connected to the key cellState and the action that connects them
        """

        self.edges: Dict[Tuple[CellState_tuple, List[Tuple[CellState_tuple, Action]]]] = dict()
        self.updated = dict()

    def update(self, cell_state: CellState):
        """
        Populates the graph by applying all possible actions to cell_state and storing the
        resulting nodes and actions.
        :param cell_state: Node whose edges will be created
        :return:
        """
        current = cell_state
        current_tuple = tuple()

        """
         If the goal is orientation agnostic it should not contain the orientation states.
         Because if it does then the planner will make a plan to go to the goal and turn after reaching it.
         This extra action makes the plan hard to follow and to know when it has ended.
         
         In this case we only check for goal_green_square but ideally you should have a method that does this
         for all the goals that are orientation agnostic.
        """

        if goal_green_square[0] in tuple(current.states.items()):
            current_tuple = self.node_without_orientation(current.tuple())
        else:
            current_tuple = current.tuple()

        if current_tuple not in self.edges:
            actions = current.get_available_actions()  #  Find all cell states that are connected to current with an action
            self.edges[current_tuple] = []
            for action in actions:
                next_state = current.apply_action(action)
                if goal_green_square[0] in tuple(next_state.states.items()):
                    node = self.node_without_orientation(next_state.tuple())
                else:
                    node = next_state.tuple()
                self.edges[current_tuple].append((node, action))
                self.update(next_state)

    def neighbors(self, cell_state: Tuple[Tuple[StateEnum, bool]]) -> List[Tuple[Tuple[State, Coordinates], Action]]:
        """
        :param cell_state: node whose neighbours you want
        :return: All the nodes connected to cell_state only by one action
        """
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
        """
        Searches the graph for a cellState that contains all the states present in goal_state.
        Usually this is used when you want to know which cell to find as goal
        :param goal_states: States to look for in the graph
        :return: Cell that contains all of the states present in goal_states, If it doesn't exist then returns None
        """
        states_total = len(goal_states)
        for node in self.edges.keys():
            states_met = 0
            for state in goal_states:
                if state in node[0]:
                    states_met += 1
            if states_met == states_total:
                    return node
        return None

    def node_without_orientation(self, node):
        """
        Takes away the orientation StateEnums from a node
        :param node: node to take away the orientation StateEnums from
        :return: node without orientation StateEnum
        """
        orientations = [StateEnum.orientation_south,
                        StateEnum.orientation_north,
                        StateEnum.orientation_east,
                        StateEnum.orientation_west]
        result = []
        for state, value in node[0]:
            if state in orientations:
                continue
            else:
                result.append((state, value))

        return tuple(result), node[1]


def reconstruct_path(came_from, goal, start):
    """
    Returns the action stack that will take the agent from start to goal
    :param came_from: Dict containing paths
    :param goal: Goal cellState
    :param start: Starting cellState
    :return:
    """
    current = came_from[goal]
    path = []
    while current[0] != start:
        path.append(current[1].name)
        current = came_from[current[0]]
    path.append(current[1].name)
    return path


class ActionPlanner:
    """
    The action planner initializes the graph and creates plans
    """
    def __init__(self, current_cell_state: CellState):
        self.graph = Graph()
        self.graph.update(current_cell_state)

    @staticmethod
    def heuristic(start: CellState_tuple, goal: CellState_tuple):
        """
        GOAP: "The heuristic distance can be calculated as the sum of the unsatisfied properties of the goal state."

        This doesn't make sense in the grid world because you could just use the coordinates to
        calculate the distance from the current cell to the desired cell and it would be more accurate.

        The unsatisfied properties of the goal state in the grid world don't say how far you are from the goal,
        these properties can all be completely different from one step to the next.

        However, because this is a GOAP implementation we do it the GOAP way.

        :return: int containing the amount of unsatisfied properties of the goal state present in start
        """
        counter: int = 0
        for state in goal[0]:
            if state not in start[0]:
                    counter += 1
        return counter

    def plan(self, start_state: State, goal_state: State):
        """
        A* search algorithm
        :param start_state: starting state (must be present in the graph)
        :param goal_state: goal state (must be present in the graph)
        :return: dictionary containing paths and another dictionary containing the costs
        """
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

            for next_state, action in self.graph.neighbors(current):
                new_cost = cost_so_far[current] + self.graph.cost(current, next_state)
                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    priority = new_cost + self.heuristic(goal_state, next_state)
                    frontier.put(next_state, priority)
                    came_from[next_state] = (current, action)

        return came_from, cost_so_far


