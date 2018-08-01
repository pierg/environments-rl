from gym_minigrid.perception import Perception as p
import logging

from monitors.safetystatemachine import SafetyStateMachine


class Response(SafetyStateMachine):
    """
    To describe relationships between a pair of events/states where the occurrence of the first
    is a necessary pre-condition for an occurrence of the second. We say that an occurrence of
    the second is enabled by an occurrence of the first.
    """

    states = [

        {'name': 'idle',
         'type': 'inf_ctrl',
         'on_enter': '_on_idle'},

        {'name': 'active',
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_active'},

        {'name': 'precond_active',
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_active'},

        {'name': 'postcond_respected',
         'type': 'satisfied',
         'on_enter': '_on_respected'},

        {'name': 'postcond_violated',
         'type': 'violated',
         'on_enter': '_on_violated'}
    ]

    transitions = [

        {'trigger': '*',
         'source': 'idle',
         'dest': 'idle',
         'unless': 'active_cond'},

        {'trigger': '*',
         'source': 'idle',
         'dest': 'active',
         'conditions': 'active_cond'},

        {'trigger': '*',
         'source': 'active',
         'dest': 'idle',
         'unless': 'active_cond'},

        {'trigger': '*',
         'source': 'active',
         'dest': 'active',
         'conditions': 'active_cond',
         'unless': 'precondition_cond'},

        {'trigger': '*',
         'source': 'active',
         'dest': 'precond_active',
         'conditions': 'precondition_cond'},

        {'trigger': '*',
         'source': 'precond_active',
         'dest': 'postcond_respected',
         'conditions': 'postcondition_cond'},

        {'trigger': '*',
         'source': 'precond_active',
         'dest': 'postcond_violated',
         'unless': 'postcondition_cond'},

        {'trigger': '*',
         'source': 'postcond_respected',
         'dest': 'active',
         'conditions': 'active_cond'},

        {'trigger': '*',
         'source': 'postcond_respected',
         'dest': 'idle',
         'unless': 'active_cond'},

        {'trigger': '*',
         'source': 'postcond_violated',
         'dest': 'active',
         'conditions': 'active_cond'},

        {'trigger': '*',
         'source': 'postcond_violated',
         'dest': 'idle',
         'unless': 'active_cond'},

    ]

    obs = {
        "active": False,
        "precondition": False,
        "postcondition": False,
    }

    # Sate machine conditions
    def active_cond(self):
        return Response.obs["active"]

    def precondition_cond(self):
        return Response.obs["precondition"]

    def postcondition_cond(self):
        return Response.obs["postcondition"]

    def __init__(self, name, conditions, notify, rewards):
        self.respectd_rwd = rewards.respected
        self.violated_rwd = rewards.violated
        self.postcondition = conditions.post
        self.precondition = conditions.pre

        super().__init__(name, "response", self.states, self.transitions, 'idle', notify)

    def _context_active(self, obs, action_proposed):
        return True

    def _map_context(self, obs, action_proposed):
        # Activating condition
        context_active = self._context_active(obs, action_proposed)
        Response.obs["active"] = context_active
        return context_active

    # Convert observations to state and populate the obs_conditions
    def _map_conditions(self, obs, action_proposed):
        self.action_proposed = action_proposed
        precondition = p.is_condition_satisfied(obs, self.precondition, action_proposed)
        Response.obs["precondition"] = precondition

        # If precondition is true, check postcondition and trigger as one atomic operation
        if precondition:
            Response.obs["postcondition"] = p.is_condition_satisfied(obs, self.postcondition, action_proposed)
            self.trigger("*")

    def _on_idle(self):
        self.active = False
        logging.info("entered state: " + self.state)
        super()._on_monitoring()

    def _on_monitoring(self):
        logging.info("entered state: " + self.state)
        super()._on_monitoring()

    def _on_active(self):
        logging.info("entered state: " + self.state)
        super()._on_monitoring()

    def _on_respected(self):
        logging.info("entered state: " + self.state)
        super()._on_shaping(self.respectd_rwd)

    def _on_violated(self):
        #print(self.name, self.action_proposed, Response.obs["precondition"],Response.obs["postcondition"])
        logging.info("entered state: " + self.state)
        super()._on_violated(self.violated_rwd)
