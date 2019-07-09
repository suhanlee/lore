from abc import ABCMeta, abstractmethod

import hashlib
import inspect

import sqlalchemy


class Base(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass

    @abstractmethod
    def __contains__(self, key):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def values(self):
        pass

    @abstractmethod
    def batch_set(self):
        pass

    @abstractmethod
    def batch_get(self, data_dict):
        pass

    def key(self, *args, **kwargs):
        stack = inspect.stack()
        caller = kwargs.pop('caller', stack[-2])
        instance = kwargs.pop('instance', self)
        if  len(args) > 0 and isinstance(args[0], sqlalchemy.sql.Selectable):
            query_string = (
                str(args[0]).encode('utf-8') +
                str(args[0].compile().params).encode('utf-8')
            )
        else:
            query_string = str(args).encode('utf-8')

        return '.'.join((
            instance.__module__,
            instance.__class__.__name__,
            caller.__code__.co_name,
            hashlib.sha1(query_string + str(kwargs).encode('utf-8')).hexdigest()
        ))
