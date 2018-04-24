from state_machines.patterns.absence import *


def notify(type, unsafe_actions=None):
    """
    Notify for violations
    :param type: Can be of state/observations mismatch or violation of safety property
    :param unsafe_actions: list of unsafe actions (in case of violation type)
    :return:
    """
    if type == "violation":
        print ("Violation Blocked!!!!" + " Unsafe actions: ", unsafe_actions)

    if type == "mismatch":
        print("Mismatch between state machine and observations!!!")



# def main():
#     # Fake observations, only for testing purposes
#     obs = 'fake_agent_observations'
#     # Fake action proposed by the agent
#     action = 'forward'
#
#     avoid_water = AvoidWater('avoid_water', notify)
#     avoid_water.draw()
#     print(avoid_water.state)
#     avoid_water.check(obs, action)
#     print(avoid_water.state)
#     avoid_water.check(obs, action)
#
#
#     avoid_dark = AvoidDark('avoid_dark', notify)
#     avoid_dark.draw()
#     print(avoid_dark.state)
#     action = '[forward, left, right]'
#     avoid_dark.check(obs, action)
#     print(avoid_dark.state)
#     avoid_dark.check(obs, action)
#     print(avoid_dark.state)
#
# def test_water():
#     # Fake observations, only for testing purposes
#     obs = 'fake_agent_observations'
#     # Fake action proposed by the agent
#     action = 'forward'
#
#     avoid_water = AvoidWater('avoid_water', notify)
#     avoid_water.draw()
#     # print(avoid_water.state)
#     avoid_water.check("safe", 'puppa')
#     # print(avoid_water.state)
#     avoid_water.check("safe", 'forward')
#     avoid_water.check("safe", 'forward')
#     avoid_water.check("safe", 'forward')
#     avoid_water.check("near_water", 'forward')
#     #
#     avoid_water.check("facing_water", 'forward')
#     # print(avoid_water.state)
#
def test_absence():

    avoid_water = Absence('avoid_water', 'water', notify)
    avoid_water.draw()
    avoid_water.check("safe", 'puppa')
    avoid_water.check("near", 'puppa')
    avoid_water.check("immediate", 'puppa')
    avoid_water.check("immediate", 'forward')
    # avoid_water.check("near", 'puppa')
    # avoid_water.check("immediate", 'forward')
    # avoid_water.check("safe", 'ciao')
    # avoid_water.check("safe", 'forward')
    # avoid_water.check("safe", 'forward')
    # avoid_water.check("immediate", 'left')
#
#

# def test():
#     test_state_types = StateTypes('TestStateTypes', notify)
#     test_state_types.draw()
#
#

class TestAutomata:
    if __name__ == "__main__":
        test_absence()
