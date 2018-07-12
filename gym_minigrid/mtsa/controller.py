from gym_minigrid.perception import Perception as p
import logging
from sys import stdout
import os
from transitions import Machine

class Controller(Machine):
    """
    MTSA Controller synthetised from safety properties
    """

    states = []
    transitions = []

    def __init__(self):
        self.observations = None

        self.tigger_action = None

        # The agent uses toggle for doors and light switch but the mtsa models does not
        self.is_toggle_a_switch = False

        states_path = os.path.abspath(os.path.dirname(__file__) + "/states.txt")
        transitions_path = os.path.abspath(os.path.dirname(__file__) + "/transitions.txt")

        # Loading the states
        with open(states_path, 'r') as inf:
            self.states = eval(inf.read())

        # Loading the transitions
        with open(transitions_path, 'r') as inf:
            self.transitions = eval(inf.read())

        # super().__init__("mtsa", self.states, self.transitions, 'S0M1', notify)
        Machine.__init__(self, states=self.states, transitions=self.transitions, initial='S0M1')

    def logger(self, message):
        print(message)
    

    def observe(self, observations):
        self.observations = observations
        self.fill_observations()
        print("state: " + str(self.state) + "    obs: " + str([x for x in Controller.obs if Controller.obs[x] == True]))
        self.trigger('observation')

    def act(self, action):
        self.tigger_action = action
        if action == 'toggle':
            if self.is_toggle_a_switch:
                self.tigger_action = 'switch'
                self.is_toggle_a_switch = False
        self.trigger(self.tigger_action)

    def get_available_actions(self):
        available_actions = self.get_triggers(self.state)
        for action in available_actions[:]:
            if action.startswith('to_'):
                available_actions.remove(action)
            if action == ('switch'):
                id = available_actions.index(action)
                available_actions[id] = 'toggle'
                self.is_toggle_a_switch = True
        return available_actions

    
    def fill_observations(self):
        Controller.obs["light-on-next-room"] = p.is_condition_satisfied(self.observations, "light-on-next-room")
        Controller.obs["light-off-next-room"] = not p.is_condition_satisfied(self.observations, "light-on-next-room")
        Controller.obs["door-opened"] = p.is_condition_satisfied(self.observations, "door-opened-in-front") or p.is_condition_satisfied(self.observations, "door-opened")
        Controller.obs["door-closed"] = p.is_condition_satisfied(self.observations, "door-closed")
        Controller.obs["room-0"] = p.is_condition_satisfied(self.observations, "room-0", self.tigger_action)
        Controller.obs["room-1"] = p.is_condition_satisfied(self.observations, "room-1", self.tigger_action)
        Controller.obs["dirt-left"] = p.at_left_is(self.observations, "dirt")
        Controller.obs["light-switch-left"] = p.at_left_is(self.observations, "lightSwitch")
        Controller.obs["water-left"] = p.at_left_is(self.observations, "water")
        Controller.obs["door-left"] = p.at_left_is(self.observations, "door")
        Controller.obs["dirt-right"] = p.at_right_is(self.observations, "dirt")
        Controller.obs["switch-right"] = p.at_right_is(self.observations, "lightSwitch")
        Controller.obs["water-right"] = p.at_right_is(self.observations, "water")
        Controller.obs["door-right"] = p.at_right_is(self.observations, "door")
        Controller.obs["dirt-front"] = p.in_front_of(self.observations, "dirt")
        Controller.obs["switch-front"] = p.in_front_of(self.observations, "lightSwitch")
        Controller.obs["water-front"] = p.in_front_of(self.observations, "water")
        Controller.obs["door-front"] = p.in_front_of(self.observations, "door")

        

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

