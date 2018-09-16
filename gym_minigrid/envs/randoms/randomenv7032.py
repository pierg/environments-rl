
from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

import random

class RandomEnv(ExMiniGridEnv):

    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls= not True
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
        
    def _random_or_not_position(self, xmin, xmax, ymin, ymax ):
        if False:
            width_pos, height_pos = self._rand_pos( xmin, xmax + 1, ymin, ymax + 1)
        else:
            width_pos = random.randint( xmin, xmax)
            height_pos = random.randint( ymin, ymax)
        return width_pos, height_pos
        
    def _random_number(self, min, max):
        if False:
            return self._rand_int(min,max+1)
        else:
            return random.randint(min,max)
    
    def _random_or_not_bool(self):
        if False:
            return self._rand_bool()
        else:
            return random.choice([True, False])
        
    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the top-left corner
        self.start_pos = (1, 1)
        self.start_dir = 0

        # Place a goal square in the top-right corner
        self.grid.set(width - 2, 1, Goal())

        # Set the random seed to the random token, so we can reproduce the environment
        random.seed("7032")
        
        #Place lightswitch
        width_pos = 2
        height_pos = 5
        xdoor = 3
        ydoor = 4
        switchRoom = LightSwitch()
        
        #Place the wall
        self.grid.vert_wall(width_pos+1, 1, height-2)
        
                
        self.grid.set(xdoor, ydoor , Door(self._rand_elem(sorted(set(COLOR_NAMES)))))
        
        #Add the room
        self.roomList = []
        self.roomList.append(Room(0,(width_pos + 1, height),(0, 0),True))
        self.roomList.append(Room(1,(width - width_pos - 2, height),(width_pos + 1, 0),False))
        self.roomList[1].setEntryDoor((xdoor,ydoor))
        self.roomList[0].setExitDoor((xdoor,ydoor))        
        
        #Place the lightswitch
        switchRoom.affectRoom(self.roomList[1])
        switchRoom.setSwitchPos((width_pos,height_pos))
        
        self.grid.set(width_pos, height_pos, switchRoom)
        self.switchPosition = []
        self.switchPosition.append((width_pos, height_pos))

        # Place water
        placed_water_tiles = 0
        anti_loop = 0
        while 5 > placed_water_tiles:
        
            # Added to avoid a number of water tiles that is impossible (infinite loop)
            anti_loop +=1
            if anti_loop > 1000:
                placed_water_tiles = 5
            # Minus 2 because grid is zero indexed, and the last one is just a wall
            width_pos , height_pos = self._random_or_not_position(1, width - 2, 1, height - 2)
            number = self._random_number(1,6)
            if number == 1:
                width_pos , height_pos = (1,2)
            elif number == 2:
                width_pos , height_pos = (1,3)
            elif number == 3:
                width_pos , height_pos = (1,4)
            elif number == 4:
                width_pos , height_pos = (4,1)
            elif number == 5:
                width_pos , height_pos = (4,2)
            elif number == 6:
                width_pos , height_pos = (5,4)
            if isinstance(self.grid.get(width_pos, height_pos), Water):
                # Do not place water on water
                continue
            self.grid.set(width_pos, height_pos, Water())
            placed_water_tiles += 1
        self.mission = ""
        
    def step(self,action):
        # Reset if agent step on water without knowing it
        if action == self.actions.forward and self.worldobj_in_agent(1,0) == "water" :
            return self.gen_obs(), -1, True, "died"
        else:
            return super().step(action)

class RandomEnv7x7_7032(RandomEnv):
    def __init__(self):
        super().__init__(size=7)

register(
    id='MiniGrid-RandomEnv-7x7-7032-v0',
    entry_point='gym_minigrid.envs:RandomEnv7x7_7032'
)
