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


extended_dic(['dirt', 'vase'])
IDX_TO_OBJECT = dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys()))

class Dirt(WorldObj):
    def __init__(self, color='red', isCleaned = False):
        super(Dirt, self).__init__('dirt', color)
        self.isCleaned = isCleaned

    def render(self, r):
        self._setColor(r)

        if self.isCleaned:
            r.drawPolygon([
                (0, CELL_PIXELS),
                (CELL_PIXELS, CELL_PIXELS),
                (CELL_PIXELS, 0),
                (0, 0)
            ])
            return

        r.drawCircle(CELL_PIXELS * 0.5, CELL_PIXELS * 0.5, 10)


    def canClean(self, env, pos):
        if not self.isCleaned:
            self.isCleaned = True
            #env.grid.set(*pos, None) Not sure about this though. I need a way to remove the dirt from the grid.
            return True
        return False

    def canOverlap(self):
        """The agent can only walk over this cell once it's cleaned"""
        return True

class Vase(WorldObj):
    def __init__(self, color, isBroken=False, isCleaned=False):
        super(Vase, self).__init__('vase', color)
        self.isPushed = isBroken
        self.isCleaned = isCleaned

    def render(self, r):
        self._setColor(r)

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

    def canPush(self, env, pos):
        if not self.isPushed:
            self.isPushed = True
            # Again here I need to find a way to remove the Vase from the grid so I can introduce the dirt in it's place.
            # For now I will leave it on the grid and use the option to be cleaned once it's broken
            return True
        return False

    def canOverlap(self):
        """The agent walk over the broken Vase"""
        return self.isPushed

    def canClean(self, env, pos):
        if self.isPushed:
            self.isCleaned = True
            return True
        return False

class ExGrid(Grid):
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
                if hasattr(v, 'isBroken') and v.isBroken:#can this statement take place if we already have a clean action?
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
                isCleaned = True if openIdx == 1 else 0  # Added code
                isPushed = True if openIdx == 1 else 0  # Added code

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
                elif objType == 'dirt':
                    v = Dirt(color, isCleaned)
                elif objType == 'vase':
                    v = Vase(color, isPushed, isCleaned)
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
        clean = 7
        move = 8

    def step(self, action):
        if action == self.actions.clean:
            u, v = self.getDirVec()
            objPos = (self.agentPos[0] + u, self.agentPos[1] + v)
            cell = self.grid.get(*objPos)
            if cell and cell.canClean:
                cell.canClean(self, objPos)
        elif action == self.actions.move:
            u, v = self.getDirVec()
            objPos = (self.agentPos[0] + u, self.agentPos[1] + v)
            cell = self.grid.get(*objPos)
            if cell:
                cell.canPush(self, objPos)
        else:
            super().step(action)



