#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest


##
# event modules
#
from pyevent import DispatcherAware


class DispatcherAwareTestCase(unittest.TestCase):

    def test_set_dispatcher_expects_1_argument(self):
        err = False
        try:
            DispatcherAware().set_dispatcher()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_set_dispatcher_expects_1_argument_1(self):
        err = False
        DispatcherAware().set_dispatcher(None)
        try:
            DispatcherAware().set_dispatcher(None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_set_dispatcher_returns_instance_of_self(self):
        da = DispatcherAware()
        self.assertEqual(da.set_dispatcher(None), da)

    def test_set_dispatcher_creates_dispatcher_attribute(self):
        da = DispatcherAware()
        self.assertFalse(hasattr(da, 'dispatcher'))
        da.set_dispatcher(None)
        self.assertTrue(hasattr(da, 'dispatcher'))
        self.assertIsNone(da.dispatcher)


if "__main__" == __name__:
    unittest.main()
