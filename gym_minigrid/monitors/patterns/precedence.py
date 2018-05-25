from gym_minigrid.perception import Perception as p
import logging

from monitors.safetystatemachine import SafetyStateMachine


class Precedence(SafetyStateMachine):
    """
    To describe relationships between a pair of events/states where the occurrence of the first
    is a necessary pre-condition for an occurrence of the second. We say that an occurrence of
    the second is enabled by an occurrence of the first.
    """

    states = [
        {'name': 'initial',
         'type': 'inf_ctrl',
         'on_enter': '_on_monitoring'},

        {'name': 'idle',
         'type': 'inf_ctrl',
         'on_enter': '_on_idle'},

        {'name': 'respected',
         'type': 'satisfied',
         'on_enter': '_on_respected'},

        {'name': 'violated',
         'type': 'violated',
         'on_enter': '_on_violated'}
    ]

    transitions = [
        {'trigger': '*',
         'source': 'initial',
         'dest': '*'},

        {'trigger': '*',
         'source': 'idle',
         'dest': 'idle',
         'unless': 'activated'},

        {'trigger': '*',
         'source': 'idle',
         'dest': 'respected',
         'conditions': ['activated', 'respected']},

        {'trigger': '*',
         'source': 'idle',
         'dest': 'violated',
         'conditions': ['activated', 'violated']},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'violated',
         'conditions': ['activated', 'violated']},

        {'trigger': '*',
         'source': 'violated',
         'dest': 'respected',
         'conditions': ['activated', 'respected']},

        {'trigger': '*',
         'source': 'violated',
         'dest': 'idle',
         'unless': 'activated'},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'idle',
         'unless': 'activated'},
    ]

    obs = {
        "respected": False
    }

    def __init__(self, name, conditions, notify, rewards):
        self.respectd_rwd = rewards.respected
        self.violated_rwd = rewards.violated
        self.precondition = conditions.pre
        self.postcondition = conditions.post
        self.active = False
        super().__init__(name, "precedence", self.states, self.transitions, 'initial', notify)

    # Convert observations to state and populate the obs_conditions
    def _obs_to_state(self, obs, action_proposed):
        # Get observations conditions
        self.active = p.is_condition_satisfied(obs, action_proposed, self.postcondition)

        if self.active:
            if p.is_condition_satisfied(obs, action_proposed, self.precondition):
                Precedence.obs["respected"] = True
                return 'respected'
            else:
                Precedence.obs["respected"] = False
                return 'violated'
        else:
            return 'idle'

    def _on_idle(self):
        super()._on_monitoring()

    def _on_active(self):
        super()._on_monitoring()

    def _on_respected(self):
        super()._on_shaping(self.respectd_rwd)

    def _on_violated(self):
        super()._on_violated(self.violated_rwd)

    def activated(self):
        return self.active

    def respected(self):
        return self.active and Precedence.obs["respected"] == True

    def violated(self):
        return self.active and Precedence.obs["respected"] == False

