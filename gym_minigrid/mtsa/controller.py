from gym_minigrid.perception import Perception as p
import logging
import os

from monitors.mtsastatemachine import SafetyStateMachine


from transitions import Machine

class Mtsa(Machine):
    """
    MTSA Controller synthetised from safety properties
    """

    states = []
    transitions = []

    def __init__(self, notify):
        self.observations = True
        self.action = None

        cwd = os.getcwd()
        states_path = cwd + "/states.txt"
        transitions_path = cwd + "/transitions.txt"

        # Loading the states
        with open(states_path, 'r') as inf:
            self.states = eval(inf.read())

        # Loading the transitions
        with open(transitions_path, 'r') as inf:
            self.transitions = eval(inf.read())

        # super().__init__("mtsa", self.states, self.transitions, 'S0M1', notify)
        Machine.__init__(self, states=self.states, transitions=self.transitions, initial='S0M1')


    def _map_conditions(self, obs, action_proposed):
        self.observations = obs
        self.action = action_proposed


    def light_on(self):
        return p.is_condition_true(self.observations)

    def light_off(self):
        return p.is_condition_true(self.observations)

    def door_open(self):
        return p.is_condition_true(self.observations)

    def door_close(self):
        return p.is_condition_true(self.observations)

    def room_0(self):
        return p.is_condition_true(self.observations)

    def room_1(self):
        return p.is_condition_true(self.observations)

    def dirt_left(self):
        return p.is_condition_true(self.observations)

    def switch_left(self):
        return p.is_condition_true(self.observations)

    def water_left(self):
        return p.is_condition_true(self.observations)

    def door_left(self):
        return p.is_condition_true(self.observations)

    def dirt_right(self):
        return p.is_condition_true(self.observations)

    def switch_right(self):
        return p.is_condition_true(self.observations)

    def water_right(self):
        return p.is_condition_true(self.observations)

    def door_right(self):
        return p.is_condition_true(self.observations)

    def dirt_forward(self):
        return p.is_condition_true(self.observations)

    def switch_forward(self):
        return p.is_condition_true(self.observations)

    def water_forward(self):
        return p.is_condition_true(self.observations)

    def door_forward(self):
        return p.is_condition_true(self.observations)

