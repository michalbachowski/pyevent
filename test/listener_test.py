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
from mock_helper import *

##
# event modules
#
from pyevent import Dispatcher, Listener


class ListenerTestCase(unittest.TestCase):

    def setUp(self):
        self.dispatcher = Dispatcher()

    def test_register_expects_mapping_to_be_implemented(self):
        # prepare listener
        listener = Listener()

        # test
        err = False
        try:
            listener.register(None)
        except RuntimeError:
            err = True
        self.assertTrue(err)

    def test_register_calls_dispatcher_attach_method(self):
        # prepare listener
        listener = Listener()

        listener.mapping = lambda: [('a', 1)]
        self.dispatcher.attach = mock.MagicMock()

        # test
        listener.register(self.dispatcher)

        # validate
        self.dispatcher.attach.assert_called_once_with('a', 1, IsA(int))


if "__main__" == __name__:
    unittest.main()
