import collections
import functools
from dataclasses import dataclass
from typing import Any, Callable, Optional

from sc2.bot_ai import BotAI
from sc2.unit import Unit


@dataclass
class CachedResult:
    expire_time: float
    value: Any


def cache_result(duration: float = 0.1):
    """returns a decorator which will cache the result with an expiration time of t + duration"""
    def caching_decorator(func: Callable[[Any], Any]):
        """returns a decorated function which uses unexpired cached value if available"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if func in Interpreter.method_cache and Interpreter.method_cache[func, args].expire_time >= Interpreter._ai.time:
                return Interpreter.method_cache[func, args].value
            else:
                result = func(*args, **kwargs)
                Interpreter.method_cache[func, args] = CachedResult(Interpreter._ai.time + duration, result)
                return result
        return wrapper
    return caching_decorator


class Interpreter:
    # key: tuple of method and args
    # value: result
    method_cache: dict[tuple[Callable[[Any], Any], [Any]], CachedResult] = {}
    _ai: BotAI

    def __init__(self, ai: BotAI):
        self._ai = ai
        self.__class__._ai = ai

    # MARK: all reading of the ai state goes through here

    @property
    @cache_result(1.0)  # cache the result for 1 second
    def my_upgrades(self):
        return self._ai.state.upgrades

    @property
    @cache_result(1.0)
    def townhalls(self):
        return self._ai.townhalls

    @property
    @cache_result(1.0)
    def mineral_fields(self):
        return self._ai.mineral_field

    @property
    @cache_result(3600.0)
    def expansion_locations(self):
        return self._ai.expansion_locations_list

    @property
    def units(self):
        return self._ai.units + self._ai.structures

    @cache_result(0.0)  # cache the result for this single game step
    def unit(self, tag) -> Optional[Unit]:
        return self._ai.units.find_by_tag(tag) or self._ai.structures.find_by_tag(tag)

    @property
    def client(self):
        return self._ai.client

    @property
    @cache_result(1.0)
    def placeholder(self):
        return self._ai.placeholder

    @property
    @cache_result(1.0)
    def placeholder(self):
        return self._ai.placeholder

    @property
    @cache_result(1.0)
    def placeholder(self):
        return self._ai.placeholder

