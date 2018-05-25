from perception import Perception as p
import logging

from monitors.safetystatemachine import SafetyStateMachine

class Avoid(SafetyStateMachine):
    """
        It makes sure that the agent will avoid an action which penalize it
        This pattern is the dual of the Existence pattern
        It takes as input the type of cell that the agent must avoid at all states
        """
    states = [
        {'name':'initial',
         'type':'inf_ctrl',
         'on_enter':'_on_monitoring'},

        {'name': 'safe',
         'type': 'inf_ctrl',
         'on_enter': '_on_safe'},

        {'name': 'warning',
         'type': 'sys_urg_ctrl',
         'on_enter': '_on_warning'},

        {'name': 'disobey',
         'type': 'violated',
         'on_enter': '_on_disobey'},
    ]

    transitions = [
        {'trigger':'*',
         'source':'initial',
         'dest':'*'},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'safe',
         'unless':['obs_warning']},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'warning',
         'conditions':'obs_warning'},

        {'trigger': '*',
         'source': 'warning',
         'dest': 'warning',
         'conditions': 'obs_warning',
         'unless': ['toggle']},

        {'trigger': '*',
         'source': 'warning',
         'dest': 'safe',
         'unless': 'obs_warning'},

        {'trigger': '*',
         'source': 'warning',
         'dest': 'disobey',
         'conditions': ['toggle', 'obs_warning']},

        {'trigger': '*',
         'source': 'disobey',
         'dest': 'safe'}

    ]

    obs = {
        "warning": False
    }

    def __init__(self, name, worldobj_avoid, notify,reward):
        self.disobeyReward = reward
        self.worldobj_avoid = worldobj_avoid
        super().__init__(name, "avoid", self.states, self.transitions, 'initial', notify)

    # Convert obsevravions to state and populate the obs_conditions
    def _obs_to_state(self, obs):
        # Get observations conditions
        warning = p.is_immediate_to_worldobj(obs, self.worldobj_avoid.name)

        # Save them in the obs_conditions dictionary
        Avoid.obs["warning"] = warning
        # Return the state
        if warning:
            return 'warning'
        else:
            return 'safe'


    def _on_safe(self):
        super()._on_monitoring()

    def _on_warning(self):
        super()._on_monitoring()

    def _on_disobey(self):
        super()._on_shaping(self.disobeyReward)

    def obs_warning(self):
        return Avoid.obs["warning"]


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

        {'name': 'sys_urg_ctrl',
         'type': 'sys_urg_ctrl'},

        {'name': 'env_fin_ctrl',
         'type': 'env_fin_ctrl'},

        {'name': 'env_urg_ctrl',
         'type': 'env_urg_ctrl'},

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