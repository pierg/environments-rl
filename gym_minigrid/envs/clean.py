from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class EmptyEnv(MiniGridEnv):
    """
    Cleaning Environment where the agent to locates the dirt and cleans it
    """

    def __init__(
        self,
        size=8,
        numObjs=2
    ):
        self.numObjs = numObjs
        super().__init__(gridSize=size, maxSteps=5*size)
        self.reward_range = (-1, 1)

    def _genGrid(self, width, height):
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horzWall(0, 0)
        self.grid.horzWall(0, height-1)
        self.grid.vertWall(0, 0)
        self.grid.vertWall(width-1, 0)


        while True:
            pos = self._randPos(
                1, width-1,
                1, height-1
            )
            if pos == self.startPos:
                continue
            if self.grid.get(*pos) != None:
                continue
            self.grid.set(*pos, Key('yellow'))
            break

        while True:
            pos = self._randPos(
                1, width-1,
                1, height-1
            )
            if pos == self.startPos:
                continue
            if self.grid.get(*pos) != None:
                continue
            self.grid.set(*pos, Ball('red'))
            break



        # Randomize the player start position and orientation
        self.placeAgent()

        # Choose the target and the item
        target =  Ball('red')
        self.targetType = target.type
        self.targetColor = target.color
        item = Key('yellow')
        self.itemType = item.type
        self.itemColor = item.color
        # Generate the mission string
        self.mission = 'Clean the red dirt'

        assert hasattr(self, 'mission')

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        if self.carrying:
            if self.carrying.color == self.targetColor and \
               self.carrying.type == self.targetType:
                reward = 1
                done = True
            elif self.carrying.color == self.itemColor and \
                 self.carrying.type == self.itemType:
                reward = -1
                done = True
            else:
                reward = 0
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
