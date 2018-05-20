from .action import *
class Node:

    def __init__(self):
        self.edges = []
        self.states = []

    def __init__(self,state):
        self.edges = []
        self.states = state
        available_actions = Action.available_actions_for_state(self.states)
        for action in available_actions:
            self.add_edge(action)

    def add_edge(self, edge) -> bool:
        if edge not in self.edges:
            self.edges.append(edge)
            return True
        return False
