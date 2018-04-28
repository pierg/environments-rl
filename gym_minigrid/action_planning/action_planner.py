from queue import PriorityQueue
from .obs_parser import ObservationParser
from .goals import *
from gym_minigrid.extendedminigrid import ExMiniGridEnv


class ActionPlanner:

    """"
         Action planner needs an implementation of A* where Nodes are
         states of the world and edges the actions between them.

         The cost of a node can be calculated as the sum of the costs of the actions
         that take the world to the state represented by the node.



         The heuristic distance can be calculated as the sum of the unstatisfied properties
         of the goal state.
    """

    print('works')
    frontier = PriorityQueue()

    @staticmethod
    def plan(obs):

        current_state = ObservationParser().get_current_state(obs)
        # how do we know the goal?
        goal_state = move_away_from_danger

        return ExMiniGridEnv.Actions.wait

    def heuristic(x, y):
        """
        :param x: Starting world state
        :param y: World state to compare
        :return: The sum (ammount) of the unsatisfied properties of the goal state compared to the current state
        """
        # TODO define the states in python

    def action_planner(actions, starting_state, goal_state):
        """
        :param actions:  list of possible actions
        :param starting_state: Starting state
        :param goal_state: Desired state
        :return: came_from, cost_so_far
        """
        #TODO implement action planner