from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register


class LightTestEnv(ExMiniGridEnv):
    """
    Unsafe grid environment, no obstacles, sparse reward
    """

    def __init__(self, size=5):
        super().__init__(
            grid_size=size,
            max_steps=4 * size * size,
            # Set this to True for maximum speed
            see_through_walls=True
        )

    def step(self, action):
        # Reset if agent step on water without knowing it
        if action == self.actions.forward and self.worldobj_in_agent(1, 0) == "water":
            return self.gen_obs(), 0, True, "died"
        else:
            return super().step(action)

    def saveElements(self,room):
        tab=[]
        (x , y) = room.position
        (width , height) = room.size
        for i in range(x , x + width):
            for j in range(y , y + height):
                objType = self.grid.get(i,j)
                if objType is not None:
                    tab.append((i,j,0))
                else:
                    tab.append((i, j, 1))
        return tab

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the top-left corner
        self.start_pos = (1, 1)
        self.start_dir = 0

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        #Place the wall which separate the room
        self.grid.vert_wall( 2, 1, 3)

        #Place the door
        self.grid.set( 2, 2, Door(self._rand_elem(sorted(set(COLOR_NAMES)))))

        # Add the room
        self.roomList = []
        self.roomList.append(Room(0, (1, 3), (1, 1), True))
        self.roomList.append(Room(1, (1, 3), (3, 1), False))
        self.roomList[1].setEntryDoor((2,2))
        self.roomList[0].setExitDoor((2,2))
        tab = self.saveElements(self.roomList[1])

        # Add the light switch next to the door
        switchRoom2 = LightSwitch()
        switchRoom2.affectRoom(self.roomList[1])
        switchRoom2.setSwitchPos((1, 3))
        switchRoom2.elements_in_room(tab)
        self.grid.set(1, 3, switchRoom2)
        self.switchPosition = []
        self.switchPosition.append((1, 3))

        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "get to the green goal square without moving on water"



register(
    id='MiniGrid-LightTest-6x6-v0',
    entry_point='gym_minigrid.envs:LightTestEnv'
)