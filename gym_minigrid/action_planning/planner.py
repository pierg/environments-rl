from .states import *


class Node:
    def __init__(self):
        self.neighbors: Tuple(WorldState, Tuple(Action))


class Graph:
    def __init__(self):
        self.edges: Dict[Action, WorldState] = {}

    def update(self, current_state: WorldState):
        available_actions = current_state.get_available_actions()
        for action in available_actions:
            self.edges[action] = current_state.apply_action(action)

