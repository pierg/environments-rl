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

    # Sate machine conditions
    def active_cond(self):
        return self.context_active

    def precondition_cond(self):
        return self.obs_precondition

    def postcondition_cond(self):
        return self.obs_postcondition

    def __init__(self, name, conditions, notify, rewards, perception, context):
        self.respectd_rwd = rewards.respected
        self.violated_rwd = rewards.violated
        self.postcondition = conditions.post
        self.precondition = conditions.pre

        self.context_active = False
        self.obs_precondition = False
        self.obs_postcondition = False

        super().__init__(name, "response", self.states, self.transitions, 'idle', notify, perception, context)

    def context_active(self, obs, action_proposed):
        return True

    # Convert observations to state and populate the obs_conditions
    def _map_conditions(self, action_proposed):
        self.action_proposed = action_proposed
        precondition = self.perception.is_condition_satisfied(self.precondition, action_proposed)
        self.obs_precondition = precondition

        # If precondition is true, check postcondition and trigger as one atomic operation
        if precondition:
            self.obs_postcondition = self.perception.is_condition_satisfied(self.postcondition, action_proposed)
            self.trigger("*")

    def _on_idle(self):
        self.context_active = False
        super()._on_monitoring()

    def _on_monitoring(self):
        super()._on_monitoring()

    def _on_active(self):
        super()._on_monitoring()

    def _on_respected(self):
        if self.config.debug_mode: print(self.name + "\trespected\t" + self.postcondition)
        super()._on_shaping(self.respectd_rwd)

    def _on_violated(self):
        if self.config.debug_mode: print(self.name + "\tviolation\t" + self.postcondition)
        super()._on_violated(self.violated_rwd)
