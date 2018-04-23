from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class EmptyEnv(MiniGridEnv):
    """
    Cleaning Environment where the agent to locates the dirt and cleans it. Works with the modified minigrid atm only. 
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
        types = ['key', 'dirt']

        objs = []
        objPos = []

        # Until we have generated all the objects
        while len(objs) < self.numObjs:
            objType = self._randElem(types)
            objColor = self._randElem(COLOR_NAMES)

            # If this object already exists, try again
            if (objType, objColor) in objs:
                continue

            if objType == 'key':
                obj = Key(objColor)
            elif objType == 'dirt':
                obj = Dirt('red')

            pos = self.placeObj(obj)
            objs.append((objType, objColor))
            objPos.append(pos)

        # Randomize the player start position and orientation
        self.placeAgent()

        # Choose the dirt objec
        objIdx = 0
        if objs[objIdx] == ('dirt', 'red'):
            pass
        else:
            objIdx = 1

        self.targetType, self.targetColor = objs[objIdx]
        self.targetPos = objPos[objIdx]

        self.mission = 'Clean'
        #print(self.mission)

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        ax, ay = self.agentPos
        tx, ty = self.targetPos

        # Reward if perform the cleaning action near to object
        if action == self.actions.clean:
            if abs(ax - tx) <= 1 and abs(ay - ty) <= 1:
                reward = 1
            done = True

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
