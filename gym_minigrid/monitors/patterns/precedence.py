from gym_minigrid.perception import Perception as p
import logging

from ..safetystatemachine import SafetyStateMachine


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
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_respected'},

        {'name': 'disobey',
         'type': 'sys_urg_ctrl',
         'on_enter': '_on_disobeyed'},

        {'name': 'fail',
         'type': 'violated',
         'on_enter': '_on_violated'}
    ]

    transitions = [
        {'trigger': '*',
         'source': 'initial',
         'dest': '*'},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'disobey',
         'conditions': 'obs_precedence_disobeyed',
         'unless': 'obs_precedence_respected'},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'respected',
         'conditions': 'obs_precedence_respected',
         'unless': 'obs_precedence_disobeyed'},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'safe',
         'unless': ['obs_precedence_disobeyed', 'obs_precedence_respected']},

        {'trigger': '*',
         'source': 'disobey',
         'dest': 'safe',
         'unless': ['obs_precedence_disobeyed', 'obs_precedence_respected']},

        {'trigger': '*',
         'source': 'disobey',
         'dest': 'respected',
         'conditions': 'obs_precedence_respected',
         'unless': 'obs_precedence_disobeyed'},

        {'trigger': '*',
         'source': 'disobey',
         'dest': 'fail',
         'conditions': ['forward','obs_precedence_disobeyed']}
    ]

    obs = {
        "precedenceRespected": False,
        "precedenceViolated": False
    }

    def __init__(self, name, object_prec, notify, reward):
        self.precedenceRespectedReward = reward.precedenceRespected
        self.precedenceViolatedReward = reward.precedenceViolated
        self.precondition = object_prec.preCondition
        self.postcondition = object_prec.postCondition
        super().__init__(object_prec.name, "precedence", self.states, self.transitions, 'initial', notify)

    # Convert observations to state and populate the obs_conditions
    def _obs_to_state(self, obs):

        # Get observations conditions
        precondition = p.precedence_condition(obs, self.precondition)
        postcondition = p.precedence_condition(obs, self.postcondition)
        if precondition and postcondition:
            Precedence.obs["precedenceRespected"] = True
            Precedence.obs["precedenceViolated"] = False
        elif not precondition and postcondition:
            Precedence.obs["precedenceRespected"] = False
            Precedence.obs["precedenceViolated"] = True
        else:
            Precedence.obs["precedenceRespected"] = False
            Precedence.obs["precedenceViolated"] = False
        logging.info("precedence %s : Conditions Respected ->%s Conditions Violated ->%s", self.name,
                     Precedence.obs["precedenceRespected"], Precedence.obs["precedenceViolated"])
        # Return the state
        if Precedence.obs["precedenceViolated"]:
            return 'disobey'
        elif Precedence.obs["precedenceRespected"]:
            return 'respected'
        else:
            return'safe'

    def _on_safe(self):
        super()._on_monitoring()

    def _on_respected(self):
        super()._on_shaping(self.precedenceRespectedReward)

    def _on_disobeyed(self):
        super()._on_shaping(self.precedenceViolatedReward)

    def _on_violated(self):
        logging.warning("precedence %s violated", self.name)
        super()._on_violated(self.precedenceViolatedReward)

    def obs_precedence_respected(self):
        return Precedence.obs["precedenceRespected"]

    def obs_precedence_disobeyed(self):
        return Precedence.obs["precedenceViolated"]



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

