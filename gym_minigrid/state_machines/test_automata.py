from state_machines.patterns.absence import *


def on_monitoring(name, type, **kwargs):
    """
    Notify for violations
    :param type: Can be of state/observations mismatch or violation of safety property
    :param unsafe_actions: list of unsafe actions (in case of violation type)
    :return:
    """

    if type == "mismatch":
        print("Mismatch between state machine and observations!!!")

    if type=="violation":
        if kwargs:
            print("Violation Blocked!!!!")
            shaped_reward = kwargs.get('shaped_reward', 0)
            unsafe_action = kwargs.get('unsafe_action')
            print("shaped_reward=" + str(shaped_reward) + " unsafe_action=" + str(unsafe_action))
        else:
            print("ERROR. missing action and reward")



def test_absence():
    avoid_water = Absence('avoid_water', 'water', on_monitoring)
    avoid_water.draw()
    avoid_water.check("safe", 'puppa')
    avoid_water.verify("safe", 'puppa')
    avoid_water.check("safe", 'forward')
    # observations change to "near"
    avoid_water.verify("near", 'forward')
    avoid_water.check("near", 'puppa')
    avoid_water.verify("near", 'puppa')
    avoid_water.check("near", 'forward')
    avoid_water.verify("immediate", 'wait')
    avoid_water.check("immediate", 'puppa')
    avoid_water.verify("immediate", 'wait')
    avoid_water.check("immediate", 'forward')
    avoid_water.verify("fail!!", 'wait')

    # avoid_water.check("immediate", 'puppa')
    # avoid_water.check("immediate", 'forward')


def test_statetypes():
    test_state_types = StateTypes('TestStateTypes', notify)
    test_state_types.draw()


class TestAutomata:
    if __name__ == "__main__":
        test_absence()
