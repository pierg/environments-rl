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
random_token = randint(0,9999)

""" This script creates a random environment in the gym_minigrid/envs folder. It uses a token_hex(4) 
        as the ID and the random seed for placing tiles in the grid.
    This to ensure that certain environments can be reproduced 
        in case the agent behaves strange in certain environments, in order to investigate why.        
"""

def generate_environment(environment="default", rewards="default"):
    elements = Configuration.grab("environments/"+environment)
    grid_size = elements.grid_size
    n_water = elements.n_water
    n_deadend = elements.n_deadend
    light_switch = elements.light_switch
    random_each_episode = False
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

        # Place a goal square in the top-right corner
        self.grid.set(width - 2, 1, Goal())

        # Set the random seed to the random token, so we can reproduce the environment
        random.seed("{4}")
        
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
        while {1} > placed_water_tiles:
        
            # Added to avoid a number of water tiles that is impossible (infinite loop)
            anti_loop +=1
            if anti_loop > 1000:
                placed_water_tiles = {1}
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
    with open(configuration_path + "randoms/" + "randomEnv-{0}x{0}-{1}-v0.json".format(grid_size, random_token), 'w') as config:
        list_of_json_patterns = {}
        patterns_map = {}
        if hasattr(elements,"monitors"):
            if hasattr(elements.monitors,"patterns"):
                for type in elements.monitors.patterns:
                    for monitor in type:
                        type_of_monitor = monitor.type
                        respected = 1
                        violated = -1
                        for current_monitor in rewards:
                            if hasattr(current_monitor,"name"):
                                if current_monitor.name == type_of_monitor:
                                    respected = current_monitor.respected
                                    violated = current_monitor.violated
                        list_of_json_patterns[monitor.name] = {
                                "{0}".format(monitor.name): {
                                    "type": "{0}".format(monitor.type),
                                    "mode": "{0}".format(monitor.mode),
                                    "active": True if monitor.active else False,
                                    "name": "{0}".format(monitor.name),
                                    "action_planner": "{0}".format(monitor.action_planner) if hasattr(monitor, "action_planner") else "wait",
                                    "conditions":"{0}".format(monitor.conditions) if not hasattr(monitor.conditions,"pre") else {
                                        "pre":"{0}".format(monitor.conditions.pre),
                                        "post":"{0}".format(monitor.conditions.post)
                                    },
                                    "rewards": {
                                        "respected": float(
                                             "{0:.2f}".format(respected)),
                                        "violated": float(
                                             "{0:.2f}".format(violated))
                                    }
                                }
                        }
                        if monitor.type in patterns_map:
                            patterns_map[monitor.type].append(monitor.name)
                        else:
                            patterns_map[monitor.type] = [monitor.name]

        json_object = json.dumps({
            "config_name": "randomEnv-{0}x{0}-{1}-v0".format(grid_size, random_token),
            "algorithm": "a2c",
            "env_name": "MiniGrid-RandomEnv-{0}x{0}-{1}-v0".format(grid_size, random_token),
            "controller": bool(elements.controller),
            "rendering": bool(elements.rendering),
            "recording": bool(elements.recording),
            "log_interval": int("{0}".format(elements.log_interval)),
            "max_num_frames": int("{0}".format(elements.max_num_frames)),
            "max_num_steps_episode": int("{0}".format(elements.max_num_steps_episode)),
            "debug_mode": bool(elements.debug_mode),
            "evaluation_directory_name": str(elements.evaluation_directory_name),
            "training_mode": bool(elements.training_mode),
            "agent_view_size": int("{0}".format(elements.agent_view_size)),
            "visdom": bool(elements.visdom),
            "a2c": {
                "algorithm": "a2c",
                "save_model_interval": int("{0}".format(elements.a2c.save_model_interval)),
                "num_processes": int("{0}".format(elements.a2c.num_processes)),
                "stop_learning": int("{0}".format(elements.a2c.stop_learning)),
                "optimal_num_step": int("{0}".format(elements.a2c.optimal_num_step)),
                "stop_after_update_number": int("{0}".format(elements.a2c.stop_after_update_number)),
                "num_steps": int("{0}".format(elements.a2c.num_steps)),
                "save_evaluation_interval": int("{0}".format(elements.a2c.save_evaluation_interval))
            },
            "dqn": {
                "exploration_rate": float("{0:.2f}".format(elements.dqn.exploration_rate)),
                "results_log_interval": int("{0}".format(elements.dqn.results_log_interval)),
                "epsilon_decay_episodes": int("{0}".format(elements.dqn.epsilon_decay_episodes)),
                "epsilon_final":  float("{0:.2f}".format(elements.dqn.epsilon_final)),
                "epsilon_decay_frame": int("{0}".format(elements.dqn.epsilon_decay_frame)),
                "epsilon_start": float("{0:.2f}".format(elements.dqn.epsilon_start)),
                "discount_factor": float("{0:.2f}".format(elements.dqn.discount_factor))
            },
            "monitors": {
                "patterns":{

                }
            },
            "rewards": {
                "actions": {
                    "forward": float("{0:.2f}".format(rewards.actions.forward if hasattr(rewards.actions,'forward') else 0))
                },
                "standard":{
                    "goal": float("{0:.2f}".format(rewards.standard.goal if hasattr(rewards.standard,'goal') else 1)),
                    "step": float("{0:.2f}".format(rewards.standard.step if hasattr(rewards.standard,'step')else 0)),
                    'death': float("{0:.2f}".format(rewards.standard.death if hasattr(rewards.standard,'death') else -1))
                },
                "cleaningenv":{
                    "clean":float("{0:.2f}".format(rewards.cleaningenv.clean if hasattr(rewards.cleaningenv,'clean') else 0.5))
                }
            }
        }, indent=2)

        d = {}
        dPatterns = {}

        for p in patterns_map:
            if isinstance(patterns_map[p],str):
                if p in dPatterns:
                    dPatterns[p].update(list_of_json_patterns[patterns_map[p]])
                else:
                    dPatterns[p] = list_of_json_patterns[patterns_map[p]]
            else:
                for value in patterns_map[p]:
                    if p in dPatterns:
                        dPatterns[p].update(list_of_json_patterns[value])
                    else:
                        dPatterns[p] = list_of_json_patterns[value]

        d = json.loads(json_object)
        d['monitors']['patterns'].update(dPatterns)
        config.write(json.dumps(d,sort_keys=True,indent=2))
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