from .action import *
class Node:

    def __init__(self):
        self.edges = []
        self.states = []

    def __init__(self,state):
        self.edges = []
        self.states = state
        available_actions = Action.availableActions(self.states)
        for action in available_actions:
            self.add_edge(action)

    def add_edge(self, edge) -> bool:
        if edge not in self.edges:
            self.edges.append(edge)
            return True
        return False

    def connect(node1, node2):
        actions = Action.getAllPossibleActions()