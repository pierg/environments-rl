from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register
from gym_minigrid.envs.multiroom import *

global realGrid, grid

class Room:

    def __init__(self, room, size, position, lightOn):
        self.number = room
        self.size = size
        self.position = position
        self.lightOn = lightOn

    def setLight(self,lightOn):
        self.lightOn = lightOn
        self.activate()

    def getLight(self):
        return self.lightOn

    def activate(self):
        global grid,realGrid
        print("ok")
        x,y = self.size
        k,l = self.position
        x += k
        y += l
        for i in range(k,x):
            for j in range(l,y):
                if self.lightOn:
                    if realGrid.get(i,j) is not None:
                        grid.set(i,j,realGrid.get(i,j))
                    else :
                        grid.set(i,j,None)
                else :
                    cell = UnknownCell()
                    cell.affectWolrdObj(realGrid.get(i,j))
                    grid.set(i,j,cell)

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

    def _gen_grid(self, width, height):
        # Create an empty grid
        global grid,realGrid

        self.grid = Grid(width, height)
        grid = self.grid
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

        # Place the lightswitch of the second room
        switch= [width//2+1,height-13]
        wx, wy = self._rand_pos(2, width//2-1, 2, height - 6)
        #self.grid.set(wx, wy, Lightswitch())

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 8, height - 2, Goal())

        # Place waters
        #The water muuss't hide a tunnel or the door
        for i in range(1, 11):
            x, y = self._rand_pos(2, width//2-1, 2, height - 6)
            self.grid.set(x, y, Water())
            x2,y2 = self._rand_pos(width//2+2, width-8, 1, height - 2)
            self.grid.set(x2, y2, Water())

        realGrid = self.grid.copy()

        #Add the room
        self.roomList = []
        self.roomList.append(Room(1,(width//2-1, height-2),(1,1),True))
        self.roomList.append(Room(2,(width//2-2, height-2),(width//2+1,1),False))

        switchRoom2 = LightSwitch()
        switchRoom2.affectRoom(self.roomList[1])
        self.grid.set(3,3,switchRoom2)

        self.roomList[1].activate()




        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "get to the green goal square without moving on water"

register(
    id='MiniGrid-BigEnv-32x32-v0',
    entry_point='gym_minigrid.envs:bigEnv'
)