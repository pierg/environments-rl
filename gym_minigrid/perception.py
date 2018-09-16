from gym_minigrid.extendedminigrid import *


class Perception():

    def __init__(self, obs_grid):
        self.obs_grid = obs_grid
        self.agent_pos = None

    def search_and_return(self, element_name):
        grid = self.obs_grid[0]
        for i, e in enumerate(grid.grid):
            if e is not None and e.type == element_name:
                return e
        return None

    def element_in_front(self):
        grid = self.obs_grid[0]
        front_index = grid.width*(grid.height-2) + int(math.floor(grid.width/2))
        return grid.grid[front_index]


    def update(self, obs_grid, agent_pos):
        self.obs_grid = obs_grid
        self.agent_pos = agent_pos


    def is_condition_satisfied(self, condition, action_proposed=None):
        if condition == "light-on-current-room":
            # Returns true if the lights are on in the room the agent is currently in
            return NotImplementedError

        elif condition == "light-switch-turned-on":
            # It looks for a light switch around its field of view and returns true if it is on
            elem = self.search_and_return("lightsw")
            if elem is not None:
                return hasattr(elem, 'is_on') and elem.is_on
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
            return NotImplementedError

        elif condition == "room-0":
            # Returns true if the agent is in the room where it first starts
            return NotImplementedError

        elif condition == "room-1":
            # Returns true if the agent is in the room after it crossed the door
            return NotImplementedError
