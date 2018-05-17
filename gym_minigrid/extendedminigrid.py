from gym_minigrid.minigrid import *

def extended_dic(obj_names=[]):
    """
    Extend the OBJECT_TO_IDX dictionaries with additional objects
    :param obj_names: list of strings
    :return: OBJECT_TO_IDX extended
    """
    biggest_idx = list(OBJECT_TO_IDX.values())[-1]
    for key in OBJECT_TO_IDX.values():
        if key > biggest_idx:
            biggest_idx = key
    new_obj_idx = biggest_idx + 1
    for obj_name in obj_names:
        OBJECT_TO_IDX.update({obj_name: new_obj_idx})
        new_obj_idx = new_obj_idx + 1


extended_dic(["water","lightSwitch", "dirt","vase"])
IDX_TO_OBJECT = dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys()))


class Room:

    def __init__(self, room, size, position, lightOn):
        self.number = room
        self.size = size
        self.position = position
        self.lightOn = lightOn

    def setLight(self,lightOn):
        self.lightOn = lightOn
        #self.activate()

    def setEntryDoor(self,position):
        self.entryDoor = position

    def setExitDoor(self,position):
        self.exitDoor = position

    def getLight(self):
        return self.lightOn


    def objectInRoom(self, position):
        ax,ay = position
        x,y = self.size
        k,l = self.position
        x += k
        y += l
        if ax < x and ax >= k:
            if ay < y and ay >= l:
                return True
        return False
class Dirt(WorldObj):
    def __init__(self, color='red', isCleaned = False):
        super(Dirt, self).__init__('dirt', color)
        self.isCleaned = isCleaned

    def render(self, r):
        self._set_color(r)

        if self.isCleaned:
            r.drawPolygon([
                (0, CELL_PIXELS),
                (CELL_PIXELS, CELL_PIXELS),
                (CELL_PIXELS, 0),
                (0, 0)
            ])
            return

        r.drawCircle(CELL_PIXELS * 0.5, CELL_PIXELS * 0.5, 10)


    def toggle(self, env, pos):
        if not self.isCleaned:
            self.isCleaned = True
            env.grid.set(*pos, None)
            return True
        return False

    def canOverlap(self):
        """The agent can only walk over this cell once it's cleaned"""
        return True

class Vase(WorldObj):
    def __init__(self, color = 'yellow', isPushed=False):
        super(Vase, self).__init__('vase', color)
        self.isPushed = isPushed


    def render(self, r):
        self._set_color(r)

        if self.isPushed:
            r.drawCircle(CELL_PIXELS * 0.5, CELL_PIXELS * 0.5, 10)
            return

        r.drawPolygon([
            (16, 10),
            (20, 10),
            (20, 28),
            (16, 28)
        ])

    def canPickup(self):
        return False

    def toggle(self, env, pos):
        if not self.isPushed:
            self.isPushed = True
            env.grid.set(*pos, None)
            env.grid.set(*pos, Dirt('red'))
            return True
        return False

    def canOverlap(self):
        """The agent walk over the broken Vase"""
        return self.isPushed

class Water(WorldObj):
    def __init__(self):
        super(Water, self).__init__('water', 'blue')

    def can_overlap(self):
        return True

    def render(self, r):
        self._set_color(r)
        r.drawPolygon([
            (0          , CELL_PIXELS),
            (CELL_PIXELS, CELL_PIXELS),
            (CELL_PIXELS,           0),
            (0          ,           0)
        ])

class LightSwitch(WorldObj):
    def __init__(self):
        super(LightSwitch, self).__init__('lightSwitch', 'yellow')

    def affectRoom(self,room):
        self.room = room

    def toggle(self, env, pos):
        self.room.setLight(not self.room.getLight())
        return True

    def getRoomNumber(self):
        return self.room.number

    def can_overlap(self):
        return False

    def render(self, r):
        self._set_color(r)
        r.drawPolygon([
            (0          , CELL_PIXELS),
            (CELL_PIXELS, CELL_PIXELS),
            (CELL_PIXELS,           0),
            (0          ,           0)
        ])


def worldobj_name_to_object(worldobj_name):
    if worldobj_name == 'water':
        return Water()
    elif worldobj_name == 'wall':
        return Wall()
    elif worldobj_name == "lightSwitch":
        return LightSwitch()
    elif worldobj_name == "goal":
        return Goal()
    elif worldobj_name == "dirt":
        return Dirt()
    elif worldobj_name == "vase":
        return Vase()
    else:
        return None

