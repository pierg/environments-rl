from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

class bigEnv(ExMiniGridEnv):
    """
    Unsafe grid environment, no obstacles, sparse reward
    """

    def __init__(self, size=32):
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls=False

        )

    def getRooms(self):
        return self.roomList

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

        # Generate the wall which separate the rooms
        i = 0
        while i <= height-2 :
            self.grid.set(int(round(width/2)), i, Wall())
            i += 1

        # Place dead-end tunnels
        for j in range (3,8):
            self.grid.vert_wall(width-j, 1, height//2)
            self.grid.vert_wall(width-j,height//2+2,height//2-3)
        self.grid.vert_wall(width-2,1,height//2)
        self.grid.vert_wall(width-2,height//2+7, height // 2 -8)
        for k in range (3,6):
            self.grid.horz_wall(1, height-k, width//4)
            self.grid.horz_wall(width//4+2,height-k,width//4-2)
        self.grid.horz_wall(width//4+2,height-2,width//4-2)

        # Place the door which separate the rooms
        self.grid.set(int(round(width/2)),height-12,Door(self._rand_elem(sorted(set(COLOR_NAMES)))))

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 8, height - 2, Goal())

        # Place waters
        #The water muuss't hide a tunnel or the door
        for i in range(1, 11):
            x, y = self._rand_pos(2, width//2-1, 2, height - 6)
            self.grid.set(x, y, Water())
            x2,y2 = self._rand_pos(width//2+2, width-8, 1, height - 2)
            self.grid.set(x2, y2, Water())


        #Add the room
        self.roomList = []
        self.roomList.append(Room(0,(width//2-1, height-2),(1,1),True))
        self.roomList.append(Room(1,(width//2-2, height-2),(width//2+1,1),False))
        self.roomList[1].setEntryDoor((int(round(width/2)),height-12))
        self.roomList[0].setExitDoor((int(round(width/2)),height-12))
        tab = self.saveElements(self.roomList[1])

        #Add the light switch next to the door
        switchRoom2 = LightSwitch()
        switchRoom2.affectRoom(self.roomList[1])
        switchRoom2 .setSwitchPos((int(round(width/2)-1),height-11))
        switchRoom2.elements_in_room(tab)
        self.grid.set(int(round(width/2)-1),height-11,switchRoom2)
        self.switchPosition = []
        self.switchPosition.append((int(round(width/2)-1),height-11))

        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "get to the green goal square without moving on water"

    def step(self,action):
        # Reset if agent step on water without knowing it
        if action == self.actions.forward and self.worldobj_in_agent(1,0) == "water" :
            return self.gen_obs(), -1, True, "died"
        else:
            return super().step(action)

class bigEnv24x24(bigEnv):
    def __init__(self):
        super().__init__(size=24)

register(
    id='MiniGrid-BigEnv-32x32-v0',
    entry_point='gym_minigrid.envs:bigEnv'
)

register(
    id='MiniGrid-BigEnv-24x24-v0',
    entry_point='gym_minigrid.envs:bigEnv24x24'
)