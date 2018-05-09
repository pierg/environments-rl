from gym_minigrid.minigrid import *

def extended_dic(obj_names=[]):
    """
    Extend the OBJECT_TO_IDX dictionaries with additional objects
    :param obj_names: list of strings
    :return: OBJECT_TO_IDX extended
    """
    latest_key = list(OBJECT_TO_IDX)[-1]
    latest_idx = OBJECT_TO_IDX[latest_key]
    new_obj_idx = latest_idx + 1
    for obj_name in obj_names:
        OBJECT_TO_IDX.update({obj_name: new_obj_idx})
        new_obj_idx = new_obj_idx + 1


extended_dic(["water"])
IDX_TO_OBJECT = dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys()))

extended_dic(["lightswitch"])
IDX_TO_OBJECT = dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys()))


extended_dic(["None"])
IDX_TO_OBJECT = dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys()))

class Water(WorldObj):
    def __init__(self):
        super(Water, self).__init__('water', 'blue')

    def can_overlap(self):
        return True

    def render(self, r):
        self._set_color(r)
        r.drawPolygon([
            (0         , CELL_PIXELS),
            (CELL_PIXELS, CELL_PIXELS),
            (CELL_PIXELS,           0),
            (0          ,           0)
        ])
class ShadowRoom(WorldObj):
    def __init__(self,color='yellow',coordinates=None,is_open=False):
        super(ShadowRoom, self).__init__('None', color)
        self.coordinates=coordinates
        self.is_open=is_open

    def can_overlap(self):
        return True

    def toggle(self, env, pos):
        if isinstance(env.carrying, Lightswitch) and env.carrying.color == self.color:
            self.is_open = True
            env.carrying = None
            return True
        return False

    def render(self, r):
        self._set_color(r)
        (xmin,ymin,width,height,xenter,yenter)=self.coordinates
        if self.is_open==False:
            r.fillRect((xmin-xenter)*(CELL_PIXELS),(ymin-yenter)*(CELL_PIXELS), width*CELL_PIXELS, height*CELL_PIXELS,0,0,0)
        else:
            r.pop



class Lightswitch(WorldObj):
    def __init__(self,color='yellow'):
        super(Lightswitch, self).__init__('None', color)
    def can_pickup(self):
        return True
    def render(self, r):
        self._set_color(r)
        r.drawPolygon([
            (0, CELL_PIXELS),
            (CELL_PIXELS, CELL_PIXELS),
            (CELL_PIXELS, 0),
            (0, 0),
        ])

def worldobj_name_to_object(worldobj_name):
    if worldobj_name == 'water':
        return Water()
    elif worldobj_name == 'wall':
        return Wall()
    elif worldobj_name == 'lightswitch':
        return Lightswitch()
    else:
        return None

class ExGrid(Grid):
    """
    Extending Grid methods to support the new objects
    """

    # Add new worldobje that need to be decoded (Ex. water)
    def decode(array):
        """
        Decode an array grid encoding back into a grid
        """
        width = array.shape[0]
        height = array.shape[1]
        assert array.shape[2] == 3

        grid = ExGrid(width, height)

        for j in range(0, height):
            for i in range(0, width):

                typeIdx  = array[i, j, 0]
                colorIdx = array[i, j, 1]
                openIdx  = array[i, j, 2]

                if typeIdx == 0:
                    continue

                objType = IDX_TO_OBJECT[typeIdx]
                color = IDX_TO_COLOR[colorIdx]
                print(color)
                is_open = True if openIdx == 1 else 0
                if objType == 'wall':
                    v = Wall(color)
                elif objType == 'ball':
                    v = Ball(color)
                elif objType == 'key':
                    v = Key(color)
                elif objType == 'box':
                    v = Box(color)
                elif objType == 'door':
                    v = Door(color, is_open)
                elif objType == 'locked_door':
                    v = LockedDoor(color, is_open)
                elif objType == 'goal':
                    v = Goal()
                elif objType == 'water':
                    v = Water()
                elif objType == 'lightswitch':
                    v = Lightswitch()
                elif objType == 'None':
                    v = ShadowRoom()
                else:
                    assert False, "unknown obj type in decode '%s'" % objType

                grid.set(i, j, v)

        return grid


