#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
import mox

# hack for loading modules
import _path
_path.fix()

##
# event modules
#
from event import Event, Dispatcher, Listener


class EventTestCase(unittest.TestCase):

    def test_init_requires_2_arguments(self):
        err = False
        try:
            e = Event()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_init_requires_2_arguments_1(self):
        err = False
        try:
            e = Event(None)
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_init_requires_2_arguments_2(self):
        err = False
        try:
            e = Event(None, None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_init_allows_to_pass_3_arguments(self):
        err = False
        try:
            e = Event(None, None, {})
        except TypeError:
            err = True
        self.assertFalse(err)
        
    def test_init_does_not_check_input_arguments(self):
        err = False
        try:
            e = Event(None, None, None)
        except:
            err = True
        self.assertFalse(err)
        
    def test_init_state(self):
        e = Event('a', 'b')
        self.assertEqual('a', e.subject)
        self.assertEqual('b', e.name)
        self.assertEqual({}, e.parameters)
        self.assertIsNone(e.return_value)
        self.assertFalse(e.processed)

        e = Event('a', 'b', {'a': 1})
        self.assertEqual({'a': 1}, e.parameters)

    def test_mark_processed_changes_state_of_object(self):
        e = Event(None, None)
        self.assertFalse(e.processed)
        e.mark_processed()
        self.assertTrue(e.processed)

    def test_processed_is_read_only_property(self):
        e = Event(None, None)
        err = False
        try:
            e.processed = True
        except AttributeError:
            err = True
        self.assertTrue(err)

    def test_parametrs_can_be_accessed_throught_event_instance(self):
        e = Event(None, None, {'a': 1})

        self.assertEqual(1, e['a'])
        self.assertTrue('a' in e)
        # event is read-only
        err = False
        try:
            e['b'] = 2
        except RuntimeError:
            err = True
        self.assertTrue(err)
        err = False
        try:
            del e['a']
        except RuntimeError:
            err = True
        self.assertTrue(err)


class DispatcherTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.event = self.mox.CreateMock(Event)
    
    def tearDown(self):
        self.mox.UnsetStubs()

    def test_init_does_not_take_any_arguments(self):
        err = False
        try:
            Dispatcher()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_attach_requires_2_arguments(self):
        err = False
        e = Dispatcher()
        try:
            e.attach()
        except TypeError:
            err = True
        self.assertTrue(err)
    
    def test_attach_requires_2_arguments_1(self):
        err = False
        e = Dispatcher()
        try:
            e.attach(None)
        except TypeError:
            err = True
        self.assertTrue(err)
    
    def test_attach_accepts_3_arguments_1(self):
        err = False
        e = Dispatcher()
        try:
            e.attach(None, None, None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_attach_maintains_priority_based_order(self):
        e = Dispatcher()
        e.attach('test', 'b', 20)
        e.attach('test', 'a', 10)
        e.attach('test', 'c', 20)

        l = e.get_listeners('test')
        self.assertEqual('a', l.next())
        self.assertEqual('b', l.next())
        self.assertEqual('c', l.next())

    def test_get_listeners_always_returns_iterator(self):
        e = Dispatcher()
        e.attach('test', 'b')
        self.assertEqual(1, sum([1 for i in e.get_listeners('test')]))
        self.assertEqual(0, sum([1 for i in e.get_listeners('unknown')]))

    def test_has_listeners_returns_integer(self):
        e = Dispatcher()
        e.attach('test', 'b')
        self.assertTrue(e.has_listeners('test'))
        self.assertFalse(e.has_listeners('unknown'))

    def test_notif_notifies_all_listeners(self):
        # prepare listener
        listener = Listener()
        self.mox.StubOutWithMock(listener, 'mapping')
        listener.mapping().AndReturn([('foo', None, 2)])

        # prepare dispatcher
        self.dispatcher.attach('foo', None, 2)
        self.mox.ReplayAll()

        # test
        listener.register(self.dispatcher)

        # verify
        self.mox.VerifyAll()


class ListenerTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.dispatcher = self.mox.CreateMock(Dispatcher)
    
    def tearDown(self):
        self.mox.UnsetStubs()

    def test_register_uses_mapping(self):
        # prepare listener
        listener = Listener()
        self.mox.StubOutWithMock(listener, 'mapping')
        listener.mapping().AndReturn([('foo', None, 2)])

        # prepare dispatcher
        self.dispatcher.attach('foo', None, 2)
        self.mox.ReplayAll()

        # test
        listener.register(self.dispatcher)

        # verify
        self.mox.VerifyAll()


if "__main__" == __name__:
    unittest.main()
