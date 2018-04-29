from .action import *
from .state_property import *
from .node import *

class Graph:
    def __init__(self):
        self.nodes = []

    def updateGraph(self, current_state: list):
        available_actions = Action.availableActions(current_state)
        if current_state not in self.nodes:
            current_state_node = Node(current_state)
            for edge in available_actions:
                current_state_node.add_edge(edge)
            self.nodes.append(current_state_node)

        for action in available_actions:
            node = Node(Action.getStateAfterAction(current_state, action))
            if node not in self.nodes:
                self.nodes.append(node)
            node.add_edge(action)

    def neighbors(self, node : Node) -> tuple:
        neighbors = []
        for graph_node in self.nodes:
            if set(node.states) == set(graph_node.states):
                for edge in graph_node.edges:
                    neighbors.append(Action.getStateAfterAction(node.states, edge))
        return tuple(neighbors)



    def cost(self, node1 : Node, node2: Node) -> int:
        return 1