class ExMiniGridEnv(MiniGridEnv):
    # Enumeration of possible actions
    class Actions(IntEnum):
        # Turn left, turn right, move forward
        left = 0
        right = 1
        forward = 2

        # Pick up an object
        pickup = 3
        # Drop an object
        drop = 4
        # Toggle/activate an object
        toggle = 5

        # Wait/stay put/do nothing
        wait = 6

        # More actions:
        # Ex:
        clean = 7


    def worldobj_in_front_agent(self, distance=1):
        """
        Returns the type of the worldobj in the cell in front of the agent
        :param distance: integer, how many cells in front
        :return: string: worldobj type
        """
        ax, ay = self.agent_pos
        wx, wy = ax, ay

        worldobj = None

        # agent facing down
        if self.agent_dir == 1:
            wy += distance
        # agent facing right
        elif self.agent_dir == 0:
            wx += distance
        # agent facing left
        elif self.agent_dir == 2:
            wx -= distance
        # agent facing up
        elif self.agent_dir == 3:
            wy -= distance

        if wx >= 0 and wx < self.grid.width and wy >=0 and wy < self.grid.height:
            worldobj = self.grid.get(wx, wy)

            if worldobj is not None:
                worldobj_type = worldobj.type
                print("front_" + str(distance) + ": " + worldobj_type)
                return worldobj_type
        return None


    def worldobj_in_right_agent(self, distance=1):
        """
        Returns the type of the worldobj in the cell in right of the agent
        :param distance: integer, how many cells in right
        :return: string: worldobj type
        """
        ax, ay = self.agent_pos
        ad = self.agent_dir
        wx, wy = ax, ay

        worldobj = None

        # agent facing down
        if self.agent_dir == 1:
            wx -= distance
        # agent facing right
        elif self.agent_dir == 0:
            wy += distance
        # agent facing left
        elif self.agent_dir == 2:
            wy -= distance
        # agent facing up
        elif self.agent_dir == 3:
            wx += distance

        if wx >= 0 and wx < self.grid.width and wy >= 0 and wy < self.grid.height:
            worldobj = self.grid.get(wx, wy)

            if worldobj is not None:
                worldobj_type = worldobj.type
                print("right_" + str(distance) + ": " + worldobj_type)
                return worldobj_type
        return None

    def worldobj_in_left_agent(self, distance=1):
        """
        Returns the type of the worldobj in the cell in left of the agent
        :param distance: integer, how many cells in left
        :return: string: worldobj type
        """
        ax, ay = self.agent_pos
        ad = self.agent_dir
        wx, wy = ax, ay

        worldobj = None

        # agent facing down
        if self.agent_dir == 1:
            wx += distance
        # agent facing right
        elif self.agent_dir == 0:
            wy -= distance
        # agent facing left
        elif self.agent_dir == 2:
            wy += distance
        # agent facing up
        elif self.agent_dir == 3:
            wx -= distance

        if wx >= 0 and wx < self.grid.width and wy >= 0 and wy < self.grid.height:
            worldobj = self.grid.get(wx, wy)

            if worldobj is not None:
                worldobj_type = worldobj.type
                print("left_" + str(distance) + ": " + worldobj_type)
                return worldobj_type
        return None

    def get_grid_coords_from_view(self,coordinates):
        """
        Dual of "get_view_coords". Translate and rotate relative to the agent coordinates (i, j) into the
        absolute grid coordinates.
        Need to have tuples of integers for the position of the agent and its direction
        :param coordinates: tuples of integers (horizontal,vertical) position from the agent relative to its position
        :return : coordinates translated into the absolute grid coordinates.
        """
        ax, ay = self.agent_pos
        ad = self.agent_dir
        x,y = coordinates
        # agent facing down
        if ad == 1:
            ax -= x
            ay += y
        # agent facing right
        elif  ad == 0:
            ax += y
            ay += x
        # agent facing left
        elif ad == 2:
            ax -= y
            ay -= x
        # agent facing up
        elif ad == 3:
            ax += x
            ay -= y
        return ax,ay


    def worldobj_in_agent(self, front, side):
        """
        Returns the type of the worldobject in the 'front' cells in front and 'side' cells right (positive) or left (negative)
        with respect to the agent
        :param front: integer representing the number of cells in front of the agent
        :param side: integer, if positive represents the cells to the right, negative to the left of the agent
        :return: string: worldobj type
        """

        coordinates = (front,side)
        worldobj = None
        wx,wy = ExMiniGridEnv.get_grid_coords_from_view(self,coordinates)

        if wx >= 0 and wx < self.grid.width and wy >= 0 and wy < self.grid.height:
            worldobj = self.grid.get(wx, wy)

            if worldobj is not None:
                worldobj_type = worldobj.type
                print("worldobject located at : ["+front+" "+side+"] from agent is : " + worldobj_type)
                return worldobj_type
        return None

    def worldpattern_in_front_agent(self,object_type):
        if object_type == "pattern_deadend":
            print("deadend")
            return self.deadend_in_front_agent()
        else :
            return False

    def worldpattern_is_near_agent(self,object_type):
        if object_type == "pattern_deadend":
            print("deadend")
            return self.deadend_is_near_agent()
        else :
            return False

    def deadend_in_front_agent(self):
        i = 1
        while i < 4:
            coordinates = (0,i)
            wx,wy = ExMiniGridEnv.get_grid_coords_from_view(self,coordinates)
            if wx >= 0 and wx < self.grid.width and 0 <= wy < self.grid.height:
                worldpattern = self.grid.get(wx,wy)
            if worldpattern is not None:
                print("ici ",worldpattern)
                if worldpattern is Goal:
                    return False
                if i == 1:
                    coordinates = (-1,0)
                    wx,wy = ExMiniGridEnv.get_grid_coords_from_view(self,coordinates)
                    if wx >= 0 and wx < self.grid.width and 0 <= wy < self.grid.height:
                        worldpattern = self.grid.get(wx, wy)
                    coordinates = (-1,0)
                    wx,wy = ExMiniGridEnv.get_grid_coords_from_view(self,coordinates)
                    if wx >= 0 and wx < self.grid.width and 0 <= wy < self.grid.height:
                        worldpattern2 = self.grid.get(wx, wy)
                    print("ici2",worldpattern,worldpattern2)

                    if worldpattern is not None and worldpattern2 is not None:
                        return True
                else :# Maybe check side?
                    j = 1
                    while j < i:
                        coordinates = (1,j)
                        wx1,wy1 = ExMiniGridEnv.get_grid_coords_from_view(self,coordinates)
                        coordinates = (-1,j)
                        wx2,wy2 = ExMiniGridEnv.get_grid_coords_from_view(self, coordinates)
                        if wx1 >= 0 and wx1 < self.grid.width and wy1 >= 0 and wy1 < self.grid.height:
                            worldpattern1 = self.grid.get(wx1, wy1)
                        if wx2 >= 0 and wx2 < self.grid.width and wy2 >= 0 and wy2 < self.grid.height:
                            worldpattern2 = self.grid.get(wx2, wy2)
                        if worldpattern1 is Goal or worldpattern2 is Goal:
                            print("found goal")
                            return False
                        if worldpattern1 is None or worldpattern2 is None:
                            return False
                        j = j+1
                    return True
            i = i+1
        return False

    def deadend_is_near_agent(self):
        i = 1
        if self.deadend_in_front_agent() :
            return False
        while i < 3 :
            coordinates = (1, i)
            wx1, wy1 = ExMiniGridEnv.get_grid_coords_from_view(self, coordinates)
            coordinates = (-1, i)
            wx2, wy2 = ExMiniGridEnv.get_grid_coords_from_view(self, coordinates)
            if wx1 >= 0 and wx1 < self.grid.width and wy1 >= 0 and wy1 < self.grid.height:
                worldpattern1 = self.grid.get(wx1, wy1)
            if wx2 >= 0 and wx2 < self.grid.width and wy2 >= 0 and wy2 < self.grid.height:
                worldpattern2 = self.grid.get(wx2, wy2)
            if worldpattern1 is None or worldpattern2 is None:
                return False
            i = i+1
        return True

