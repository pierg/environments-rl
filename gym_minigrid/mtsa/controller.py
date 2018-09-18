import logging
from sys import stdout
import os
from transitions import Machine
from configurations import config_grabber as cg
import random

class Controller(Machine):
    """
    MTSA Controller synthetised from safety properties
    """

    def __init__(self, name, type, perception):

        self.controller_name = name
        self.controller_type = type
        self.perception = perception

        # Grab configuration
        self.config = cg.Configuration.grab()

        # active, end, inactive
        self.controller_state = None

        self.observations = None

        self.tigger_action = None
        self.available_actions = None

        # The agent uses toggle for doors and light switch but the mtsa models does not
        self.is_toggle_a_switch = False

        # The agent uses toggle for dirt but the mtsa models does not
        self.is_toggle_a_clean = False

        states_path = os.path.abspath(os.path.dirname(__file__) + "/state_machines/" + self.controller_name + "_states.txt")
        transitions_path = os.path.abspath(os.path.dirname(__file__) + "/state_machines/" + self.controller_name + "_transitions.txt")

        # Loading the states
        with open(states_path, 'r') as inf:
            self.states = eval(inf.read())

        # Loading the transitions
        with open(transitions_path, 'r') as inf:
            self.transitions = eval(inf.read())

        # super().__init__("mtsa", self.states, self.transitions, 'S0M1', notify )
        Machine.__init__(self, states=self.states, transitions=self.transitions, initial='S0')


    def get_name(self):
        return self.controller_name

    def is_active(self):
        return self.controller_state is "active"
    

    def observe(self, observations):
        self.observations = observations
        self.fill_observations()
        if self.config.debug_mode:
            print(self.controller_name + "-" + self.controller_type + "   state: " + str(self.state) + "    obs: " + str([x for x in Controller.obs if Controller.obs[x] == True]))
        self.trigger('observation')

        # Get available actions
        available_actions = self.get_triggers(self.state)
        for action in available_actions[:]:
            if action.startswith('to_'):
                available_actions.remove(action)

        # Set controller active or not
        if "observation" in available_actions:
            self.set_state("S0")
            self.controller_state = "inactive"
        elif len(available_actions) == 0:
            self.set_state("S0")
            self.controller_state = "end"
        else:
            self.controller_state = "active"

        self.available_actions = available_actions


    def act(self, action):
        if self.is_active():
            self.tigger_action = action
            if action == 'toggle':
                safe_actions = set(["clean", "toggle", "switch"])
                safe_actions.intersection_update(self.available_actions)
                self.tigger_action = random.choice(list(safe_actions))
            self.trigger(self.tigger_action)



    def get_available_actions_for_agent(self):
        av_actions = self.available_actions[:]
        toggle_is_in = False
        for action in av_actions[:]:
            if action in ["clean", "toggle", "switch"]:
                id = av_actions.index(action)
                if toggle_is_in:
                    av_actions.remove(action)
                else:
                    av_actions[id] = 'toggle'
                    toggle_is_in = True
        return av_actions


    
    def fill_observations(self):
        Controller.obs["light-on-next-room"] = self.perception.is_condition_satisfied("light-on-next-room")
        Controller.obs["light-off-next-room"] = not self.perception.is_condition_satisfied("light-on-next-room")
        Controller.obs["door-opened"] = self.perception.is_condition_satisfied("door-opened-in-front") or self.perception.is_condition_satisfied("door-opened")
        Controller.obs["door-closed"] = self.perception.is_condition_satisfied("door-closed")
        Controller.obs["room-0"] = self.perception.is_condition_satisfied("room-0")
        Controller.obs["room-1"] = self.perception.is_condition_satisfied("room-1")
        Controller.obs["dirt-left"] = self.perception.at_left_is("dirt")
        Controller.obs["light-switch-left"] = self.perception.at_left_is("lightsw")
        Controller.obs["water-left"] = self.perception.at_left_is("water")
        Controller.obs["door-left"] = self.perception.at_left_is("door")
        Controller.obs["dirt-right"] = self.perception.at_right_is("dirt")
        Controller.obs["switch-right"] = self.perception.at_right_is("lightsw")
        Controller.obs["water-right"] = self.perception.at_right_is("water")
        Controller.obs["door-right"] = self.perception.at_right_is("door")
        Controller.obs["dirt-front"] = self.perception.in_front_of("dirt")
        Controller.obs["switch-front"] = self.perception.in_front_of("lightsw")
        Controller.obs["water-front"] = self.perception.in_front_of("water")
        Controller.obs["door-front"] = self.perception.in_front_of("door")
        Controller.obs["vase-left"] = self.perception.at_left_is("vase")
        Controller.obs["vase-front"] = self.perception.in_front_of("vase")
        Controller.obs["vase-right"] = self.perception.at_right_is("vase")
        Controller.obs["wall-left"] = self.perception.at_left_is("wall")
        Controller.obs["wall-front"] = self.perception.in_front_of("wall")
        Controller.obs["wall-right"] = self.perception.at_right_is("wall")
        Controller.obs["goal-left"] = self.perception.at_left_is("goal")
        Controller.obs["goal-front"] = self.perception.in_front_of("goal")
        Controller.obs["goal-right"] = self.perception.at_right_is("goal")



    obs = {
        "light-on-next-room": False,
        "light-off-next-room": False,
        "door-opened": False,
        "door-closed": False,
        "room-0": False,
        "room-1": False,
        "dirt-left": False,
        "light-switch-left": False,
        "water-left": False,
        "door-left": False,
        "dirt-right": False,
        "switch-right": False,
        "water-right": False,
        "door-right": False,
        "dirt-front": False,
        "switch-front": False,
        "water-front": False,
        "door-front": False,
        "vase-right": False,
        "vase-front": False,
        "vase-left": False,
        "wall-right": False,
        "wall-front": False,
        "wall-left": False,
        "goal-right": False,
        "goal-front": False,
        "goal-left": False
    }


    
    
    # State machine conditions

    def light_on(self):
        return Controller.obs["light-on-next-room"]

    def light_off(self):
        return Controller.obs["light-off-next-room"]

    def door_open(self):
        return Controller.obs["door-opened"]

    def door_close(self):
        return Controller.obs["door-closed"]

    def room_0(self):
        return Controller.obs["room-0"]

    def room_1(self):
        return Controller.obs["room-1"]

    def dirt_left(self):
        return Controller.obs["dirt-left"]

    def switch_left(self):
        return Controller.obs["light-switch-left"]

    def water_left(self):
        return Controller.obs["water-left"]

    def door_left(self):
        return Controller.obs["door-left"]

    def dirt_right(self):
        return Controller.obs["dirt-right"]

    def switch_right(self):
        return Controller.obs["switch-right"]

    def water_right(self):
        return Controller.obs["water-right"]

    def door_right(self):
        return Controller.obs["door-right"]

    def dirt_forward(self):
        return Controller.obs["dirt-front"]

    def switch_forward(self):
        return Controller.obs["switch-front"]

    def water_forward(self):
        return Controller.obs["water-front"]

    def door_forward(self):
        return Controller.obs["door-front"]

    def vase_left(self):
        return Controller.obs["vase-left"]

    def vase_right(self):
        return Controller.obs["vase-right"]

    def vase_forward(self):
        return Controller.obs["vase-front"]

    def wall_left(self):
        return Controller.obs["wall-left"]

    def wall_right(self):
        return Controller.obs["wall-right"]

    def wall_forward(self):
        return Controller.obs["wall-front"]

    def goal_left(self):
        return Controller.obs["goal-left"]

    def goal_right(self):
        return Controller.obs["goal-right"]

    def goal_forward(self):
        return Controller.obs["goal-front"]

