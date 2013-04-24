#!/usr/bin/env python
# -*- coding: utf-8 -*-
import heapq
import itertools
from functools import partial, wraps
from promise import Deferred


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
    e = Event(subject, {'a' :1})
    e.subject           # subject
    e.name              # None
    e.parameters        # {'a': 1}
    e.is_processed()    # False
    e.mark_procesed()
    e.is_propagation_stopped() # false
    """

    def __init__(self, subject, parameters={}):
        """
        Initializes class instance
        """
        self.subject = subject
        self.name = None
        self.parameters = parameters
        self._processed = False
        self._propagate = True

    # propagation
    def is_propagation_stopped(self):
        """
        Returns information whether event propagation has been stopped
        """
        return not self._propagate

    def stop_propagation(self):
        self._propagate = False
        return self

    def start_propagation(self):
        self._propagate = True
        return self

    # process status
    def is_processed(self):
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


class Dispatcher(object):
    """
    Dispatches given events according to previously set listeners
    """

    def __init__(self):
        """
        Initializes class instance
        """
        self._listeners = {}
        self._dirty = False
        self.priority = 400
        self.counter = itertools.count()

    def attach(self, name, listener, priority=None):
        """
        Attaches new listener to dispatcher
        """
        if priority is None:
            priority = self.priority
        if name not in self._listeners:
            self._listeners[name] = []
        heapq.heappush(self._listeners[name], self._prepare(listener, priority))
        self._dirty = True

    def _prepare(self, listener, priority=0):
        """
        Prepares internal listener structure
        """
        return (priority, next(self.counter), listener)

    def __contains__(self, name):
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
        # sort list in order to iterate over elements (heapq changes order)
        if self._dirty:
            self._dirty = False
            self._listeners[name].sort()
        if name not in self._listeners:
            return iter([])
        return (l[2] for l in self._listeners[name])

    def notify(self, name, event):
        """
        Notifies each listener about new event
        """
        event.start_propagation().name = name
        # asynchronous call
        return Deferred(partial(self._async_notify, self.get_listeners(name),
                event)).promise()

    def _async_notify(self, listeners, event, deferred):
        """
        Notifies listeners about new event until any of then returns True
        in asynchronous manner
        """
        try:
            if event.is_propagation_stopped():
                raise StopIteration()
            Deferred(partial(next(listeners), event))\
                    .done(partial(self._async_notify, listeners, event,
                        deferred=deferred))\
                    .fail(deferred.fail)
        except StopIteration:
            deferred.resolve(event)


class Manager(object):
    """
    Class that simplifies attaching listeners to dispatcher
    """

    def __init__(self, dispatcher):
        """
        Class initialization
        """
        self.dispatcher = dispatcher

    def register(self, listener):
        """
        Registers event listeners to given dispatcher
        """
        # try to set dispatcher
        try:
            listener.set_dispatcher(self.dispatcher)
        except AttributeError:
            pass

        for t in listener.mapping():
            try:
                priority = t[2]
            except IndexError:
                priority = None
            self.dispatcher.attach(t[0], t[1], priority)


class Listener(object):
    """
    Class that defines simple interface for classes to work with Dispatcher
    """

    def mapping(self):
        """
        Returns list of listeners to be attached to dispatcher.
        [(event name, listener, priority), (event name, listener, priority)]
        """
        raise NotImplementedError('Return list of tuples with ' +\
            '(event, callback priority) mappings')


class DispatcherAware(object):
    """
    Mixin for listeners that want to have dispatcher reference be given
    """

    def set_dispatcher(self, dispatcher):
        """
        Dispatcher setter
        """
        self.dispatcher = dispatcher
        return self


def synchronous(function):
    """
    Decorator that marks event listeners as synchronous
    It handles deferred object on behalf of decorated function
    """
    @wraps(function)
    def wrapper(event, deferred, *args, **kwargs):
        ret = function(event, *args, **kwargs)
        deferred.resolve(ret)
        return ret
    return wrapper
