#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

# hack for loading modules
from _path import fix, mock
fix()

##
# test helper
#
from mock_helper import IsA

##
# event modules
#
from pyevent import Manager


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.dispatcher = mock.MagicMock()
        self.dispatcher.attach = mock.MagicMock()
        self.listener = mock.MagicMock()
        self.listener.mapping = mock.MagicMock(return_value=[('a', 'b')])
        self.listener.set_dispatcher = mock.MagicMock()

    def test_init_expects_1_argument(self):
        err = False
        try:
            Manager()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_init_expects_1_argument_1(self):
        err = False
        try:
            Manager(None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_register_expects_1_argument(self):
        err = False
        try:
            Manager(None).register()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_register_expects_1_argument_1(self):
        err = False
        try:
            Manager(None).register(None)
        except AttributeError:
            err = True
        self.assertTrue(err)

    def test_register_expects_listener(self):
        Manager(self.dispatcher).register(self.listener)
        self.listener.mapping.assert_called_once_with()

    def test_register_calls_dispatcher_attach_method(self):
        Manager(self.dispatcher).register(self.listener)
        self.listener.mapping.assert_called_once_with()
        self.dispatcher.attach.assert_called_once_with('a', 'b', IsA(int))

    def test_register_tries_to_set_dispatcher_to_listener(self):
        Manager(self.dispatcher).register(self.listener)
        self.listener.mapping.assert_called_once_with()
        self.listener.set_dispatcher.assert_called_once_with(IsA(mock.MagicMock))


if "__main__" == __name__:
    unittest.main()
