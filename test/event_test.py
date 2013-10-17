#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# event modules
#
from pyevent import Event


class EventTestCase(unittest.TestCase):

    def test_init_requires_argument(self):
        err = False
        try:
            Event()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_init_requires_argument_1(self):
        err = False
        try:
            Event(None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_init_allows_to_pass_2_arguments(self):
        err = False
        try:
            Event(None, {})
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_init_does_not_check_input_arguments(self):
        err = False
        try:
            Event(None, None)
        except:
            err = True
        self.assertFalse(err)

    def test_init_state(self):
        e = Event('a')
        self.assertEqual('a', e.subject)
        self.assertIsNone(e.name)
        self.assertEqual({}, e.parameters)
        self.assertFalse(e.is_processed())
        self.assertFalse(e.is_propagation_stopped())

        e = Event('a', {'a': 1})
        self.assertEqual({'a': 1}, e.parameters)

    def test_mark_processed_changes_state_of_object(self):
        e = Event(None)
        self.assertFalse(e.is_processed())
        e.mark_processed()
        self.assertTrue(e.is_processed())

    def test_is_propagation_stopped_returns_propagation_status(self):
        e = Event(None)
        self.assertFalse(e.is_propagation_stopped())
        e.stop_propagation()
        self.assertTrue(e.is_propagation_stopped())

    def test_stop_propagation_changes_propagation_status(self):
        e = Event(None)
        self.assertFalse(e.is_propagation_stopped())
        e.stop_propagation()
        self.assertTrue(e.is_propagation_stopped())
        e.stop_propagation()
        self.assertTrue(e.is_propagation_stopped())
        e.start_propagation()
        self.assertFalse(e.is_propagation_stopped())
        e.stop_propagation()
        self.assertTrue(e.is_propagation_stopped())

    def test_start_propagation_changes_propagation_status(self):
        e = Event(None)
        self.assertFalse(e.is_propagation_stopped())
        e.stop_propagation()
        self.assertTrue(e.is_propagation_stopped())
        e.start_propagation()
        self.assertFalse(e.is_propagation_stopped())
        e.start_propagation()
        self.assertFalse(e.is_propagation_stopped())
        e.stop_propagation()
        self.assertTrue(e.is_propagation_stopped())

    def test_parametrs_can_be_accessed_throught_parameters_variable(self):
        e = Event(None, {'a': 1})

        self.assertEqual(1, e.parameters['a'])
        self.assertTrue('a' in e.parameters)


if "__main__" == __name__:
    unittest.main()
