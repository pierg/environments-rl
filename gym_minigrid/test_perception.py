from unittest import *
from perception import *


class TestPerception(TestCase):

    def setup(self):
        self.light = 0
        self.door = 0

    def test_door_opened_in_front(self):
        #TestPerception.setup(self)
        p = Perception.door_opened_in_front(self.env)
        self.assertTrue(p)

    def test_door_closed_in_front(self):
        TestPerception.setup(self)
        p = Perception.door_closed_in_front(self.env)
        self.assertTrue(p)
    """
    def test_check_if_coordinates_in_env(self, obj_in_front):
        obj_for_test = Perception.check_if_coordinates_in_env(self.env, (1, 0))
        if obj_for_test is not None:
            print(obj_in_front, "   ", obj_for_test.type)
            self.assertTrue(obj_in_front == obj_for_test.type)
        else:
            print(obj_in_front, "   ", obj_for_test)
            self.assertTrue(obj_in_front == obj_for_test)
    """

    def test_deadend_in_front(self):
        p = Perception.deadend_in_front(self.env)
        self.assertTrue(p)

    def test_light_on_current_room(self):
        p = Perception.light_on_current_room(self.env)
        self.assertTrue(p)

    def test_light_switch_turned_on(self):
        p = Perception.light_switch_turned_on(self.env)
        self.assertTrue(p)

