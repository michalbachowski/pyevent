#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# event modules
#
from pyevent import Listener


class ListenerTestCase(unittest.TestCase):

    def test_mapping_must_be_implemented(self):
        err = False
        try:
            Listener().mapping()
        except NotImplementedError:
            err = True
        self.assertTrue(err)


if "__main__" == __name__:
    unittest.main()
