import logging

from monitors.safetystatemachine import SafetyStateMachine


class Precedence(SafetyStateMachine):
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

        {'name': 'postcond_active',
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_active'},

        {'name': 'precond_respected',
         'type': 'satisfied',
         'on_enter': '_on_respected'},

        {'name': 'precond_violated',
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
         'unless': 'postcondition_cond'},

        {'trigger': '*',
         'source': 'active',
         'dest': 'postcond_active',
         'conditions': 'postcondition_cond'},

        {'trigger': '*',
         'source': 'postcond_active',
         'dest': 'precond_respected',
         'conditions': 'precondition_cond'},

        {'trigger': '*',
         'source': 'postcond_active',
         'dest': 'precond_violated',
         'unless': 'precondition_cond'},

        {'trigger': '*',
         'source': 'precond_respected',
         'dest': 'active',
         'conditions': 'active_cond'},

        {'trigger': '*',
         'source': 'precond_respected',
         'dest': 'idle',
         'unless': 'active_cond'},

        {'trigger': '*',
         'source': 'precond_violated',
         'dest': 'active',
         'conditions': 'active_cond'},

        {'trigger': '*',
         'source': 'precond_violated',
         'dest': 'idle',
         'unless': 'active_cond'},
        
    ]

    # Sate machine conditions
    def active_cond(self):
        return self.active

    def postcondition_cond(self):
        return self.obs_postcondition

    def precondition_cond(self):
        return self.obs_precondition

    def reset(self):
        super().reset()
        self.obs_precondition = False

    def __init__(self, name, conditions, notify, rewards, perception):
        self.respectd_rwd = rewards.respected
        self.violated_rwd = rewards.violated
        self.precondition = conditions.pre
        self.postcondition = conditions.post

        self.active = False
        self.obs_precondition = False
        self.obs_postcondition = False

        super().__init__(name, "precedence", self.states, self.transitions, 'idle', notify, perception)


    def context_active(self, obs, action_proposed):
        return True

    def _map_context(self, obs, action_proposed):
        # Activating condition
        context_active = self.context_active(obs, action_proposed)
        self.active = context_active
        return context_active

    # Convert observations to state and populate the obs_conditions
    def _map_conditions(self, action_proposed):

        postcondition = self.perception.is_condition_satisfied(self.postcondition, action_proposed)
        self.obs_postcondition = postcondition

        if not self.obs_precondition:
            self.obs_precondition = self.perception.is_condition_satisfied(self.precondition, action_proposed)

        # If postcondition is true, check precondition and trigger as one atomic operation
        if postcondition:
            self.trigger("*")


    def _on_idle(self):
        self.active = False
        super()._on_monitoring()

    def _on_monitoring(self):
        super()._on_monitoring()

    def _on_active(self):
        super()._on_monitoring()

    def _on_respected(self):
        if self.config.debug_mode: print(self.name + "\trespected\t" + self.precondition)
        super()._on_shaping(self.respectd_rwd)

    def _on_violated(self):
        if self.config.debug_mode: print(self.name + "\tviolation\t" + self.precondition)
        super()._on_violated(self.violated_rwd)
