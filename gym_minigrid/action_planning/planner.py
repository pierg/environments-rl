from .graph import *
from queue import PriorityQueue
from .obs_parser import *
from .goals import *
import numpy as np

class ActionPlanner:

    def plan(self, obs):
        current_state = ObservationParser().get_current_state(obs)
        goal_state = move_away_from_danger

        graph = Graph()
        graph.updateGraph(current_state)

        plan, cost = self.action_planner(graph, tuple(current_state), tuple(goal_state))

        return 1



    def heuristic(node1:Node, node2:Node):
        counter = 0
        for state1 in node1.states:
            for state2 in node2.states:
                for property1 in state1:
                    for property2 in state2:
                        if property1.property == property2.property:
                            if property1.value != property2.value:
                                counter = counter + 1
        return counter

    def action_planner(self, graph, starting_state, goal_state):
        self.graph = graph
        self.graph.updateGraph(starting_state)

        frontier = PriorityQueue()
        frontier.put(goal_state,0)
        came_from = {}
        cost_so_far = {}
        came_from[goal_state] = None
        cost_so_far[goal_state] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == starting_state:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + self.graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(starting_state, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far