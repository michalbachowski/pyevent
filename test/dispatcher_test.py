#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# test helpers
#
from testutils import mock, IsA

##
# pypromise modules
#
from promise import Deferred, Promise

##
# event modules
#
from pyevent import Event, Dispatcher


def call_deferred(event, deferred):
    deferred.resolve()

class DispatcherTestCase(unittest.TestCase):

    def setUp(self):
        self.event = Event('test')

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
        d = Dispatcher()
        d.attach('test', 'b', 20)
        d.attach('test', 'a', 10)
        d.attach('test', 'c', 20)

        l = d.get_listeners('test')
        self.assertEqual('a', next(l))
        self.assertEqual('b', next(l))
        self.assertEqual('c', next(l))

    def test_get_listeners_always_returns_iterator(self):
        d = Dispatcher()
        d.attach('test', 'b')
        self.assertEqual(1, sum([1 for i in d.get_listeners('test')]))
        self.assertEqual(0, sum([1 for i in d.get_listeners('unknown')]))

    def test_contains_checks_is_listener_exists(self):
        d = Dispatcher()
        d.attach('test', 'b')
        self.assertTrue('test' in d)
        self.assertFalse('unknown' in d)

    def test_notify_expects_2_arguments(self):
        err = False
        try:
            Dispatcher().notify()
        except TypeError:
            err = True
        self.assertTrue(err)
    def test_notify_expects_2_arguments_1(self):
        err = False
        try:
            Dispatcher().notify('a')
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_notify_expects_2_arguments_2(self):
        err = False
        try:
            Dispatcher().notify('a', self.event)
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_notify_starts_event_propagation(self):
        self.event.stop_propagation()
        Dispatcher().notify('a', self.event)
        self.assertFalse(self.event.is_propagation_stopped())

    def test_notify_sets_event_name(self):
        self.assertIsNone(self.event.name)
        Dispatcher().notify('a', self.event)
        self.assertEqual('a', self.event.name)

    def test_notify_returns_promise_instance(self):
        self.assertTrue(isinstance(Dispatcher().notify('a', self.event),
                Promise))

    def test_notify_notifies_listeners_until_propagation_is_not_stopped(self):
        # prepare dispatcher
        d = Dispatcher()

        foo = mock.MagicMock(side_effect=call_deferred)
        bar = mock.MagicMock(side_effect=call_deferred)

        d.attach('foo', foo)
        d.attach('foo', bar)

        # test
        d.notify('foo', self.event)

        # verify
        foo.assert_called_once_with(IsA(Event), deferred=IsA(Deferred))
        bar.assert_called_once_with(IsA(Event), deferred=IsA(Deferred))

    def test_notify_terminates_notification_when_event_propagation_is_stopped(
            self):
        # prepare dispatcher
        d = Dispatcher()

        def stop_propagation(event, deferred):
            event.stop_propagation()
            call_deferred(event, deferred)
        foo = mock.MagicMock(side_effect=stop_propagation)
        bar = mock.MagicMock(side_effect=call_deferred)

        d.attach('foo', foo)
        d.attach('foo', bar)

        # test
        d.notify('foo', self.event)

        # verify
        foo.assert_called_once_with(IsA(Event), deferred=IsA(Deferred))
        bar.assert_never_called()

    def test_notify_resolves_promise_when_finished(self):
        # prepare dispatcher
        d = Dispatcher()

        foo = mock.MagicMock(side_effect=call_deferred)
        cb = mock.MagicMock()

        d.attach('foo', foo)

        # test
        d.notify('foo', self.event).done(cb)

        # verify
        foo.assert_called_once_with(IsA(Event), deferred=IsA(Deferred))
        cb.assert_called_once_with(IsA(Event))


if "__main__" == __name__:
    unittest.main()
