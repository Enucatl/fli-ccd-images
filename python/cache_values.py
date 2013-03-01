#!/usr/bin/env python
from __future__ import division, print_function

"""cache return values
as in http://www.slideshare.net/mchruszcz/caching-techniques-in-python"""

_cache = {} #cache storage

def memoize_method(key):
    """works for methods by extracting the instance (=self)
    parameter"""
    def _decorating_wrapper(func):
        def _caching_wrapper(instance, *args, **kwargs):
            try:
                cache = instance._cache
            except AttributeError:
                cache = instance._cache = {}
            if key in cache:
                "value was cached: use it"
                return cache[key]
            else:
                "store the return value"
                ret = func(instance, *args, **kwargs)
                cache[key] = ret
                return ret
        return _caching_wrapper
    return _decorating_wrapper
