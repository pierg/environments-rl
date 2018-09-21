import logging

from monitors.safetystatemachine import SafetyStateMachine


class Absence(SafetyStateMachine):
    """
    ALways false
    """

    states = [

        {'name': 'idle',
         'type': 'inf_ctrl',
         'on_enter': '_on_idle'},

        {'name': 'active',
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_active'},

        {'name': 'respected',
         'type': 'sys_fin_ctrl',
         'on_enter': '_on_respected'},

        {'name': 'violated',
         'type': 'satisfied',
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
         'dest': 'respected',
         'conditions': 'condition_cond'},

        {'trigger': '*',
         'source': 'active',
         'dest': 'violated',
         'unless': 'condition_cond'},

        {'trigger': '*',
         'source': 'respected',
         'dest': 'idle'},

        {'trigger': '*',
         'source': 'violated',
         'dest': 'idle'},

    ]


    # Sate machine conditions
    def active_cond(self):
        return self.context_active

    def condition_cond(self):
        return self.obs_condition


    def __init__(self, name, conditions, notify, rewards, perception, context):
        self.respectd_rwd = rewards.respected
        self.violated_rwd = rewards.violated
        self.condition = conditions

        self.obs_condition = False

        super().__init__(name, "absence", self.states, self.transitions, 'idle', notify, perception, context)

    def context_active(self, obs, action_proposed):
        return self.context_active

    # Convert observations to state and populate the obs_conditions
    def _map_conditions(self, action_proposed):
        condition = not self.perception.is_condition_satisfied(self.condition, action_proposed)
        self.obs_condition = condition

    def _on_idle(self):
        self.context_active = False
        super()._on_monitoring()

    def _on_monitoring(self):
        super()._on_monitoring()

    def _on_active(self):
        super()._on_monitoring()

    def _on_respected(self):
        if self.config.debug_mode: print(self.name + "\trespected\t" + self.condition)
        super()._on_shaping(self.respectd_rwd)

    def _on_violated(self):
        if self.config.debug_mode: print(self.name + "\tviolated\t" + self.condition)
        super()._on_violated(self.violated_rwd)
