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
        if not obj_name in OBJECT_TO_IDX.keys():
            OBJECT_TO_IDX.update({obj_name: new_obj_idx})
            new_obj_idx = new_obj_idx + 1


extended_dic(["water","unsafe","lightSwitch","dirt","vase"])
IDX_TO_OBJECT = dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys()))


class Room:

    def __init__(self, room, size, position, lightOn):
        self.number = room
        self.size = size
        self.position = position
        self.lightOn = lightOn

    def setLight(self,lightOn):
        self.lightOn = lightOn

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
        if ax <= x and ax >= k:
            if ay <= y and ay >= l:
                return True
        return False


class Unsafe(WorldObj):
    def __init__(self):
        super(Unsafe, self).__init__('unsafe', 'yellow')

    def can_overlap(self):
        return True

    def toggle(self, env, pos):
        return True

    def render(self, r):
        self._set_color(r)
        t = CELL_PIXELS
        d = 0.2 * CELL_PIXELS
        e = (CELL_PIXELS + 2 * d)/18
        f = 0.85 * e
    
        r.drawPolygon([
            (d, t-d),  # A
            (t/2, t - d),  # B
            (t/2, t - d - 0.5 * e),  # Z
            (t/2 - f, t - d - 0.5 * e),  # C
            (t/2 - f, t - d - 2*e),  # D
            (t/2, t - d - 2*e),  # E
            (t/2, t - d - 3*e),  # F
            (t/2 - f, t - d - 3*e),  # G
            (t/2 - f, t - d - 6*e),  # H
            (t/2, t - d - 6*e),  # I
            (t/2, d)
        ])
        
        r.drawPolygon([
            (t - d, t - d),  # A
            (t/2, t - d),  # B
            (t/2, t - d - 0.5 * e),  # Z
            (t/2 + f, t - d - 0.5 * e),  # C
            (t/2 + f, t - d - 2*e),  # D
            (t/2, t - d - 2*e),  # E
            (t/2, t - d - 3*e),  # F
            (t/2 + f, t - d - 3*e),  # G
            (t/2 + f, t - d - 6*e),  # H
            (t/2, t - d - 6*e),  # I
            (t/2, d)  # J
        ])


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
        self.state = False
        super(LightSwitch, self).__init__('lightSwitch', 'yellow')

    def affectRoom(self,room):
        self.room = room

    def setSwitchPos(self,position):
        self.position = position

    def elements_in_room(self,room):
        self.elements = room

    def toggle(self, env, pos):
        self.room.setLight(not self.room.getLight())
        self.state = not self.state
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
        self.dark_light(r)

    def dark_light(self,r):

        if self.room.getLight() == False:
            r.setColor(255,0,0)
            r.drawCircle(0.5*CELL_PIXELS,0.5*CELL_PIXELS,0.2*CELL_PIXELS)
            if hasattr(self, 'position'):
                if hasattr(self, 'elements'):
                    (xl, yl) = self.position
                    for i in range(0,len(self.elements)):
                        if self.elements[i][2] == 1:
                            r.setLineColor(10, 10, 10)
                            r.setColor(10,10,10)
                            r.drawPolygon([
                                ((self.elements[i][0]-xl)*CELL_PIXELS, (self.elements[i][1]-yl+1)*CELL_PIXELS),
                                ((self.elements[i][0]-xl+1)*CELL_PIXELS,(self.elements[i][1]-yl+1)*CELL_PIXELS),
                                ((self.elements[i][0] - xl + 1) * CELL_PIXELS, (self.elements[i][1] - yl) * CELL_PIXELS),
                                ((self.elements[i][0] - xl) * CELL_PIXELS, (self.elements[i][1] - yl) * CELL_PIXELS)
                        ])
        else :
            r.setColor(0,255,0)
            r.drawCircle(0.5*CELL_PIXELS,0.5*CELL_PIXELS,0.2*CELL_PIXELS)
            r.pop

class Dirt(WorldObj):
    def __init__(self):
        super(Dirt, self).__init__('dirt', 'yellow')

    def can_overlap(self):
        return True

    def affect_list(self,list):
        self.list = list

    def toggle(self, env, pos):
        x,y = ExMiniGridEnv.get_grid_coords_from_view(env,(1,0))
        env.grid.set(x,y,None)
        del self.list[len(self.list)-1]
        return True

    def render(self,r):
        self._set_color(r)
        r.setColor(240 ,150 , 0)
        r.setLineColor(81, 41, 0)
        r.drawPolygon([
            (0, CELL_PIXELS),
            (CELL_PIXELS, CELL_PIXELS),
            (CELL_PIXELS, 0),
            (0, 0)
        ])


