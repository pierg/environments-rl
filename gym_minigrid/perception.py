import math
from gym_minigrid.extendedminigrid import *
from gym_minigrid.extendedminigrid import Water

AGENT_GRID_LOCATION = 2

# Helper class to analyse agent's observations
# All the methods should return True/False

class Perception():

    @staticmethod
    def is_immediate_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 1
        :param object_type: type of WorldObj
        :param distance: number of cells from the agent (1 = the one next to the agent cell)
        :return: True / False
        """
        # Todo : Ask pier if the monitors using env instead of agent_obs is normal ? if yes delete condition
        if Perception.light_on_current_room(obs):
            return object_type == obs.worldobj_in_agent(1, 0)
        return object_type == "None"


    @staticmethod
    def is_near_to_worldobj(obs, object_type):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_type' is equals to 2
        :param object_type: type of WorldObj
        :return: True / False
        """
        # Todo : Ask pier if the monitors using env instead of agent_obs is normal ? if yes delete condition
        if Perception.light_on_current_room(obs):
            return  object_type == obs.worldobj_in_agent(2, 0) or \
                    object_type == obs.worldobj_in_agent(0, 1) or \
                    object_type == obs.worldobj_in_agent(0, -1)
        return object_type == "None"

    @staticmethod
    def is_condition_satisfied(env, action_proposed, condition):
        """

        :param env: instance of ExMiniGridEnv
        :return:
        """
        if condition == "light-on-current-room":
            # Returns true if the lights are on in the room the agent is currently in
            return Perception.light_on_current_room(env)

        elif condition == "light-switch-turned-on":
            # It looks for a light switch around its field of view and returns true if it is on
            return Perception.light_switch_turned_on(env)

        elif condition == "door-opened-in-front":
            # Returns true if the agent is in front of an opened door
            return Perception.door_opened_in_front(env)

        elif condition == "door-closed-in-front":
            # Returns true if the agent is in front of an opened door
            return Perception.door_closed_in_front(env)

        elif condition == "deadend-in-front":
            # Returns true if the agent is in front of a deadend
            # deadend = all the tiles surrounding the agent view are 'wall' and the tiles in the middle are 'None'
            return Perception.deadend_in_front(env)

        elif condition == "entering-a-room":
            # Returns true if the agent is entering a room
            # Meaning there is a door in front and its action is to move forward
            if Perception.door_opened_in_front(env) and action_proposed == ExMiniGridEnv.Actions.forward:
                return True
            return False

    def door_opened_in_front(env):
        if ExMiniGridEnv.worldobj_in_agent(env, 1, 0) == "door":
            x, y = env.get_grid_coords_from_view((1, 0))
            if env.grid.get(x, y).is_open:
                return True
        return False

    def door_closed_in_front(env):
        if env.worldobj_in_agent(1, 0) == "door":
            x, y = env.get_grid_coords_from_view((1, 0))
            if not env.grid.get(x, y).is_open:
                return True
        return False

    def check(env, coordinates):
        wx, wy = env.get_grid_coords_from_view(coordinates)
        if 0 <= wx < env.grid.width and 0 <= wy < env.grid.height:
            front = env.grid.get(wx, wy)
            return front

    def deadend_in_front(env):
        i = 1
        while i < 4:
            left = Perception.check(env, (-1, i - 1))
            right = Perception.check(env, (1, i - 1))
            front = Perception.check(env, (0, i))
            if left is None or right is None:
                return False
            if front is not None:
                if front is Goal:
                    return False
                if left is None or right is None:
                    return False
                if left is not None and right is not None:
                    if left.type == "goal" or right.type == "goal":
                        return False
                    return True
                else:
                    return False
            i = i + 1
        return False

    def light_on_current_room(env):
        try:
            if env.roomList:
                for x in env.roomList:
                    if x.objectInRoom(env.agent_pos):
                        return x.getLight()
            return False
        except AttributeError:
            return False

    # Todo Fix bug (formula not correct ?)
    def light_switch_turned_on(env):
        agent_obs = ExGrid.decode(env.gen_obs()['image'])
        for i in range (0, len(agent_obs.grid)):
            if agent_obs.grid[i] is not None:
                if agent_obs.grid[i].type == "lightSwitch":
                    j, k = env.get_grid_coords_from_view((3-int(i/math.sqrt(len(agent_obs.grid))), (i%4)-2))
                    return env.grid.get(j, k).state
        return False