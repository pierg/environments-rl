import argparse
import json
from random import randint
from configurations.config_grabber import Configuration

parser = argparse.ArgumentParser(description='Arguments for creating the environments and its configuration')
parser.add_argument('--environment_file', type=str, required=False, help="A json file containing the keys: "
                                                                         "step, goal, near, immediate, violated. "
                                                                         "The values should be the wanted rewards "
                                                                         "of the actions")
parser.add_argument('--rewards_file', type=str, required=False, help="A json file containing the keys: "
                                                                     "step, goal, near, immediate, violated. "
                                                                     "The values should be the wanted rewards "
                                                                     "of the actions")

environment_path = "../gym-minigrid/gym_minigrid/envs/"
configuration_path = "configurations/"
random_token = randint(0, 9999)

""" This script creates a random environment in the gym_minigrid/envs folder. It uses a token_hex(4) 
        as the ID and the random seed for placing tiles in the grid.
    This to ensure that certain environments can be reproduced 
        in case the agent behaves strange in certain environments, in order to investigate why.        
"""


def generate_environment(environment="default", rewards="default"):
    elements = Configuration.grab("environments/" + environment)
    grid_size = elements.grid_size
    n_water = elements.n_water
    n_deadend = elements.n_deadend
    light_switch = elements.light_switch
    random_each_episode = elements.random_each_episode
    rewards = Configuration.grab("rewards/" + rewards)
    with open(environment_path + "randoms/" + "randomenv{0}.py".format(random_token), 'w') as env:
        env.write("""
from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register
import random
class RandomEnv(ExMiniGridEnv):
    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls= not {3}
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
        if {5}:
            width_pos, height_pos = self._rand_pos( xmin, xmax + 1, ymin, ymax + 1)
        else:
            width_pos = random.randint( xmin, xmax)
            height_pos = random.randint( ymin, ymax)
        return width_pos, height_pos

    def _random_number(self, min, max):
        if {5}:
            return self._rand_int(min,max+1)
        else:
            return random.randint(min,max)

    def _random_or_not_bool(self):
        if {5}:
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
        random.seed("{4}")

        #Place lightswitch
        lightswitch_is_posed = False
        test_goal = 0
        if width > 10:
            if {3}:
                while not lightswitch_is_posed:
                    width_pos , height_pos = self._random_or_not_position(2, width - 3, 2, height - 1)

                    #lightswitch and room wall must not replace a fundamental element (goal, key, ...)
                    continue_while = True
                    if isinstance(self.grid.get(width_pos, height_pos), Goal) or \
                     isinstance(self.grid.get(width_pos, height_pos), Key):
                        continue_while = False
                    for i in range(0,height):
                        if isinstance(self.grid.get(width_pos + 1, i), Goal) or \
                         isinstance(self.grid.get(width_pos + 1, i), Key):
                            continue_while = False
                            break
                    if not continue_while:
                        continue

                    switchRoom = LightSwitch()

                    #Place the wall
                    self.grid.vert_wall(width_pos+1, 1, height-2)

                    xdoor, ydoor = width_pos + 1, height_pos - 1
                    #Place the door
                    #if height_pos == 0 or height_pos == 1:
                        #xdoor, ydoor = width_pos + 1, height_pos + 1
                    #elif height_pos == height - 2 or height_pos == height - 1:
                        #xdoor, ydoor = width_pos + 1, height_pos - 1
                    #else:

                        #if self._random_or_not_bool():
                            #xdoor, ydoor = width_pos + 1, height_pos - 1
                        #else:
                            #xdoor, ydoor = width_pos + 1, height_pos + 1

                    self.grid.set(xdoor, ydoor , Door(self._rand_elem(sorted(set(COLOR_NAMES)))))

                    #Add the room
                    self.roomList = []
                    self.roomList.append(Room(0,(width_pos + 1, height),(0, 0),True))
                    self.roomList.append(Room(1,(width - width_pos - 2, height),(width_pos + 1, 0),False))
                    self.roomList[1].setEntryDoor((xdoor,ydoor))
                    self.roomList[0].setExitDoor((xdoor,ydoor))


                    #Place the lightswitch
                    switchRoom.affectRoom(self.roomList[1])
                    #switchRoom.setSwitchPos((width_pos,height_pos))

                    self.grid.set(width_pos, height_pos, switchRoom)
                    self.switchPosition = []
                    self.switchPosition.append((width_pos, height_pos))

                    lightswitch_is_posed = True
        # Place dead ends
        placed_dead_ends = 0
        tmp = self._random_number(0,3)
        while {2} > placed_dead_ends:
            if self.grid_size < 10:
                # Limit to one dead end if the grid is too small
                if self._random_or_not_bool():
                    self.grid.vert_wall(width//2-1,height//2,height//2)
                else:
                    self.grid.horz_wall(width//2,height//2-1,width//2)
                placed_dead_ends = {2}
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
        while {1} > placed_water_tiles:

            # Added to avoid a number of water tiles that is impossible (infinite loop)
            anti_loop +=1
            if anti_loop > 1000:
                placed_water_tiles = {1}
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

            if self.grid_size < 10 and {2} > 0:
                placed_water_tiles = {1}
            else:
                placed_water_tiles += 1

        #if lightswitch_is_posed:
            #if {3}:
                # transfert the position of the objects in the room in tha dark for visual  
                #tab = self.saveElements(self.roomList[1])
                #switchRoom.elements_in_room(tab)

        self.mission = ""
    def step(self,action):
        # Reset if agent step on water without knowing it
        if action == self.actions.forward and self.worldobj_in_agent(1,0) == "water" :
            return self.gen_obs(), {6}, True, "died"
        else:
            return super().step(action)
class RandomEnv{0}x{0}_{4}(RandomEnv):
    def __init__(self):
        super().__init__(size={0})
register(
    id='MiniGrid-RandomEnv-{0}x{0}-{4}-v0',
    entry_point='gym_minigrid.envs:RandomEnv{0}x{0}_{4}'
)
""".format(grid_size, n_water, n_deadend, light_switch, random_token, random_each_episode, rewards.standard.death))
        env.close()
    # Adds the import statement to __init__.py in the envs folder in gym_minigrid,
    # otherwise the environment is unavailable to use.
    with open(environment_path + "__init__.py", 'a') as init_file:
        init_file.write("\n")
        init_file.write("from gym_minigrid.envs.randoms.randomenv{0} import *".format(random_token))
        init_file.close()

    # Creates a json config file for the random environment
    with open(configuration_path + "randoms/" + "randomEnv-{0}x{0}-{1}-v0.json".format(grid_size, random_token),
              'w') as config:
        action_planning = {}
        if hasattr(elements,"action_planning"):
            unsafe = -0.3
            on_plan = 0.01
            off_plan = -0.15
            for current_monitor in rewards:
                if current_monitor == "action_planning":
                    unsafe = current_monitor.unsafe
                    on_plan = current_monitor.on_plan
                    off_plan = current_monitor.off_plan
            action_planning = {
                "active": True if elements.action_planning.active else False,
                "random_unsafe_obj":int("{0}".format(elements.action_planning.random_unsafe_obj)),
                "secondary_goals":"{0}".format(elements.action_planning.secondary_goals),
                "reward": {
                    "unsafe": float("{0:.2f}".format(unsafe)),
                    "on_plan": float("{0:.2f}".format(on_plan)),
                    "off_plan": float("{0:.2f}".format(off_plan)),
                }
            }

        json_object = json.dumps({
            "config_name": "randomEnv-{0}x{0}-{1}-v0".format(grid_size, random_token),
            "algorithm": "a2c",
            "env_name": "MiniGrid-RandomEnv-{0}x{0}-{1}-v0".format(grid_size, random_token),
            "num_processes": 48,
            "optimal_num_steps": int("{0}".format(elements.optimal_num_steps if hasattr(elements, 'optimal_num_steps') else (int("{0}".format(elements.grid_size))*int("{0}".format(elements.grid_size))//2))),
            "stop_after_update_number": 0,
            "num_steps": 4,
            "log_interval": 10,
            "on_violation_reset": False,
            "rendering": False,
            "stop_learning": int("{0}".format(elements.stop_learning)),
            "number_of_iteration": int("{0}".format(elements.number_of_iteration)),
            "evaluation_directory_name": "evaluations",
            "visdom": False,
            "debug_mode": False,
            "action_planning": {

            },
            "monitors": {
                "properties": {

                },
                "patterns": {

                }
            },
            "rewards": {
                "standard": {
                    "goal": float("{0:.2f}".format(rewards.standard.goal if hasattr(rewards.standard, 'goal') else 1)),
                    "step": float("{0:.2f}".format(rewards.standard.step if hasattr(rewards.standard, 'step') else 0)),
                    'death': float(
                        "{0:.2f}".format(rewards.standard.death if hasattr(rewards.standard, 'death') else -1))
                },
                "cleaningenv": {
                    "clean": float(
                        "{0:.2f}".format(rewards.cleaningenv.clean if hasattr(rewards.cleaningenv, 'clean') else 0.5))
                }
            }
        }, indent=2)

        d = {}
        daction_planning ={}

        for p in action_planning:
                daction_planning[p] = action_planning[p]
        d = json.loads(json_object)
        d['action_planning'].update(daction_planning)
        config.write(json.dumps(d, sort_keys=True, indent=2))
        config.close()

    return "randomEnv-{0}x{0}-{1}-v0.json".format(grid_size, random_token)


def main():
    args = parser.parse_args()
    environment = "default"
    rewards = "default"
    if args.rewards_file is not None:
        rewards = args.rewards_file
    if args.environment_file is not None:
        environment = args.environment_file
    file_name = generate_environment(environment, rewards)
    print(file_name)


if __name__ == '__main__':
    main()