class Vase(WorldObj):
    def __init__(self):
        super(Vase, self).__init__('vase','grey')
        self.content = Dirt()
        self.list = []

    def can_overlap(self):
        return False

    def toggle(self, env, pos):
        x, y = ExMiniGridEnv.get_grid_coords_from_view(env, (1, 0))
        env.grid.set(x, y, self.content)
        self.list.append(Dirt())
        self.content.affect_list(self.list)

    def render(self,r):
        self._set_color(r)
        r.setColor(255,255,255)
        QUARTER_CELL = 0.25 * CELL_PIXELS
        DEMI_CELL = 0.5 * CELL_PIXELS
        r.drawCircle(DEMI_CELL,DEMI_CELL,DEMI_CELL)
        r.drawPolygon([
            (QUARTER_CELL, 3 * QUARTER_CELL),
            (3 * QUARTER_CELL, 3 * QUARTER_CELL),
            (3 * QUARTER_CELL, QUARTER_CELL),
            (QUARTER_CELL, QUARTER_CELL)
        ])
        r.setColor(240,150,0)
        r.drawPolygon([
            (0.32 * CELL_PIXELS, 0.7 * CELL_PIXELS),
            (0.7 * CELL_PIXELS, 0.7 * CELL_PIXELS),
            (0.7 * CELL_PIXELS, 0.32 * CELL_PIXELS),
            (0.32 * CELL_PIXELS, 0.32 * CELL_PIXELS)
        ])

    def list_dirt(self,list):
        self.list = list

def worldobj_name_to_object(worldobj_name):
    if worldobj_name == 'unsafe':
        return Unsafe()
    elif worldobj_name == 'water':
        return Water()
    elif worldobj_name == 'wall':
        return Wall()
    elif worldobj_name == "lightSwitch":
        return LightSwitch()
    elif worldobj_name == "dirt":
        return Dirt()
    elif worldobj_name == "vase":
        return Vase()
    elif worldobj_name == "goal":
        return Goal()
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
                elif objType == 'unsafe':
                    v = Unsafe()
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
        #pickup = 3
        # Drop an object
        #drop = 4
        # Toggle/activate an object
        #toggle = 5

        # Wait/stay put/do nothing
        #wait = 6

        # More actions:
        # Ex:
        #clean = 7

    def get_obs_render(self, obs):
        """
        Render an agent observation for visualization
        """

        if self.obs_render == None:
            self.obs_render = Renderer(
                AGENT_VIEW_SIZE * CELL_PIXELS // 2,
                AGENT_VIEW_SIZE * CELL_PIXELS // 2
            )

        r = self.obs_render

        r.beginFrame()

        grid = ExGrid.decode(obs)

        # Render the whole grid
        grid.render(r, CELL_PIXELS // 2)

        # Draw the agent
        r.push()
        r.scale(0.5, 0.5)
        r.translate(
            CELL_PIXELS * (0.5 + AGENT_VIEW_SIZE // 2),
            CELL_PIXELS * (AGENT_VIEW_SIZE - 0.5)
        )
        r.rotate(3 * 90)
        r.setLineColor(255, 0, 0)
        r.setColor(255, 0, 0)
        r.drawPolygon([
            (-12, 10),
            (12, 0),
            (-12, -10)
        ])
        r.pop()

        r.endFrame()

        return r.getPixmap()

    def gen_obs(self):
        """
        Generate the agent's view (partially observable, low-resolution encoding)
        """
        grid, vis_mask = self.gen_obs_grid()
        """if Perception.light_on_current_room(self):"""
        try:
            if self.roomList:
                for x in self.roomList:
                    if x.objectInRoom(self.agent_pos):
                        if not x.getLight():
                            for i in range(0, len(grid.grid)):
                                if grid.grid[i] is not None:
                                        grid.grid[i] = None
                            # Encode the partially observable view into a numpy array
                        image = grid.encode()

                        assert hasattr(self, 'mission'), "environments must define a textual mission string"

                        # Observations are dictionaries containing:
                        # - an image (partially observable view of the environment)
                        # - the agent's direction/orientation (acting as a compass)
                        # - a textual mission string (instructions for the agent)
                        obs = {
                            'image': image,
                            'direction': self.agent_dir,
                            'mission': self.mission
                        }
                        return obs
        except AttributeError:
            return super().gen_obs()

    def get_grid_coords_from_view(self,coordinates):
        """
        Dual of "get_view_coords". Translate and rotate relative to the agent coordinates (i, j) into the
        absolute grid coordinates.
        Need to have tuples of integers for the position of the agent and its direction
        :param coordinates: tuples of integers (vertical,horizontal) position from the agent relative to its position
        :return : coordinates translated into the absolute grid coordinates.
        """
        ax, ay = self.agent_pos
        ad = self.agent_dir
        x, y = coordinates
        # agent facing down
        if ad == 1:
            ax -= y
            ay += x
        # agent facing right
        elif  ad == 0:
            ax += x
            ay += y
        # agent facing left
        elif ad == 2:
            ax -= x
            ay -= y
        # agent facing up
        elif ad == 3:
            ax += y
            ay -= x
        return ax, ay

    def worldobj_in_agent(self, front, side):
        """
        Returns the type of the worldobject in the 'front' cells in front and 'side' cells right (positive) or left (negative)
        with respect to the agent
        :param front: integer representing the number of cells in front of the agent
        :param side: integer, if positive represents the cells to the right, negative to the left of the agent
        :return: string: worldobj type
        """

        coordinates = (front,side)
        wx, wy = ExMiniGridEnv.get_grid_coords_from_view(self,coordinates)

        if 0 <= wx < self.grid.width and 0 <= wy < self.grid.height:
            worldobj = self.grid.get(wx, wy)

            if worldobj is not None:
                worldobj_type = worldobj.type
                return worldobj_type
        return None