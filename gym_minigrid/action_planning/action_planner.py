from queue import PriorityQueue
from .obs_parser import ObservationParser
from .goals import *
from gym_minigrid.extendedminigrid import ExMiniGridEnv
from .state_graph import *





class ActionPlanner:

    """"
         Action planner needs an implementation of A* where Nodes are
         states of the world and edges the actions between them.

         The cost of a node can be calculated as the sum of the costs of the actions
         that take the world to the state represented by the node.



         The heuristic distance can be calculated as the sum of the unstatisfied properties
         of the goal state.
    """
    def __init__(self):
        self.proposed_action = None

    print('works')



    def plan(self, obs):

        current_state = ObservationParser().get_current_state(obs)
        # how do we know the goal?
        goal_state = move_away_from_danger

        stateGraph = StateGraph()
        stateGraph.updateGraph(current_state)

        plan , cost = self.action_planner(stateGraph,current_state,goal_state)



        #TODO check if this works, maybe plan.get returns a list of actions isntead of an action
        return self.proposed_action
        #return 2

    def heuristic(x, y):
        """
        :param x: Starting world state
        :param y: World state to compare
        :return: The sum (ammount) of the unsatisfied properties of the goal state compared to the current state
        """
        i = 0


        for k, v in x.items():
            if y [k] != v:
                i= i + 1

        return i


    def action_planner(self, actions_graph, starting_state, goal_state):
        """
        :param actions_graph:  state_graph of possible actions and states
        :param starting_state: Starting state
        :param goal_state: Desired state
        :return: came_from, cost_so_far
        """

        goal_state = json.dumps(goal_state)
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



            for next_state in actions_graph.neighbors(current):
                new_cost = cost_so_far[current] + actions_graph.cost(current, next_state)
                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    #priority = new_cost + ActionPlanner().heuristic(starting_state, json.loads(next_state))
                    priority = 2
                    frontier.put(next_state,priority)
                    came_from[next_state] = current

        attributes_met = 0
        attributes_required = len(came_from)

        for states, actionList in actions_graph.edges.items():
            for k in came_from.keys():
                k_parsed = json.loads(k)
                for key, value in k_parsed:
                    for actionObject in actionList:
                        if actionObject.effects[key] == value:
                            attributes_met = attributes_met + 1

                    if attributes_required == attributes_met:
                        self.proposed_action = actionObject





      #  self.proposed_action = actions_graph.

        return came_from, cost_so_far






