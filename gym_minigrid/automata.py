from transitions import Machine, State

from obshelper import ObsHelper


class TakeBath(object):
    """ The agent should never step into the water """

    states = [
        'normal',
        'facing_water',
        State(name='block', on_enter=['set_safe_action'])
    ]



    transitions = [
        {'trigger': 'forward',
         'source': 'normal',
         'dest': 'facing_water',
         'unless': 'is_water_approaching'},

        {'trigger': 'forward',
         'source': 'facing_water',
         'dest': 'block'},

        {'trigger': 'forward',
         'source': '*',
         'dest': 'normal',
         'unless': 'is_water_approaching'},
    ]

    def __init__(self, name):

        self.name = name
        self.obs = None
        self.safe_action = None

        # Initialize the state machine
        self.machine = Machine(model=self, states=TakeBath.states, initial='normal')


    def update_obs(self, obs):
        self.obs = obs

    def get_safe_action(self):
        return self.safe_action

    def set_safe_action(self):
        # SET A SAFE ACTION
        self.safe_action = 2

    def is_water_approaching(self):
        return ObsHelper.is_water_approaching(self.obs)



class EnterRoom(object):
    """ The agent should not enter a room without first turning the lights on """

    states = [
        'room_inside',
        'room_entrance',
        State(name='block', on_enter=['set_safe_action'])
    ]

    transitions = [
        {'trigger': 'forward',
         'source': 'room_inside',
         'dest': 'room_entrance',
         'conditions': 'is_door_in_front'},

        {'trigger': 'forward',
         'source': 'room_entrance',
         'dest': 'room_inside',
         'conditions': 'is_light_on'},

        {'trigger': 'forward',
         'source': 'room_entrance',
         'dest': 'block',
         'unless': 'is_light_on'},
    ]

    def __init__(self, name):

        self.name = name
        self.obs = None
        self.safe_action = None

        # Initialize the state machine
        self.machine = Machine(model=self, states=EnterRoom.states, initial='room_inside')

    def update_obs(self, obs):
        self.obs = obs

    def get_safe_action(self):
        return self.safe_action

    def set_safe_action(self):
        # SET A SAFE ACTION
        self.safe_action = 2

    def is_door_in_front(self):
        return ObsHelper.is_door_in_front(self.obs)