from .graph import *
from queue import PriorityQueue
from .obs_parser import *
from .goals import *
import numpy as np
import copy

class ActionPlanner:

    def plan(self, obs):
        current_state = ObservationParser().get_current_state(obs)
        goal_state = move_away_from_danger

        graph = Graph()
        graph.updateGraph(current_state)
        relevant_current_state = self.relevantTo(current_state, goal_state)

        came_from, cost = self.action_planner(graph, tuple(current_state), tuple(goal_state))

        list_of_nodes = []
        list_of_states = []
        for node_as_tuple in came_from:
            for state_property in node_as_tuple:
                list_of_states.append(state_property)
            list_of_nodes.append(Node(list_of_states))
            list_of_states = []

        came_from = list_of_nodes


        path = ActionPlanner.reconstruct_path(came_from, current_state, goal_state)

        # TODO for some reason this name (that is supposed to be a minigrid.action) is not recognized as an action
        
        return path.pop().name

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        came_from_changes = copy.deepcopy(came_from)
        start_changes = copy.deepcopy(start)
        goal_changes = copy.deepcopy(goal)
        start_changes = ActionPlanner.relevantTo(start_changes, goal_changes)

        actions = []

        for node in came_from_changes:
            goal_length = len(goal_changes)
            goal_counter = 0
            for edge in node.edges:
                for state in goal_changes:
                    for state_after_action in Action.getStateAfterAction(node.states, edge):
                        if state.property == state_after_action.property:
                            if state.value == state_after_action.value:
                                goal_counter = goal_counter + 1

                if(goal_counter == goal_length):
                    actions.append(edge)

        return actions






        return 1


    @staticmethod
    def heuristic(goal: tuple, current: tuple):
        goal_list = list(goal)
        current_list = list(current)
        counter = 0

        for goal_property in goal_list:
            for current_property in current_list:
                if goal_property.property == current_property.property:
                    if goal_property.value != current_property.value:
                        counter = counter + 1
        return counter

    def action_planner(self, graph, starting_state, goal_state):
        frontier = []
        frontier.append(starting_state)
        came_from = {}
        cost_so_far = {}
        came_from[starting_state] = None
        cost_so_far[starting_state] = 0

        while not len(frontier) == 0:
            current = frontier.pop()

            if current == goal_state:
                break

            for next in graph.neighbors(Node(list(current))):
                next = tuple(next)
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal_state, next)
                    frontier.append(next)
                    came_from[next] = list(current)

        return came_from, cost_so_far

    @staticmethod
    def relevantTo(start: list, goal: list):
        relevantProperties = []
        for state_property in start:
            for goal_property in goal:
                if state_property.property == goal_property.property:
                    relevantProperties.append(state_property)
        return relevantProperties
