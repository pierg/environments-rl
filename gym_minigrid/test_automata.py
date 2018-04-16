from automata import *


def notify_violations(unsafe_actions):
    print ("Violation Blocked!!!!" + " Unsafe actions: ", unsafe_actions)

def main():
    # Fake observations, only for testing purposes
    obs = 'fake_agent_observations'
    # Fake action proposed by the agent
    action = 'forward'

    avoid_water = AvoidWater('avoid_water', notify_violations)
    avoid_water.draw()
    print(avoid_water.state)
    avoid_water.check(obs, action)
    print(avoid_water.state)
    avoid_water.check(obs, action)


    avoid_dark = AvoidDark('avoid_dark', notify_violations)
    avoid_dark.draw()
    print(avoid_dark.state)
    action = '[forward, left, right]'
    avoid_dark.check(obs, action)
    print(avoid_dark.state)
    avoid_dark.check(obs, action)
    print(avoid_dark.state)


def test():
    test_state_types = TestStateTypes('TestStateTypes', notify_violations)
    test_state_types.draw()



class TestAutomata:
    if __name__ == "__main__":
        test()
        main()