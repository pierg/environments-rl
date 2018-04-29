from .action_wrapper import *
from .states import world_states
from .obs_parser import *
import json

class StateGraph:

    def __init__(self):
        self.edges={}
        # has as key a string which is a json dump of the state dictionary



    def updateGraph(self, current_state: dict):
        """
        updates the Graph with the current state, this needs to be executed everytime the
        current state changes
        :param current_state:
        :return: none
        """
        aw = ActionWrapper()
        actions = [aw.action(0),
                   aw.action(1),
                   aw.action(2),
                   aw.action(3),
                   aw.action(4),
                   aw.action(5),
                   aw.action(6)]

        for action in actions:
            preconditions_total = len(action.preconditions)
            preconditions_met = 0

            for k, v in action.preconditions.items():
                if (current_state[k] == v):
                    preconditions_met = preconditions_met + 1

            #Add this action to the graph
            if preconditions_met == preconditions_total:
                # create new state with postconditions
                new_state = current_state.copy()
                for k, v in action.effects.items():
                    new_state[k] = v

                #add the action to the graph
                if json.dumps(new_state) in self.edges:
                    self.edges[json.dumps(new_state)].append(action)
                else:
                    self.edges[json.dumps(new_state)] = [action]


    def actionEffects(self, state, action):
        new_state = state.copy()
        for k, v in action.effects.items():
            new_state[k] = v
        return new_state


    def neighbors(self,state : str) -> list:

        if(state not in self.edges):
            state_attribute_parsed = json.loads(state)
            requirements_total = len(state_attribute_parsed)
            requirements_met = 0

            for state_str, actions in self.edges.items():
                state_parsed = json.loads(state_str)

                edges = []

                for k, v in state_attribute_parsed.items():
                    if state_parsed[k] == v:
                        requirements_met += 1
                    if requirements_met == requirements_total:
                        edges.append(state_str)

            return edges

        edges = []
        for action in self.edges[state]:
            edges.append(json.dumps(action.effects))

        return edges


    def cost(self, state1, state2):
        return 1
'''
        if state1 not in self.edges:
            state1_parsed = json.loads(state1)

        for action in self.edges[state1]:
            if StateGraph.actionEffects(state1, action) == state2:
                return action.cost
            else:
                return 0
'''
