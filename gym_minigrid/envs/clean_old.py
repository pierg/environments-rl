from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class EmptyEnv(MiniGridEnv):
    """
    Cleaning Environment where the agent to locates the dirt and cleans it
    """

    def __init__(
        self,
        size=6,
        numObjs=2
    ):
        self.numObjs = numObjs
        super().__init__(gridSize=size, maxSteps=5*size)
        self.reward_range = (0, 1)

    def _genGrid(self, width, height):
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wallRect(0, 0, width, height)

        # Types and colors of objects we can generate
        types = ['vase', 'dirt']

        objs = []
        objPos = []

        # Until we have generated all the objects
        while len(objs) < self.numObjs:
            objType = self._randElem(types)
            objColor = self._randElem(COLOR_NAMES)

            # If this object already exists, try again
            if (objType, objColor) in objs:
                continue

            if objType == 'vase':
                obj = Vase(objColor)
            elif objType == 'dirt':
                obj = Dirt('red')

            pos = self.placeObj(obj)
            objs.append((objType, objColor))
            objPos.append(pos)

        # Randomize the player start position and orientation
        self.placeAgent()

        # Force the dirt to be the target and vase to be the item
        objTargetIdx = 0
        objItemIdx = 1
        if objs[objTargetIdx] == ('dirt', 'red'):
            pass
        else:
            objTargetIdx = 1
            objItemIdx = 0

        self.targetType, self.targetColor = objs[objTargetIdx]
        self.targetPos = objPos[objTargetIdx]
        self.itemType, self.itemColor = objs[objItemIdx]
        self.itemPos = objPos[objItemIdx]

        self.mission = 'Clean'
        #print(self.mission)

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        ax, ay = self.agentPos
        tx, ty = self.targetPos
        ix, iy = self.itemPos

        # Reward if perform the cleaning action near to object
        if action == self.actions.clean:
            if abs(ax - tx) <= 1 and abs(ay - ty) <= 1:
                reward = 1
            done = True
        elif action == self.actions.breakVase:
            if abs(ax - ix) <= 1 and abs(ay - iy) <= 1:
        # Here the removal of the Vase should take place and replace it with a Dirt('red') item
                pass
        return obs, reward, done, info

class EmptyEnv6x6(EmptyEnv):
    def __init__(self):
        super().__init__(size=6)

class EmptyEnv16x16(EmptyEnv):
    def __init__(self):
        super().__init__(size=16)

register(
    id='MiniGrid-Empty-6x6-v0',
    entry_point='gym_minigrid.envs:EmptyEnv6x6'
)

register(
    id='MiniGrid-Empty-8x8-v0',
    entry_point='gym_minigrid.envs:EmptyEnv'
)

register(
    id='MiniGrid-Empty-16x16-v0',
    entry_point='gym_minigrid.envs:EmptyEnv16x16'
)
