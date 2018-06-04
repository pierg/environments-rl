from perception import Perception as p
import logging

from monitors.safetystatemachine import SafetyStateMachine


class Avoid(SafetyStateMachine):
    """
    It will always avoid a certain world-object
    """

    states = [
        {'name': 'initial',
         'type': 'inf_ctrl',
         'on_enter': '_on_monitoring'},

        {'name': 'safe',
         'type': 'inf_ctrl',
         'on_enter': '_on_safe'},

        {'name': 'near',
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_near'},

        {'name': 'immediate',
         'type': 'sys_urg_ctrl',
         'on_enter': '_on_immediate'},

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
         'conditions': 'obs_immediate'},

        {'trigger': '*',
         'source': 'immediate',
         'dest': 'immediate',
         'conditions': 'obs_immediate',
         'unless': ['violated_action']},

        {'trigger': '*',
         'source': 'immediate',
         'dest': 'near',
         'conditions': 'obs_near',
         'unless': 'obs_immediate'},

        {'trigger': '*',
         'source': 'immediate',
         'dest': 'fail',
         'conditions': ['violated_action', 'obs_immediate']
         },
    ]

    obs = {
        "near": False,
        "immediate": False
    }

    def __init__(self, name, worldobj_avoid, action, notify, rewards):
        self.near_rwd = rewards.near
        self.immediate_rwd = rewards.immediate
        self.violated_rwd = rewards.violated
        self.worldobj_avoid = worldobj_avoid
        self.action = action
        self.test = False
        super().__init__(name, "avoid", self.states, self.transitions, 'initial', notify)

    # Convert obseravions to state and populate the obs_conditions
    def _obs_to_state(self, obs, action_proposed):
        # Get observations conditions
        near = p.is_near_to_worldobj(obs, self.worldobj_avoid)
        immediate = p.is_immediate_to_worldobj(obs, self.worldobj_avoid)

        # Save them in the obs_conditions dictionary
        Avoid.obs["near"] = near
        Avoid.obs["immediate"] = immediate

        if str(action_proposed) == self.action :
            self.test = True
        else:
            self.test = False

        # Return the state
        if immediate:
            return 'immediate'
        elif near:
            return 'near'
        else:
            return 'safe'

    def _on_safe(self):
        super()._on_monitoring()

    def _on_near(self):
        super()._on_shaping(self.near_rwd)

    def _on_immediate(self):
        super()._on_shaping(self.immediate_rwd)

    def _on_violated(self):
        logging.warning("avoid %s violated", self.name)
        self.machine.set_state(self.env_state)
        logging.warning("Rolled-back state to: %s", self.state)
        super()._on_violated(self.violated_rwd)

    def obs_near(self):
        return Avoid.obs["near"]

    def obs_immediate(self):
        return Avoid.obs["immediate"]

    def violated_action(self):
        return self.test
