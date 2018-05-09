from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register
from gym_minigrid.envs.multiroom import *




class BigEnvironnementEnv(ExMiniGridEnv):
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
        self.grid.set(width//2,height-12,Door(('red')))

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 8, height - 2, Goal())

        # Place waters
        # The water muss't hide a tunnel or the door
        for i in range(1, 11):
            x, y = self._rand_pos(2, width // 2 - 1, 2, height - 6)
            self.grid.set(x, y, Water())
            x2, y2 = self._rand_pos(width // 2 + 2, width - 8, 1, height - 2)
            self.grid.set(x2, y2, Water())

        # Add the room
        RoomList = []
        RoomList.append(Room(
            (1, 1),
            (width // 2-1, height - 2),
            None,
            (width / 2, height - 12)
        ))
        RoomList.append(Room(
            (width // 2 + 1, 1),
            (width // 2 - 2, height - 1),
            (width // 2, height - 12),
            None
        ))




        # Create the shadow room
        xmin, ymin = RoomList[1].top
        sidex, sidey = RoomList[1].size
        xmax = xmin + sidex
        ymax = ymin + sidey
        xenter, yenter = RoomList[1].entryDoorPos
        tab=self._ShadowRoom(xmin,ymin,xmax,ymax)
        self.grid.set(xenter+1,yenter,ShadowRoom('yellow',(xmin, ymin, sidex, sidey,xenter+1,yenter)))

        # Place the door which separate the rooms
        self.grid.set(width // 2, height - 12, Door(('red')))
        # Place the lightswitch of the second room
        switch = [width // 2 + 1, height - 13]
        wx, wy = self._rand_pos(2, width // 2 - 1, 2, height - 6)
        self.grid.set(wx, wy, Lightswitch('yellow'))


        # Set start position
        self.start_pos = (1, 1)
        self.start_dir = 0

        self.mission = "get to the green goal square without moving on water"



    def _ShadowRoom(
        self,
        xmin,
        ymin,
        ymax,
        xmax,
    ):
        tab=[[]]
        for z in range(xmin, xmax):
            for t in range(ymin, ymax):
                worldobj = self.grid.get(z, t)
                if worldobj is not None:
                    tab.append((z, t, worldobj.type))
                    """
                    if worldobj.type == 'wall':
                        self.grid.set(z, t, Unnewswall())
                    else:
                        self.grid.set(z, t, Unnews())
                    #"""
                else:
                    tab.append((z, t, None))
                    #self.grid.set(z, t, Unnews())
        del tab[0]
        return tab
    #"""


    def save_room(self,room,pos):
        (z,t) = pos
        worldobj = self.grid.get(z, t)
        if worldobj is not None:
            if worldobj.type == "lightswitch":
                print("on the switch")
                for z in range(0, len(room)):
                    if room[z][2] == 'wall':
                        self.grid.set(room[z][0], room[z][1], Wall())
                    elif room[z][2] == 'water':
                        self.grid.set(room[z][0], room[z][1], Water())
                    elif room[z][2] == 'goal':
                        self.grid.set(room[z][0], room[z][1], Goal())
                    else:
                        self.grid.set(room[z][0], room[z][1], None)

register(
    id='MiniGrid-BigEnvironnement-32x32-v0',
    entry_point='gym_minigrid.envs:BigEnvironnementEnv'
)


