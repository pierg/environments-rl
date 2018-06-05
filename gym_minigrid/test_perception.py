from unittest import *
from perception import Perception
from extendedminigrid import ExMiniGridEnv

class TestPerception(TestCase):

    def __init__(self):
        self.light = 0
        self.door = 0

    def test_door_opened_in_front(self, env, action):
        if str(ExMiniGridEnv.worldobj_in_agent(env, 1, 0)) == "door" and str(action) == "Actions.toggle":
            if self.door == 0:
                print("door open")
                p = Perception.door_opened_in_front(env)
                self.assertTrue(p)
                self.door =1
            else:
                TestPerception.test_door_closed_in_front(self,env, action)

    def test_door_closed_in_front(self, env, action):
        if str(ExMiniGridEnv.worldobj_in_agent(env, 1, 0)) == "door" and str(action) == "Actions.toggle":
            if self.door == 1:
                print("door closed")
                p = Perception.door_closed_in_front(env)
                self.assertTrue(p)
                self.door =0

    def test_check_if_coordinates_in_env(self,env):
        object = ExMiniGridEnv.worldobj_in_agent(env,1,0)
        objecttest = Perception.check_if_coordinates_in_env(env,(1,0))

        if objecttest is not None:
            print(object,"   ", objecttest.type)
            self.assertTrue( object == objecttest.type)
        else:
            print(object, "   ", objecttest)
            self.assertTrue(object == objecttest)


    def test_deadend_in_front(self, env):
        p = Perception.deadend_in_front(env)
        if p:
            print("deadend_in_front")
            self.assertTrue(p)

    def test_light_on_current_room(self,env):
        p = Perception.light_on_current_room(env)
        self.assertTrue(p)

    def test_light_switch_turned_on(self,env,action):
        if str(ExMiniGridEnv.worldobj_in_agent(env,1,0)) == "lightSwitch" and str(action) == "Actions.toggle":
            p = Perception.light_switch_turned_on(env)
            if self.light == 0:
                print(True)
                self.assertTrue(p)
                self.light = 1
            else:
                print("False")
                self.assertFalse(p)
                self.light = 0

