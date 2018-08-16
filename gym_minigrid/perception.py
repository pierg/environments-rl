from gym_minigrid.extendedminigrid import *

AGENT_GRID_LOCATION = 2


# Helper class to analyse agent's observations
# All the methods should return True/False


class Perception():

    scanning_is_done = False
    array_pos =[]
    door_open = False
    light_on = False
    door_room = 0

    def save_position_scan(env):
        width = env.grid.width
        height = env.grid.height
        for i in range(height):
            for j in range(width):
                object_pos = env.grid.get(i, j)
                if object_pos is not None:
                    if hasattr(object_pos, 'state') or hasattr(object_pos, 'is_open'):
                        Perception.array_pos.append([object_pos.type, i, j])
                    if object_pos.type == 'door':
                        try:
                            if env.roomList:
                                for x in env.roomList:
                                    if x.objectInRoom((i,j)):
                                        door_room = x.number
                        except AttributeError:
                            pass

        print(Perception.array_pos)
        Perception.scanning_is_done = True

    def check_state(env):
        for k in  range(len(Perception.array_pos)):
            object = env.grid.get(Perception.array_pos[k][1], Perception.array_pos[k][2])
            if object.type == 'door':
                Perception.door_open = object.is_open
            elif object.type == 'lightsw':
                Perception.light_on = object.state

        
    @staticmethod
    def in_front_of(obs, object_name):
        """
        General method that returns true the object_name is in the cell in front of the agent
        :param object_name: string indicating the type of WorldObj
        :return: True / False
        """
        if Perception.light_on_current_room(obs):
            return object_name == obs.worldobj_in_agent(1, 0)
        # TODO: why compare object type to None? and not just sinmply return false if the light is off
        return object_name == "None"

    @staticmethod
    def at_left_is(obs, object_name):
        """
        General method that returns true the object_name is at the cell on the left side of the agent
        :param object_name: string indicating the type of WorldObj
        :return: True / False
        """
        if Perception.light_on_current_room(obs):
            return object_name == obs.worldobj_in_agent(0, -1)
        return object_name == "None"

    @staticmethod
    def at_right_is(obs, object_name):
        """
        General method that returns true the object_name is at the cell on the right side of the agent
        :param object_name: string indicating the type of WorldObj
        :return: True / False
        """
        if Perception.light_on_current_room(obs):
            return object_name == obs.worldobj_in_agent(0, 1)
        return object_name == "None"

    @staticmethod
    def is_immediate_to_worldobj(obs, object_name):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_name' is equals to 1
        :param object_name: string indicating the type of WorldObj
        :param distance: number of cells from the agent (1 = the one next to the agent cell)
        :return: True / False
        """
        if Perception.light_on_current_room(obs):
            return object_name == obs.worldobj_in_agent(1, 0)
        return object_name == "None"

    @staticmethod
    def is_near_to_worldobj(obs, object_name):
        """
        General method that returns true if the number of steps (sequence of actions) to reach a cell
        of type 'object_name' is equals to 2
        :param object_name: string indicating the type of WorldObj
        :return: True / False
        """
        if Perception.light_on_current_room(obs):
            return object_name == obs.worldobj_in_agent(2, 0) or \
                   object_name == obs.worldobj_in_agent(0, 1) or \
                   object_name == obs.worldobj_in_agent(0, -1)
        return object_name == "None"

    @staticmethod
    def is_condition_satisfied(env, condition, action_proposed=None):
        """
        :param env: instance of ExMiniGridEnv
        :return:
        """
        if not Perception.scanning_is_done:
            Perception.save_position_scan(env)
        Perception.check_state(env)

        if condition == "light-on-current-room":
            # Returns true if the lights are on in the room the agent is currently in
            return Perception.light_on_current_room(env)

        elif condition == "light-switch-turned-on":
            # It looks for a light switch around its field of view and returns true if it is on
            return Perception.light_switch_turned_on(env)

        elif condition == "light-switch-in-front-off":
            # Returns true if the agent is in front of a light-switch and it is off
            return Perception.list_switch_in_front_off(env)

        elif condition == "door-opened":
            # Returns true if the agent is in front of an opened door
            return Perception.door_opened(env)

        elif condition == "door-closed":
            # Returns true if the agent is in front of an opened door
            return Perception.door_closed(env)

        elif condition == "door-opened-in-front":
            # Returns true if the agent is in front of an opened door
            return Perception.door_opened_in_front(env)

        elif condition == "door-closed-in-front":
            # Returns true if the agent is in front of an opened door
            return Perception.door_closed_in_front(env)

        elif condition == "deadend-in-front":
            # Returns true if the agent is in front of a deadend
            # deadend = all the tiles surrounding the agent view are 'wall' and the tiles in the middle are 'None'
            return Perception.deadend_in_front(env) and action_proposed == ExMiniGridEnv.Actions.forward

        elif condition == "stepping-on-water":
            # Returns true if the agent is in front of a water tile and its action is "Forward"
            return ExMiniGridEnv.worldobj_in_agent(env, 1, 0) == "water" \
                   and action_proposed == ExMiniGridEnv.Actions.forward and Perception.light_on_current_room(env)

        elif condition == "entering-a-room":
            # Returns true if the agent is entering a room
            # Meaning there is a door in front and its action is to move forward
            if Perception.door_opened_in_front(env) and action_proposed == ExMiniGridEnv.Actions.forward:
                return True
            return False

        elif condition == "action-is-toggle":
            return action_proposed == ExMiniGridEnv.Actions.toggle

        elif condition == "action-is-forward":
            return action_proposed == ExMiniGridEnv.Actions.forward

        elif condition == "action-is-left":
            return action_proposed == ExMiniGridEnv.Actions.left

        elif condition == "action-is-right":
            return action_proposed == ExMiniGridEnv.Actions.right

        elif condition == "light-on-next-room":
            # It returns true is the light in the other room of the environment
            return Perception.light_on_next_room(env)

        elif condition == "room-0":
            # Returns true if the agent is in the room where it first starts
            return Perception.agent_in_room_number(env, 0)

        elif condition == "room-1":
            # Returns true if the agent is in the room after it crossed the door
            return Perception.agent_in_room_number(env, 1)

    def light_on_next_room(env):
        try:
            if env.roomList:
                for x in env.roomList:
                    bCurrent = False
                    if x.objectInRoom(env.agent_pos):
                        bCurrent = True
                    if not bCurrent:
                        return x.lightOn
            return False
        except AttributeError:
            return True

    def agent_in_room_number(env, number):
        try:
            if env.roomList:
                for x in env.roomList:
                    if x.objectInRoom(env.agent_pos):
                        return x.number == number
            return True
        except AttributeError:
            return True

    def is_condition_true(self):
        return True

    def door_opened_in_front(env):
        return ExMiniGridEnv.worldobj_in_agent(env, 1, 0) == "door" and Perception.door_open

    def door_closed(env):
        return not Perception.door_open

    def door_opened(env):
        return Perception.door_open


    def list_switch_in_front_off(env):
        return (env.worldobj_in_agent(1, 0) == "lightsw" and not Perception.light_on)

    def list_switch_in_front_on(env):
        return (env.worldobj_in_agent(1, 0) == "lightsw" and Perception.light_on)

    def door_closed_in_front(env):
        return (env.worldobj_in_agent(1, 0) == "door" and not Perception.door_open)

    def check_if_coordinates_in_env(env, coordinates):
        wx, wy = env.get_grid_coords_from_view(coordinates)
        if 0 <= wx < env.grid.width and 0 <= wy < env.grid.height:
            front = env.grid.get(wx, wy)
            return front

    def deadend_in_front(env):
        i = 1
        agent_obs = ExGrid.decode(env.gen_obs()['image'])
        grid_len = int(math.sqrt(len(agent_obs.grid)))
        front = None
        while i < grid_len and front is None:
            front = Perception.check_if_coordinates_in_env(env, (i, 0))
            left = Perception.check_if_coordinates_in_env(env, (i - 1, -1))
            right = Perception.check_if_coordinates_in_env(env, (i - 1, 1))
            if left is None or right is None:
                return False
            if front is not None:
                if front.type == "goal":
                    return False
                if left is not None and right is not None:
                    if left.type == "goal" or right.type == "goal":
                        return False
                return True
            i += 1
        return False

    def light_on_current_room(env):
        try:
            if env.roomList:
                for x in env.roomList:
                    if x.objectInRoom(env.agent_pos):
                        return x.lightOn
            return True
        except AttributeError:
            return True

    def light_switch_turned_on(env):
        agent_obs = ExGrid.decode(env.gen_obs()['image'])
        for i in range(0, len(agent_obs.grid)):
            if agent_obs.grid[i] is not None:
                if agent_obs.grid[i].type == "lightsw":
                    return Perception.light_on
        return False
