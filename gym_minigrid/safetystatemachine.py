from transitions.extensions import GraphMachine as Machine
from minigrid import MiniGridEnv



class SafetyStateMachine(object):

    def __init__(self, name, states, transitions, on_block_notify):
        self.name = name

        # Initialize the state machine
        self.machine = Machine(model=self,
                          states=states,
                          transitions=transitions,
                          initial='safe',
                          show_conditions='True')

        # Agent's observations
        self.obs = None
        # Function to be called when violation is detected (on_block)
        self.on_block_notify = on_block_notify

        # MiniGrid Actions and unsafe_actions list to be returned by the on_block
        self.actions = MiniGridEnv.Actions
        self.unsafe_actions = []


    def draw(self):
        self.machine.get_graph(title=self.name).draw('automaton_' + self.name + '.png', prog='dot')

    def check(self, obs, action):
        self.obs = obs
        self.trigger('*', action=action)

    # Return list of unsafe_actions, called everytime a violation is detected
    def _on_block(self):
       self.on_block_notify(self.unsafe_actions)



    """ Actions available to the agnet - used for conditions checking """
    def forward(self, action):
        return action == 'forward'

    def toggle(self, action):
        return action == 'toggle'
