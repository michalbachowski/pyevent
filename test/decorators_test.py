#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# event modules
#
from pyevent import synchronous

##
# test helpers
#
from testutils import mock


@synchronous
def sync_notify(event):
    return True


class DecoratorsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_synchronous_notify_requires_at_least_2_arguments(self):
        err = False
        try:
            sync_notify()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_synchronous_notify_requires_at_least_2_arguments_1(self):
        err = False
        try:
            sync_notify('foo')
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_synchronous_notify_requires_at_least_2_arguments_3(self):
        err = False
        try:
            sync_notify('foo', 'bar')
        except AttributeError:
            err = True
        self.assertTrue(err)

    def test_synchronous_allows_to_pass_more_then_2_arguments(self):
        cb = mock.MagicMock(return_value='asd')
        cb.__name__ = 'callback'
        d = mock.MagicMock()
        d.resolve = mock.MagicMock()
        synchronous(cb)('foo', d, 'baz', 1, 2, d='f')
        cb.assert_called_once_with('foo', 'baz', 1, 2, d='f')
        d.resolve.assert_called_once_with('asd')

    def test_synchronous_resolves_given_deferred(self):
        d = mock.MagicMock()
        d.resolve = mock.MagicMock()
        self.assertTrue(sync_notify('foo', d))
        d.resolve.assert_called_once_with(True)


if "__main__" == __name__:
    unittest.main()
