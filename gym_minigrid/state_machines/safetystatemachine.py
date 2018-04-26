from transitions.extensions import LockedHierarchicalGraphMachine as Machine

from transitions import MachineError

from transitions.extensions.nesting import NestedState, HierarchicalMachine

from transitions.extensions.locking import LockedMachine

from transitions.extensions.diagrams import GraphMachine, NestedGraph, Graph

from transitions.extensions.factory import NestedGraphTransition, LockedNestedEvent

from gym_minigrid.extendedminigrid import *




class SafetyNestedGraph(NestedGraph):
    safety_style_attributes = {
        'node': {
            'default': {
                'shape': 'circle',
                'height': '1',
                'style': 'filled',
                'fillcolor': 'white',
                'color': 'black',
            },
            'inf_ctrl': {
                'shape': 'diamond',
                'fillcolor': 'white',
                'color': 'black'
            },
            'sys_fin_ctrl': {
                'shape': 'box',
                'fillcolor': 'white',
                'color': 'black'
            },
            'sys_urg_ctrl': {
                'shape': 'box',
                'fillcolor': 'yellow',
                'color': 'black'
            },
            'env_fin_ctrl': {
                'shape': 'circle',
                'fillcolor': 'white',
                'color': 'black'
            },
            'env_urg_ctrl': {
                'shape': 'circle',
                'fillcolor': 'yellow',
                'color': 'black'
            },
            'violated': {
                'shape': 'doublecircle',
                'fillcolor': 'red',
                'color': 'black'
            },
            'satisfied': {
                'shape': 'doublecircle',
                'fillcolor': 'green',
                'color': 'black'
            },
            'active': {
                'color': 'red'
            },
            'previous': {
                'color': 'blue',
                'fillcolor': 'azure2'
            }
        },
        'edge': {
            'default': {
                'color': 'black'
            },
            'previous': {
                'color': 'blue'
            }
        },
        'graph': {
            'default': {
                'color': 'black',
                'fillcolor': 'white'
            },
            'previous': {
                'color': 'blue',
                'fillcolor': 'azure2',
                'style': 'filled'
            },
            'active': {
                'color': 'red',
                'fillcolor': 'darksalmon',
                'style': 'filled'
            },
        }
    }

    def __init__(self, *args, **kwargs):
        self.style_attributes = SafetyNestedGraph.safety_style_attributes
        super(SafetyNestedGraph, self).__init__(*args, **kwargs)


    def _add_nodes(self, states, container):
        states = [self.machine.get_state(state) for state in states] if isinstance(states, dict) else states
        for state in states:
            if state.name in self.seen_nodes:
                continue
            self.seen_nodes.append(state.name)
            if state.children:
                cluster_name = "cluster_" + state.name
                sub = container.add_subgraph(name=cluster_name, label=state.name, rank='source',
                                             **self.style_attributes['graph']['default'])
                anchor_name = state.name + "_anchor"
                root_container = sub.add_subgraph(name=state.name + '_root')
                child_container = sub.add_subgraph(name=cluster_name + '_child', label='', color=None)
                root_container.add_node(anchor_name, shape='point', fillcolor='black', width='0.1')
                self._add_nodes(state.children, child_container)
            else:
                container.add_node(state.name,
                                   shape=self.style_attributes['node'][state.type]['shape'],
                                   fillcolor=self.style_attributes['node'][state.type]['fillcolor'],
                                   color=self.style_attributes['node'][state.type]['color'])



class SafetyGraphMachine(GraphMachine):

    def _get_graph(self, model, title=None, force_new=False, show_roi=False):
        if title is None:
            title = self.title
        if not hasattr(model, 'graph') or force_new:
            model.graph = SafetyNestedGraph(self).get_graph(title) if isinstance(self, HierarchicalMachine) \
                else Graph(self).get_graph(title)
            self.set_node_state(model.graph, model.state, state='active')

        return model.graph if not show_roi else self._graph_roi(model)




