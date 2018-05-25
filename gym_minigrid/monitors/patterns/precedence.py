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

        {'name': 'safe',
         'type': 'inf_ctrl',
         'on_enter': '_on_safe'},

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
         'source': 'safe',
         'dest': 'safe',
         'unless': 'obs_precedence_active'},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'respected',
         'conditions': ['obs_precedence_active','obs_precedence_respected']},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'violated',
         'conditions': ['obs_precedence_active', 'obs_precedence_violated']},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'violated',
         'conditions': ['obs_precedence_active', 'obs_precedence_violated']},

        {'trigger': '*',
         'source': 'violated',
         'dest': 'respected',
         'conditions': ['obs_precedence_active', 'obs_precedence_respected']},

        {'trigger': '*',
         'source': 'violated',
         'dest': 'safe',
         'unless': 'obs_precedence_active'},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'safe',
         'unless': 'obs_precedence_active'},
    ]

    obs = {
        "precedenceRespected": False
    }

    def __init__(self, name, object_prec, notify, reward):
        self.precedenceRespectedReward = reward.precedenceRespected
        self.precedenceViolatedReward = reward.precedenceViolated
        self.precondition = object_prec.preCondition
        self.postcondition = object_prec.postCondition
        self.active = False
        super().__init__(object_prec.name, "precedence", self.states, self.transitions, 'initial', notify)

    # Convert observations to state and populate the obs_conditions
    def _obs_to_state(self, obs):
        # Get observations conditions
        self.active = p.precedence_condition(obs,self.postcondition)
        if self.active :
            if p.precedence_condition(obs,self.precondition):
                Precedence.obs["precedenceRespected"]=True
                return 'respected'
            else:
                Precedence.obs["precedenceRespected"] = False
                return 'violated'
        else:
            return 'safe'

    def _on_safe(self):
        super()._on_monitoring()

    def _on_active(self):
        super()._on_monitoring()

    def _on_respected(self):
        super()._on_shaping(self.precedenceRespectedReward)

    def _on_violated(self):
        super()._on_violated(self.precedenceViolatedReward)

    def obs_precedence_active(self):
        return self.active

    def obs_precedence_respected(self):
        return self.active and Precedence.obs["precedenceRespected"]==True

    def obs_precedence_violated(self):
        return self.active and Precedence.obs["precedenceRespected"]==False

class StateTypes(SafetyStateMachine):
    """ Testing """

    states = [

        {'name': 'initial',
         'type': 'inf_ctrl'},

        {'name': 'satisfied',
         'type': 'satisfied'},

        {'name': 'inf_ctrl',
         'type': 'inf_ctrl'},

        {'name': 'sys_fin_ctrl',
         'type': 'sys_fin_ctrl'},

        {'name': 'env_fin_ctrl',
         'type': 'env_fin_ctrl'},

        {'name': 'violated',
         'type': 'violated'}
    ]

    transitions = []

    # Convert the observations stored in self.current_obs in a state a saves the state in current_state
    def _obs_to_state(self, obs):
        self.curret_state = ''

    def __init__(self, name, notify):
        # Initializing the SafetyStateMachine
        super().__init__(name, self.states, self.transitions, 'initial', notify)

