#!/usr/bin/env python
# -*- coding: utf-8 -*-
import heapq
import itertools


class Event(object):
    """
    Class that represents single event to be handled

    Provides information about:
    
    subject - subject which sends event
    name - name of an event
    parameters - event parameters
    return_value - event return value
    processed - whether event has been processed or not

    Example:

    subject = self
    e = Event(subject, 'test', {'a' :1})
    e.subject           # subject
    e.name              # 'test'
    e.parameters        # {'a': 1}
    e['a']              # 1
    e.parameters['a']   # 1
    e.return_value      # None
    e.return_value = 'a'
    e.return_value      # 'a'
    e.processed         # False
    e.mark_procesed()
    e.processed         # True
    """

    def __init__(self, subject, name, parameters={}):
        """
        Initializes class instance
        """
        self.subject = subject
        self.name = name
        self.parameters = parameters
        self.return_value = None
        self._processed = False

    @property
    def processed(self):
        """
        Returns information whether event has been processed
        """
        return self._processed

    def mark_processed(self):
        """
        Marks event as processed
        """
        self._processed = True
        return self

    def __getitem__(self, key):
        """
        Allows to treat class instances as dicts
        """
        return self.parameters[key]

    def __setitem__(self, key, value):
        """
        Allows to treat class instances as dicts
        """
        self.parameters[key] = value

    def __delitem__(self, key):
        """
        Allows to treat class instances as dicts
        """
        del self.parameters[key]

    def __iter__(self):
        """
        Allows to treat class instances as dicts
        """
        return self.parameters

    def __reversed__(self):
        """
        Allows to treat class instances as dicts
        """
        return self.parameters.__reversed__()

    def __contains__(self, item):
        """
        Allows to treat class instances as dicts
        """
        return item in self.parameters


class Dispatcher(object):
    """
    Dispatches given events according to previously set listeners
    """

    def __init__(self):
        """
        Initializes class instance
        """
        self._listeners = {}
        self.counter = itertools.count()

    def attach(self, name, listener, priority=0):
        """
        Attaches new listener to dispatcher
        """
        if name not in self._listeners:
            self._listeners[name] = []
        heapq.heappush(self._listeners[name], self._prepare(listener, priority))

    def _prepare(self, listener, priority=0):
        """
        Prepares internal listener structure
        """
        return (priority, next(self.counter), listener)

    def has_listeners(self, name):
        """
        Returns information whether there are any listeners 
        attached to given event name
        """
        return name in self._listeners and len(self._listeners[name])>0

    def get_listeners(self, name):
        """
        Fetches list of listeners attached to given event.
        Returns iterator
        """
        if name not in self._listeners:
            return []
        return (l[2] for l in self._listeners[name])

    def notify(self, event):
        """
        Notifies each listener about new event
        """
        for listener in self.get_listeners(event.name):
            listener(event)
        return event;

    def notify_until(self, event):
        """
        Notifies listeners about new event until any of then returns True
        """
        for listener in self.get_listeners(event.name):
            if listener(event):
                event.mark_processed()
                break
        return event

    def filter(self, event, value):
        """
        Filters given value using given event
        """
        for listener in self.get_listeners(event.name):
            value = listener(event, value)
        event.return_value = value
        return event


class Listener(object):
    """
    Class that simplifies attaching listeners
    """

    def register(self, dispatcher):
        """
        Registers event listeners to given dispatcher
        """
        for (event, callback, priority) in self.mapping.iteritems():
            dispatcher.connect(event, callback, priority)

    @property
    def mapping(self):
        """
        Returns list of listeners to be attached to dispatcher.
        [(event name, listener, priority), (event name, listener, priority)]
        """
        raise NotImplementedError('Return list of event=>callback mappings')


def test():
    def foo(e):
        print ('foo', e.name)

    def bar(e):
        print ('bar', e.name)

    d = Dispatcher()
    d.attach('test', bar, 2)
    d.attach('test', foo, 1)

    e = Event(None, 'test', {'a': 1})
    d.notify(e)


if '__main__' == __name__:
    test()
