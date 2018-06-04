from unittest import *
from perception import Perception
from gym_minigrid.envs.bigEnv import  bigEnv


class TestPerception(TestCase):

    def test_door_opened_in_front(self):
        obs = bigEnv()
        p = Perception.door_opened_in_front(obs)
        if p:
            print("door_opened_in_front")
            self.assertTrue(p)
        #print("No")
        pass

    def test_door_closed_in_front(self):
        obs = bigEnv()
        p = Perception.door_closed_in_front(obs)
        if p:
            self.assertTrue(p)
        pass

    def test_check_if_coordinates_in_env(self):
        obs = bigEnv()
        object = Perception.check_if_coordinates_in_env(obs,(1,0))
        self.assertIsNotNone(object)

    def test_deadend_in_front(self, env):
        p = Perception.deadend_in_front(env)
        if p:
            print("deadend_in_front")
            self.assertTrue(p)
        else:
            pass

    def test_light_on_current_room(self):
        obs = bigEnv()
        p = Perception.light_on_current_room(obs)
        self.assertTrue(p)

    def test_light_switch_turned_on(self):
        obs = bigEnv()
        p = Perception.light_switch_turned_on(obs)
        self.assertTrue(p)
