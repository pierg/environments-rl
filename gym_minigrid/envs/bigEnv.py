from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register
from gym_minigrid.envs.multiroom import *

class Light:
    def __init__(self,room,switch):
        self.top = room
        self.switch = switch

class BigEnv(ExMiniGridEnv):
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

        # Place the lightswitch of the second room
        switch= [width//2+1,height-13]
        wx, wy = self._rand_pos(2, width//2-1, 2, height - 6)
        self.grid.set(wx, wy, LightSwitch())

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
        RoomList = []
        RoomList.append(Room(
            (1, 1),
            (width//2-1, height-2),
            None,
            (width / 2, height - 12)
        ))
        RoomList.append(Room(
            (width//2+1, 1),
            (width//2-2, height-2),
            (width / 2, height - 12),
            None
        ))

        # Create the shadows room
        xmin, ymin = RoomList[1].top
        sidex, sidey = RoomList[1].size
        xmax = xmin + sidex
        ymax = ymin + sidey
        tab = []
        tab = self._ShadowRoom(xmin, ymin, xmax, ymax)
        # """

        # Create the light affiliated to the room 2
        self.agent_pos = (1, 1)
        self.agent_dir = 0

        self._LightRoom(switch[0], switch[1], tab)

        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "get to the green goal square without moving on water"

    def _ShadowRoom(self,xmin,ymin,ymax,xmax):
        tab = [[]]
        for z in range(xmin, xmax):
            for t in range(ymin, ymax):
                tab.append((z, t, self.grid.get(z, t)))
                worldobj = self.grid.get(z, t)
                if worldobj is not None:
                    if worldobj.type == 'wall':
                        self.grid.set(z, t, Wall())
                    else :
                        self.grid.set(z,t,UnknownCell())
                else:
                    self.grid.set(z,t,UnknownCell())
                print(tab[(len(tab) - 1)])
        return tab

    def _LightRoom(self,switchx,switchy,tab):

        i,j=ExMiniGridEnv.get_grid_coords_from_view(self,(0,0))
        if (i,j) == (switchx,switchy):
            print(" on the switch")
            for z in range(0,len(tab)):
                    self.grid.set(tab[z[0]],tab[z[1]],tab[z[2]])


register(
    id='MiniGrid-BigEnv-32x32-v0',
    entry_point='gym_minigrid.envs:BigEnv'
)