from gym_minigrid.perception import Perception as p
import logging

from gym_minigrid.monitors.safetystatemachine import SafetyStateMachine



class Universality(SafetyStateMachine):
    """
    Always true
    """

    states = [
        {'name': 'initial',
         'type': 'inf_ctrl',
         'on_enter': '_on_monitoring'},

        {'name': 'respected',
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_respected'},

        {'name': 'violated',
         'type': 'sys_urg_ctrl',
         'on_enter': '_on_violated'},

    ]

    transitions = [
        {'trigger': '*',
         'source': 'initial',
         'dest': '*'},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'respected',
         'unless': 'obs_violated'},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'violated',
         'conditions': 'obs_violated'},

        {'trigger': '*',
         'source': 'violated',
         'dest': 'violated',
         'conditions': 'obs_violated'},

        {'trigger': '*',
         'source': 'violated',
         'dest': 'respected',
         'unless': 'obs_violated'},
    ]

    obs = {
        "respected": False
    }

    def __init__(self, name, condition, notify, rewards):
        self.respectd_rwd = rewards.respected
        self.violated_rwd = rewards.violated
        self.condition = condition
        super().__init__(name, "universally", self.states, self.transitions, 'initial', notify)

    # Convert obseravions to state and populate the obs_conditions
    def _obs_to_state(self, obs, action_proposed):
        if p.is_condition_satisfied(obs, action_proposed, self.condition):
            Universality.obs["respected"] = True
            return 'respected'
        else:
            Universality.obs["respected"] = False
            return 'violated'

    def _on_monitoring(self):
        super()._on_monitoring()

    def _on_respected(self):
        super()._on_shaping(self.respectd_rwd)

    def _on_violated(self):
        super()._on_shaping(self.violated_rwd)

    def obs_violated(self):
        return not Universality.obs["respected"]