class SafetyState(NestedState):
    """ Allows states to have different types.
                Attributes:
                type: can be a string among the state_types. `State.is_<type>` may be used
                        to check if the state is of type <type>.

                    satisfied:    Satisfied, in the current state, the property is satisfied and, from the current state
                                  it does not exist a path that may invalidate the property in the future.
                    inf_ctrl:     Infinitely controllable, in the current state the property is satisfied and it may reach
                                  a failure state in the future but is not close.
                    sys_fin_ctrl: System finitely controllable, the current state is finitely controllable by the
                                  system, and consequently the system can only stay in this state for a finite number of
                                  steps and then a failure may happen.
                    sys_urg_ctrl: System urgently controllable, the current state is urgently controllable by the
                                  system, and the next step of the system may lead to a failure.
                    env_fin_ctrl: Environment finitely controllable, the current state is finitely controllable by
                                  the environment, consequently the environment can only stay in the state for a finite
                                  number of steps and then a failure may happen. However, the environment can have
                                  the ability to make the system avoid this failure.
                    env_url_ctrl: Environment urgently controllable, the current state is urgently
                                  controllable by the environment, and the next step of the environment
                                  may lead to a failure.
                    violated:     Violated: the property is definitely violated.
            """

    state_types = ["satisfied",
                   "inf_ctrl",
                   "sys_fin_ctrl",
                   "sys_urg_ctrl",
                   "env_fin_ctrl",
                   "env_urg_ctrl",
                   "violated"]

    def __init__(self, *args, **kwargs):
        """
        Args:
            **kwargs: If kwargs contains `type`, assign it to the attribute.
        """
        if 'type' in kwargs:
            arg_type = kwargs.pop('type')
            if arg_type in SafetyState.state_types:
                self.type = arg_type
            else:
                raise MachineError("Error state '{0}' cannot be of type '{1}' !".format(self.name, arg_type))
        else:
            # Default if not specified
            self.type = "satisfied"
        super(SafetyState, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        if item.startswith('is_'):
            return item[3:] == self.type
        return super(SafetyState, self).__getattribute__(item)



class SafetyNestedGraphTransition(NestedGraphTransition):
    pass

class SafetyLockedHierarchicalGraphMachine(SafetyGraphMachine, LockedMachine, HierarchicalMachine):
    """
        A threadsafe hiearchical machine with graph support.
    """
    state_cls = SafetyState
    transition_cls = SafetyNestedGraphTransition
    event_cls = LockedNestedEvent



class MyTest(Machine):
    state_cls = SafetyState



class SafetyStateMachine(object):

    def __init__(self, name, pattern, states, transitions, initial, notify):
        self.name = name
        self.pattern = pattern

        # Initialize the state machine
        self.machine = SafetyLockedHierarchicalGraphMachine(
                                     model=self,
                                     states=states,
                                     transitions=transitions,
                                     initial=initial,
                                     show_conditions=True,
                                     auto_transitions=True)

        # Initial state observed by the agent
        self.initial_state = None
        self.env_state = None

        # Observations retreived before applying the action
        self.observations = None
        # Observations retreived after applying the action
        self.observations_post = None

        # Action proposed by the agent
        self.action_proposed = None

        # Function to be called when violation is detected (on_block) or when observations are needed (uncertainty)
        self.notify = notify
        # self.on_uncertainty_notify = on_uncertainty_notify

        # MiniGrid Actions and unsafe_actions list to be returned by the on_block
        self.actions = MiniGridEnv.Actions

    def _obs_to_state(self, obs):
        raise NotImplementedError


    def _on_monitoring(self):
        # Notify
        self.notify(self.name, "monitoring")

    def _on_shaping(self):
        # Notify
        self.notify(self.name, "shaping", shaped_reward=100)

    # Triggered when it enters in a state of time 'violated'
    def _on_violated(self):

        # Rollback to the state before the violation:
        self.machine.set_state(self.env_state)
        print("Rolled-back state to: " + self.state)

        # Notify
        self.notify(self.name, "violation", shaped_reward=100, unsafe_action=self.action_proposed)

    def _on_mismatch(self):
        self.notify(self.name, "mismatch")

    def draw(self):
        self.machine.get_graph(title=self.name).draw('patterns/' + self.pattern + "_" + self.name + '.png', prog='dot')

    # Called before the action is going to be performed on the environment and obs are the current observations
    def check(self, obs_pre, action_proposed):
        self.observations = obs_pre
        self.action_proposed = action_proposed
        self.env_state = self.state

        # Map the observation to a state
        self.env_state = self._obs_to_state(obs_pre)

        if self.initial_state is None:
            # First time
            # print("first time!")
            self.initial_state = self.env_state
            self.machine.set_state(self.env_state)
            self.trigger('*')
        elif self.state == self.env_state:
            self.trigger('*')
        else:
            self._on_mismatch()
        # print("monitor_state: " + self.state)

    # Update the state after the action has been performed in the environment
    def verify(self, obs_post, applied_action):

        # Map the observation to a state
        self.env_state = self._obs_to_state(obs_post)

        if self.state != self.env_state:
            # Switched to a new state
            self.observations = obs_post
            self.trigger('*')
            # print("new_monitor_state: " + self.state)
            if self.state != self.env_state:
                self._on_mismatch()

    """ Actions available to the agent - used for conditions checking """
    def forward(self):
        return self.action_proposed == 'forward'

    def toggle(self):
        return self.action_proposed == 'toggle'
