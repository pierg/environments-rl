from .action import *
from .state_property import *
from .node import *

class Graph:
    def __init__(self):
        self.nodes = []

    def updateGraph(self, current_state: list):
        available_actions = Action.availableActions(current_state)
        for action in available_actions:
            node = Node(Action.getStateAfterAction(current_state, action))
            if node not in self.nodes:
                node.add_edge(action)
                self.nodes.append(node)
            node.add_edge(action)

    def neighbors(self, node : Node) -> list:
        neighbors = []
        if node in self.nodes:
            for edge in node.edges:
                neighbors.append(Action.getStateAfterAction(node,edge))
        return neighbors

    def cost(self, node1 : Node, node2: Node) -> int:
        return 1