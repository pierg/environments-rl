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



    # State machine conditions

    def light_on(self):
        condition = p.is_condition_satisfied(self.observations, "light-on-next-room")
        if condition:
            self.logger("light_on")
        return condition

    def light_off(self):
        condition = not p.is_condition_satisfied(self.observations, "light-on-next-room")
        if condition:
            self.logger("light_off")
        return condition

    def door_open(self):
        condition = p.is_condition_satisfied(self.observations, "door-opened-in-front")
        if condition:
            self.logger("door_open")
        return condition

    def door_close(self):
        condition = not p.is_condition_satisfied(self.observations, "door-opened-in-front")
        if condition:
            self.logger("door_close")
        return condition

    def room_0(self):
        condition = p.is_condition_satisfied(self.observations, "room-0", self.tigger_action)
        if condition:
            self.logger("room_0")
        return condition

    def room_1(self):
        condition = p.is_condition_satisfied(self.observations, "room-1", self.tigger_action)
        if condition:
            self.logger("room_1")
        return condition

    def dirt_left(self):
        condition = p.at_left_is(self.observations, "dirt")
        if condition:
            self.logger("dirt_left")
        return condition

    def switch_left(self):
        condition = p.at_left_is(self.observations, "lightSwitch")
        if condition:
            self.logger("switch_left")
        return condition

    def water_left(self):
        condition = p.at_left_is(self.observations, "water")
        if condition:
            self.logger("water_left")
        return condition

    def door_left(self):
        condition = p.at_left_is(self.observations, "door")
        if condition:
            self.logger("door_left")
        return condition

    def dirt_right(self):
        condition = p.at_right_is(self.observations, "dirt")
        if condition:
            self.logger("dirt_right")
        return condition

    def switch_right(self):
        condition = p.at_right_is(self.observations, "lightSwitch")
        if condition:
            self.logger("switch_right")
        return condition

    def water_right(self):
        condition = p.at_right_is(self.observations, "water")
        if condition:
            self.logger("water_right")
        return condition

    def door_right(self):
        condition = p.at_right_is(self.observations, "door")
        if condition:
            self.logger("door_right")
        return condition

    def dirt_forward(self):
        condition = p.in_front_of(self.observations, "dirt")
        if condition:
            self.logger("dirt_forward")
        return condition

    def switch_forward(self):
        condition = p.in_front_of(self.observations, "lightSwitch")
        if condition:
            self.logger("switch_forward")
        return condition

    def water_forward(self):
        condition = p.in_front_of(self.observations, "water")
        if condition:
            self.logger("water_forward")
        return condition

    def door_forward(self):
        condition = p.in_front_of(self.observations, "door")
        if condition:
            self.logger("door_forward")
        return condition

