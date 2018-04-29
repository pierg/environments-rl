
class Node:

    def __init__(self):
        self.edges = []
        self.states = []

    def __init__(self,state):
        self.edges = []
        self.states = state

    def add_edge(self, edge) -> bool:
        if edge not in self.edges:
            self.edges.append(edge)
            return True
        return False
