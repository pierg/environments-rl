
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

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height - 2, Goal())

        # Set the random seed to the random token, so we can reproduce the environment
        random.seed("9660")
        
        #Place lightswitch
        lightswitch_is_posed = False
        test_goal = 0
        if True:
            while not lightswitch_is_posed:
                width_pos , height_pos = self._random_or_not_position(5, width - 6, 0, height - 1)
                
                #lightswitch and room wall must not replace a fundamental element (goal, key, ...)
                continue_while = True
                if isinstance(self.grid.get(width_pos, height_pos), Goal) or                  isinstance(self.grid.get(width_pos, height_pos), Key):
                    continue_while = False
                for i in range(0,height):
                    if isinstance(self.grid.get(width_pos + 1, i), Goal) or                      isinstance(self.grid.get(width_pos + 1, i), Key):
                        continue_while = False
                        break
                if not continue_while:
                    print("true")
                    continue
                        
                switchRoom = LightSwitch()
                
                #Place the wall
                self.grid.vert_wall(width_pos+1, 1, height-2)
                
                #Place the door
                if height_pos == 0 or height_pos == 1:
                    xdoor, ydoor = width_pos + 1, height_pos + 1
                elif height_pos == height - 2 or height_pos == height - 1:
                    xdoor, ydoor = width_pos + 1, height_pos - 1
                else:
                    
                    if self._random_or_not_bool():
                        xdoor, ydoor = width_pos + 1, height_pos - 1
                    else:
                        xdoor, ydoor = width_pos + 1, height_pos + 1
                        
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
                
                lightswitch_is_posed = True


        # Place dead ends
        placed_dead_ends = 0
        tmp = self._random_number(0,3)
        while 2 > placed_dead_ends:
            if self.grid_size < 10:
                # Limit to one dead end if the grid is too small
                if self._random_or_not_bool():
                    self.grid.vert_wall(width//2-1,height//2,height//2)
                else:
                    self.grid.horz_wall(width//2,height//2-1,width//2)
                placed_dead_ends = 2
            else:
                if tmp == 0:
                    self.grid.vert_wall(2,height-6,3)
                    self.grid.horz_wall(1,height-3,1)
                elif tmp == 1:
                    self.grid.horz_wall(1,height-3,3)
                elif tmp == 2:
                    self.grid.vert_wall(width-3,3,3)
                    self.grid.horz_wall(width-2,6,2)
                elif tmp == 3:
                    self.grid.vert_wall(6,0,2)
                    self.grid.horz_wall(3,2,3)
                tmp = (tmp+1)%4
                placed_dead_ends += 1

        # Place water
        placed_water_tiles = 0
        anti_loop = 0
        while 2 > placed_water_tiles:
        
            # Added to avoid a number of water tiles that is impossible (infinite loop)
            anti_loop +=1
            if anti_loop > 1000:
                placed_water_tiles = 2
            # Minus 2 because grid is zero indexed, and the last one is just a wall
            width_pos , height_pos = self._random_or_not_position(1, width - 2, 1, height - 2)

            if width_pos == 1 and height_pos == 1:
                # Do not place water on agent
                continue
            if width_pos == 1 and height_pos == 2 and isinstance(self.grid.get(2, 1), Water) or width_pos == 2 and height_pos == 1 and isinstance(self.grid.get(1, 2), Water):
                # Do not place two water tiles in front of the agent A W -
                #                                                    W | |
                #                                                    | | |
                continue
            if isinstance(self.grid.get(width_pos, height_pos), Water):
                # Do not place water on water
                continue
            if isinstance(self.grid.get(width_pos, height_pos), Goal):
                # Do not place water on Goal
                continue
            if width_pos == width - 2 and height_pos == height - 3 and isinstance(self.grid.get(width - 3, height - 2), Water) or width_pos == width - 3 and height_pos == height - 2 and isinstance(self.grid.get(width - 2, height - 3), Water):
                # Do not place water preventing the agent from reaching the goal - | |
                #                                                                - A W
                #                                                                - W G
                continue
            if isinstance(self.grid.get(width_pos-1, height_pos), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos+1, height_pos), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos, height_pos-1), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos, height_pos+1), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos-1, height_pos-1), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos-1, height_pos+1), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos+1, height_pos-1), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos+1, height_pos+1), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos, height_pos), Wall):
                # Do not place water preventing the agent from going into a tunnel
                continue
            if isinstance(self.grid.get(width_pos, height_pos), LightSwitch):
                # Do not place water on lightswitch
                continue
            if isinstance(self.grid.get(width_pos + 1, height_pos), Door) or isinstance(self.grid.get(width_pos - 1, height_pos), Door):
                # Do not place water front a door
                continue
            if isinstance(self.grid.get(width_pos,height_pos),Door):
                # Do not place water on Door
                continue
            self.grid.set(width_pos, height_pos, Water())
        
            if self.grid_size < 10 and 2 > 0:
                placed_water_tiles = 2
            else:
                placed_water_tiles += 1
        
        if True:
            # transfert the position of the objects in the room in tha dark for visual  
            tab = self.saveElements(self.roomList[1])
            switchRoom.elements_in_room(tab)
                
        self.mission = ""

    def step(self,action):
        # Reset if agent step on water without knowing it
        if action == self.actions.forward and self.worldobj_in_agent(1,0) == "water" :
            return self.gen_obs(), 0, True, "died"
        else:
            return super().step(action)

class RandomEnv16x16_9660(RandomEnv):
    def __init__(self):
        super().__init__(size=16)

register(
    id='MiniGrid-RandomEnv-16x16-9660-v0',
    entry_point='gym_minigrid.envs:RandomEnv16x16_9660'
)
