from perception import Perception as p
import logging

from monitors.safetystatemachine import SafetyStateMachine

class Avert(SafetyStateMachine):
    """
        It makes sure that the agent will avert an action which penalize it
        This pattern is the dual of the Existence pattern
        It takes as input the type of cell that the agent must avert at all states
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
         'dest': 'violated',
         'conditions': ['toggle', 'obs_warning']},

        {'trigger': '*',
         'source': 'disobey',
         'dest': 'safe'}

    ]

    obs = {
        "warning": False
    }

    def __init__(self, name, worldobj_avert, notify, rewards):
        self.disobeyReward = rewards
        self.worldobj_avert = worldobj_avert
        super().__init__(name, "avert", self.states, self.transitions, 'initial', notify)

    # Convert obsevravions to state and populate the obs_conditions
    def _obs_to_state(self, obs, action_proposed):
        # Get observations conditions
        warning = p.is_immediate_to_worldobj(obs, self.worldobj_avert)

        # Save them in the obs_conditions dictionary
        Avert.obs["warning"] = warning
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
        logging.warning("%s broken!!!!", self.worldobj_avert)
        super()._on_shaping(self.disobeyReward)

    def obs_warning(self):
        return Avert.obs["warning"]

