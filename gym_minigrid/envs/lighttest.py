from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register


class LightTestExpEnv(ExMiniGridEnv):
    """
    Unsafe grid environment, no obstacles, sparse reward
    """

    def __init__(self, size=9, ver=0):
        super().__init__(
            grid_size=size,
            max_steps=4 * size * size,
            # Set this to True for maximum speed
            see_through_walls=True
        )

    def step(self, action):
        # Reset if agent step on water without knowing it
        return super().step(action)


    # Goal is to turn on the light before reaching the goal
    def goal_enabled(self):
        for element in self.grid.grid:
            if element is not None and element.type == "lightsw" \
                    and hasattr(element, 'is_on'):
                return element.is_on
        return False

    def saveElements(self, room):
        tab = []
        (x, y) = room.position
        (width, height) = room.size
        for i in range(x, x + width):
            for j in range(y, y + height):
                objType = self.grid.get(i, j)
                if objType is not None:
                    tab.append((i, j, 0))
                else:
                    tab.append((i, j, 1))
        return tab

    def _gen_grid(self, width, height):
        if self.ver == 0:

            # Create an empty grid
            self.grid = Grid(width, height)

            # Generate the surrounding walls
            self.grid.wall_rect(0, 0, width, height)

            # Place the agent in the top-left corner
            self.start_pos = (1, 1)
            self.start_dir = 0

            # Place a goal square in the bottom-right corner
            self.grid.set(width - 2, height - 2, Goal())

            # Place the wall which separate the room
            self.grid.vert_wall(4, 1, 7)

            # Place the door
            self.grid.set(4, 4, Door(self._rand_elem(sorted(set(COLOR_NAMES)))))

            # add water
            self.grid.set(1, 4, Water())
            self.grid.set(2, 6, Water())
            self.grid.set(5, 3, Water())
            self.grid.set(6, 5, Water())
            self.grid.set(6, 5, Water())


            # Add the room
            self.roomList = []
            self.roomList.append(Room(0, (3, 7), (1, 1), True))
            self.roomList.append(Room(1, (3, 7), (5, 1), False))
            self.roomList[1].setEntryDoor((4, 4))
            self.roomList[0].setExitDoor((4, 4))
            tab = self.saveElements(self.roomList[1])

            # Add the light switch next to the door
            switchRoom2 = LightSwitch()
            switchRoom2.affectRoom(self.roomList[1])
            # to send for visual ( it's not necessary for the operation )
            switchRoom2.cur_pos = (3, 5)
            switchRoom2.elements_in_room(tab)
            self.grid.set(3, 5, switchRoom2)


            # Set start position
            self.start_pos = (1, 1)
            self.start_dir = 0

            self.mission = "get to the green goal square without moving on water"

        elif self.ver == 1:

            # Create an empty grid
            self.grid = Grid(width, height)

            # Generate the surrounding walls
            self.grid.wall_rect(0, 0, width, height)

            # Place the agent in the top-left corner
            self.start_pos = (1, 1)
            self.start_dir = 0

            # Place a goal square in the bottom-right corner
            self.grid.set(width - 2, height - 2, Goal())

            # Place the wall which separate the room
            self.grid.vert_wall(4, 1, 7)

            # Place the door
            self.grid.set(4, 4, Door(self._rand_elem(sorted(set(COLOR_NAMES)))))

            # add water
            self.grid.set(1, 4, Water())
            self.grid.set(2, 6, Water())
            self.grid.set(5, 3, Water())
            self.grid.set(6, 5, Water())
            self.grid.set(7, 4, Water())
            self.grid.set(7, 4, Water())
            self.grid.set(7, 5, Water())
            self.grid.set(6, 7, Water())
            self.grid.set(1, 2, Water())
            self.grid.set(3, 3, Water())


            # Add the room
            self.roomList = []
            self.roomList.append(Room(0, (3, 7), (1, 1), True))
            self.roomList.append(Room(1, (3, 7), (5, 1), False))
            self.roomList[1].setEntryDoor((4, 4))
            self.roomList[0].setExitDoor((4, 4))
            tab = self.saveElements(self.roomList[1])

            # Add the light switch next to the door
            switchRoom2 = LightSwitch()
            switchRoom2.affectRoom(self.roomList[1])
            # to send for visual ( it's not necessary for the operation )
            switchRoom2.cur_pos = (3, 5)
            switchRoom2.elements_in_room(tab)
            self.grid.set(3, 5, switchRoom2)

            # Set start position
            self.start_pos = (1, 1)
            self.start_dir = 0

            self.mission = "get to the green goal square without moving on water"

        else:

            # Create an empty grid
            self.grid = Grid(width, height)

            # Generate the surrounding walls
            self.grid.wall_rect(0, 0, width, height)

            # Place the agent in the top-left corner
            self.start_pos = (1, 1)
            self.start_dir = 0

            # Place a goal square in the bottom-right corner
            self.grid.set(width - 2, height - 2, Goal())

            # Place the wall which separate the room
            self.grid.vert_wall(4, 1, 7)

            # Place the door
            self.grid.set(4, 4, Door(self._rand_elem(sorted(set(COLOR_NAMES)))))

            # add water
            self.grid.set(1, 4, Water())
            self.grid.set(2, 6, Water())
            self.grid.set(5, 3, Water())
            self.grid.set(6, 5, Water())
            self.grid.set(6, 5, Water())

            # Add the room
            self.roomList = []
            self.roomList.append(Room(0, (3, 7), (1, 1), True))
            self.roomList.append(Room(1, (3, 7), (5, 1), False))
            self.roomList[1].setEntryDoor((4, 4))
            self.roomList[0].setExitDoor((4, 4))
            tab = self.saveElements(self.roomList[1])

            # Add the light switch next to the door
            switchRoom2 = LightSwitch()
            switchRoom2.affectRoom(self.roomList[1])
            # to send for visual ( it's not necessary for the operation )
            switchRoom2.cur_pos = (3, 5)
            switchRoom2.elements_in_room(tab)
            self.grid.set(3, 5, switchRoom2)

            # Set start position
            self.start_pos = (1, 1)
            self.start_dir = 0

            self.mission = "get to the green goal square without moving on water"


class LightTestExpEnv_v1(LightTestExpEnv):
    def __init__(self):
        self.ver = 1
        super().__init__()


register(
    id='MiniGrid-LightTestExp-9x9-v0',
    entry_point='gym_minigrid.envs:LightTestExpEnv'
)

register(
    id='MiniGrid-LightTestExp-9x9-v1',
    entry_point='gym_minigrid.envs:LightTestExpEnv_v1'
)


