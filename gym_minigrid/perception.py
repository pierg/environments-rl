from gym_minigrid.extendedminigrid import *


class Perception():

    def __init__(self, observations):
        self.obs_grid, extra_obs = observations
        self.obs_door_open = extra_obs[0]
        self.obs_light_on = extra_obs[1]
        self.current_room = extra_obs[2]
        self.current_room_light = extra_obs[3]
        self.next_room_light = extra_obs[4]

    def search_and_return(self, element_name):
        grid = self.obs_grid
        for i, e in enumerate(grid.grid):
            if e is not None and e.type == element_name:
                return e
        return None

    def element_in_front(self):
        grid = self.obs_grid
        front_index = grid.width*(grid.height-2) + int(math.floor(grid.width/2))
        return grid.grid[front_index]

    def element_at_right(self):
        grid = self.obs_grid
        right_index = grid.width*(grid.height-1) + int(math.floor(grid.width/2) + 1)
        return grid.grid[right_index]

    def element_at_left(self):
        grid = self.obs_grid
        left_index = grid.width*(grid.height-1) + int(math.floor(grid.width/2) - 1)
        return grid.grid[left_index]

    def in_front_of(self, elem):
        e = self.element_in_front()
        if e is not None and e.type == elem:
            return True
        return False

    def at_right_is(self, elem):
        e = self.element_at_right()
        if e is not None and e.type == elem:
            return True
        return False

    def at_left_is(self, elem):
        e = self.element_at_left()
        if e is not None and e.type == elem:
            return True
        return False

    def update(self, observations):
        self.obs_grid, extra_obs = observations
        self.obs_door_open = extra_obs[0]
        self.obs_light_on = extra_obs[1]
        self.current_room = extra_obs[2]
        self.current_room_light = extra_obs[3]
        self.next_room_light = extra_obs[4]

    def is_condition_satisfied(self, condition, action_proposed=None):
        if condition == "light-on-current-room":
            # Returns true if the lights are on in the room the agent is currently in
            if self.current_room_light == 1:
                return True
            return False

        elif condition == "light-switch-turned-on":
            # It looks for a light switch around its field of view and returns true if it is on
            if self.obs_light_on == 1:
                return True
            return False


        elif condition == "light-switch-in-front-off":
            # Returns true if the agent is in front of a light-switch and it is off
            elem = self.element_in_front()
            if elem is not None and elem.type == "lightsw" \
                    and hasattr(elem, 'is_on') and not elem.is_on:
                return True
            return False

        elif condition == "door-opened-in-front":
            # Returns true if the agent is in front of an opened door
            elem = self.element_in_front()
            if elem is not None and elem.type == "door" \
                    and hasattr(elem, 'is_open') and elem.is_open:
                return True
            return False

        elif condition == "door-opened":
            # Returns true if the agent is in front of an opened door
            elem = self.search_and_return("door")
            if elem is not None and hasattr(elem, 'is_open') and elem.is_open:
                return True
            return False

        elif condition == "door-closed":
            # Returns true if the agent is in front of an opened door
            elem = self.search_and_return("door")
            if elem is not None and hasattr(elem, 'is_open') and not elem.is_open:
                return True
            return False

        elif condition == "door-closed-in-front":
            # Returns true if the agent is in front of an opened door
            elem = self.element_in_front()
            if elem is not None and elem.type == "door" \
                    and hasattr(elem, 'is_open') and not elem.is_open:
                return True
            return False

        elif condition == "deadend-in-front":
            # Returns true if the agent is in front of a deadend
            # deadend = all the tiles surrounding the agent view are 'wall' and the tiles in the middle are 'None'
            return NotImplementedError

        elif condition == "stepping-on-water":
            # Returns true if the agent is in front of a water tile and its action is "Forward"
            elem = self.element_in_front()
            if elem is not None and elem.type == "water" \
                    and action_proposed == ExMiniGridEnv.Actions.forward:
                return True
            return False

        elif condition == "entering-a-room":
            # Returns true if the agent is entering a room
            # Meaning there is a door in front and its action is to move forward
            elem = self.element_in_front()
            if elem is not None and elem.type == "door" \
                    and hasattr(elem, 'is_open') and elem.is_open \
                    and action_proposed == ExMiniGridEnv.Actions.forward:
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
            if self.next_room_light == 1:
                return True
            return False

        elif condition == "room-0":
            # Returns true if the agent is in the room where it first starts
            if self.current_room == 0:
                return True
            return False

        elif condition == "room-1":
            # Returns true if the agent is in the room after it crossed the door
            if self.current_room == 1:
                return True
            return False
