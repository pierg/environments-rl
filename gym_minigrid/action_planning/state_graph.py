from .action_wrapper import *
from .states import world_states
from .obs_parser import *

class StateGraph:

    def __init__(self):
        self.edges = {}



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
                if new_state in self.edges:
                    self.edges.get(new_state).append(action)
                else:
                    self.edges[new_state] = [action]

    def neighbors(self,state):
        return self.edges[state]




