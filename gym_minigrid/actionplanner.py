from queue import PriorityQueue

class ActionPlanner():
    frontier = PriorityQueue()


    """"
         Action planner needs an implementation of A* where Nodes are
         states of the world and edges the actions between them.

         The cost of a node can be calculated as the sum of the costs of the actions
         that take the world to the state represented by the node.



         The heuristic distance can be calculated as the sum of the unstatisfied properties
         of the goal state.
    """

    def heuristic(x, y):
        """
        :param x: Starting world state
        :param y: World state to compare
        :return: The sum (ammount) of the unsatisfied properties of the goal state compared to the current state
        """
        # TODO define the states in python

    def actionPlanner(actions, starting_state, goal_state):
        """
        :param actions:  list of possible actions
        :param starting_state: Starting state
        :param goal_state: Desired state
        :return: came_from, cost_so_far
        """
        #TODO implement action planner


