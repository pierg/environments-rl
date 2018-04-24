from fake_obshelper import ObsHelper as oh

from state_machines.safetystatemachine import SafetyStateMachine



class Absence(SafetyStateMachine):
    """
    It makes sure that the agent will never enter in the state of type 'violated'
    This pattern is the dual of the Existence pattern
    It takes as input the type of cell that the agent must avoid at all states
    """

    states = [
        {'name': 'initial',
         'type': 'inf_ctrl'},

        {'name': 'safe',
         'type': 'inf_ctrl'},

        {'name': 'near',
         'type': 'sys_fin_ctrl'},

        {'name': 'immediate',
         'type': 'sys_urg_ctrl'},

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
         'dest': 'safe',
         'unless': ['obs_near', 'obs_immediate']},

        {'trigger': '*',
         'source': 'safe',
         'dest': 'near',
         'conditions': 'obs_near',
         'unless': 'obs_immediate'},

        {'trigger': '*',
         'source': 'near',
         'dest': 'near',
         'conditions': 'obs_near',
         'unless': 'obs_immediate'},

        {'trigger': '*',
         'source': 'near',
         'dest': 'safe',
         'unless': ['obs_near', 'obs_immediate']},

        {'trigger': '*',
         'source': 'near',
         'dest': 'immediate',
         'conditions': 'obs_immediate',
         'unless': 'obs_near'},


        {'trigger': '*',
         'source': 'immediate',
         'dest': 'immediate',
         'conditions': 'obs_immediate',
         'unless': ['forward', 'obs_near']},

        {'trigger': '*',
         'source': 'immediate',
         'dest': 'near',
         'conditions': 'obs_near',
         'unless': 'obs_immediate'},

        {'trigger': '*',
         'source': 'immediate',
         'dest': 'fail',
         'conditions': ['forward', 'obs_immediate'],
         'unless': 'obs_near'},
    ]

    def __init__(self, name, worldobj_avoid, notify):
        self.worldobj_avoid = worldobj_avoid
        super().__init__(name, "absence", self.states, self.transitions, 'initial', notify)

    def _obs_to_state(self, obs):
        near = oh.is_near_to_worldobj(obs, self.worldobj_avoid)
        immediate = oh.is_immediate_to_worldobj(obs, self.worldobj_avoid)
        if immediate:
            return 'immediate'
        elif near and not immediate:
            return 'near'
        else:
            return'safe'

    def obs_near(self):
        n = oh.is_near_to_worldobj(self.observations_pre, self.worldobj_avoid)
        return oh.is_near_to_worldobj(self.observations_pre, self.worldobj_avoid)

    def obs_immediate(self):
        i = oh.is_immediate_to_worldobj(self.observations_pre, self.worldobj_avoid)
        return oh.is_immediate_to_worldobj(self.observations_pre, self.worldobj_avoid)






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