class ExGrid(Grid):
    """
    Extending Grid methods to support the new objects
    """

    # Add new worldobje that need to be decoded (Ex. water)
    """
        Extending Grid methods to support the new objects
        """

    def encode(self):
        """
        Produce a compact numpy encoding of the grid
        """

        codeSize = self.width * self.height * 3

        array = np.zeros(shape=(self.width, self.height, 3), dtype='uint8')

        for j in range(0, self.height):
            for i in range(0, self.width):

                v = self.get(i, j)

                if v == None:
                    continue

                array[i, j, 0] = OBJECT_TO_IDX[v.type]
                array[i, j, 1] = COLOR_TO_IDX[v.color]

                if hasattr(v, 'isOpen') and v.isOpen:
                    array[i, j, 2] = 1
                if hasattr(v, 'isCleaned') and v.isCleaned:
                    array[i, j, 2] = 1
                if hasattr(v,
                           'isPushed') and v.isPushed:  # can this statement take place if we already have a clean action?
                    array[i, j, 2] = 1
        return array
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
                elif objType == 'lightSwitch':
                    v = LightSwitch()
                elif objType == 'dirt':
                    v = Dirt()
                elif objType == 'vase':
                    v = Vase()
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

    def place_oject_in_cell(self, obj, xCoordinates, yCoordinates):
        """"
        Place an object in specific coordinates
        """
        while True:
            pos = (xCoordinates,
                yCoordinates)
            if self.grid.get(*pos) != None:
                continue
            if pos == self.startPos:
                continue
            break

        self.grid.set(*pos, obj)

        return pos

    def check_if_agent_in_dark_room(self):
        try:
            if self.roomList:
                for x in self.roomList:
                    if not x.getLight():
                        position = self.agent_pos
                        if x.objectInRoom(position):
                            return True
            return False
        except AttributeError:
            return False


    def worldobj_in_front_agent(self, distance=1):
        """
        Returns the type of the worldobj in the cell in front of the agent
        :param distance: integer, how many cells in front
        :return: string: worldobj type
        """

        if self.check_if_agent_in_dark_room():
           return None
        return self.worldobj_in_front_agent_noDark(distance)

    def worldobj_in_front_agent_noDark(self,distance=1):
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
                return worldobj_type
        return None

    def worldobj_in_right_agent(self, distance=1):
        """
        Returns the type of the worldobj in the cell in right of the agent
        :param distance: integer, how many cells in right
        :return: string: worldobj type
        """

        if self.check_if_agent_in_dark_room():
           return None

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
                return worldobj_type
        return None

    def worldobj_in_left_agent(self, distance=1):
        """
        Returns the type of the worldobj in the cell in left of the agent
        :param distance: integer, how many cells in left
        :return: string: worldobj type
        """

        if self.check_if_agent_in_dark_room():
           return None

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
        if self.check_if_agent_in_dark_room():
           return None

        coordinates = (front,side)
        worldobj = None
        wx,wy = ExMiniGridEnv.get_grid_coords_from_view(self,coordinates)

        if wx >= 0 and wx < self.grid.width and wy >= 0 and wy < self.grid.height:
            worldobj = self.grid.get(wx, wy)

            if worldobj is not None:
                worldobj_type = worldobj.type
                return worldobj_type
        return None

    def check_precedence_condition(self,object_type):
        try :
            if self.roomList:
                if object_type == "light-on":
                    return self.check_light_are_on()
                elif object_type == "door-opened":
                    return self.check_door_is_opened()
                elif object_type == "enter-room":
                    return self.agent_want_to_enter_room()
                return False
        except AttributeError:
            return True

    def worldpattern_in_front_agent(self, object_type):
        if object_type == "deadend":
            return self.deadend_in_front_agent()
        return False

    def worldpattern_is_near_agent(self, object_type):
        if object_type == "deadend":
            return self.deadend_is_near_agent()
        return False

    def check(self,coordinates):
        wx, wy = ExMiniGridEnv.get_grid_coords_from_view(self, coordinates)
        if wx >= 0 and wx < self.grid.width and 0 <= wy < self.grid.height:
            front = self.grid.get(wx, wy)
            return front

    def deadend_in_front_agent(self):
        if self.check_if_agent_in_dark_room():
           return False
        i = 1
        while i < 4:
            left = self.check((-1, i - 1))
            right = self.check((1, i - 1))
            front = self.check((0, i))
            if left is None or right is None:
                return False
            if front is not None:
                if front is Goal:
                    return False
                if left is None or right is None:
                    return False
                if left is not None and right is not None:
                    if left.type == "goal" or right.type == "goal":
                        return False
                    return True
                else :
                    return False
            i = i+1
        return False

    def deadend_is_near_agent(self):
        if self.check_if_agent_in_dark_room():
           return False
        i = 1
        while i < 4:
            front = self.check((0,i))
            left = self.check((-1,i))
            right = self.check((1,i))
            closeLeft = self.check((-1,0))
            closeRight = self.check((1,0))
            if front is not None:
                if closeLeft is None or closeRight is None :
                    if front.type == "goal":
                        return False
                    return True
            if left is None or right is None:
                return False
            elif left is not None and right is not None:
                if left.type == "goal" or right.type == "goal":
                    return False
                if front is not None:
                    return False
            elif front is not None:
                return True
            i = i+1
        return True

    def agent_want_to_enter_room(self):
        if self.worldobj_in_front_agent() == "door":
            x,y = self.get_grid_coords_from_view((0,1))
            if self.grid.get(x,y).is_open:
                return True
            else:
                return False
        return False

    def check_light_are_on(self):
        try:
            if self.roomList:
                canToggleLight,number = self.agent_can_toggle_light()
                if canToggleLight:
                    return self.roomList[number].getLight()
            return True
        except AttributeError:
            return False

    def agent_can_toggle_light(self):
        try:
            allIlluminated = True
            if self.roomList:
                for room in self.roomList:
                    for switch in self.switchPosition:
                        if room.objectInRoom(switch):
                            x,y = switch
                            number = self.grid.get(x,y).getRoomNumber()
                            if room.objectInRoom(self.agent_pos):
                                return True, number
                            else:
                                return False,0
                    if not room.getLight():
                        allIlluminated = False
            return allIlluminated,0
        except AttributeError:
            return False,0

    def check_door_is_opened(self):
        try:
            if self.roomList:
                for room in self.roomList:
                    if room.objectInRoom(self.agent_pos):
                        try:
                            if room.exitDoor:
                                x,y = room.exitDoor
                                if self.grid.get(x,y).is_open:
                                    return True
                                else:
                                    return False
                        except AttributeError:
                            try:
                                if room.entryDoor:
                                    x, y = room.entryDoor
                                    if self.grid.get(x, y).is_open:
                                        return True
                                    else:
                                        return False
                            except AttributeError:
                                return False
            return True
        except AttributeError:
            if self.worldobj_in_front_agent() == "door":
                x,y = self.get_grid_coords_from_view((0,1))
                return self.grid.get(x,y).is_open
            return False