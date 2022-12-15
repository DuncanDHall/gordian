import functools
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Callable, Any, final, Optional

from blackboard import Blackboard
from operations.operation_base import Operation
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

CacheKey = Callable[[Any], Any]  # use the method as the key, cause first class functions are hashable lol


@dataclass
class CacheValue:
    expire_time: float
    value: Any


def cache_interpretation(duration: float = 0.1):
    """returns a decorator which will cache the result with an expiration time of t + duration"""
    def caching_decorator(func: Callable[[Any], Any]):
        """returns a decorated function which uses unexpired cached value if available"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = kwargs['time']
            if func in Interpreter.cache and Interpreter.cache[func].expire_time <= 10:  # Interpreter.ai.time:
                return Interpreter.cache[func].value
            else:
                result = func(*args, **kwargs)
                Interpreter.cache[func] = CacheValue(duration, result)  # add ai.time to duration
                return result
        return wrapper
    return caching_decorator


class Interpreter(metaclass=ABCMeta):
    cached_result: Any
    cache_expires: float
    ai: BotAI

    @property
    @abstractmethod
    def cache_longevity(self) -> float:
        pass

    # @cache_longevity.setter
    # @abstractmethod
    # def cache_longevity(self, val: float):
    #     self.cache_longevity = val

    def __init__(self, ai: BotAI):
        self.ai = ai

    @abstractmethod
    def call_body(self):
        pass

    @final
    def __call__(self, *args, **kwargs):
        if self.cached_result and self.cache_expires < self.ai.time:
            return self.cached_result
        else:
            result = self.call_body(*args, **kwargs)
            self.cached_result = result
            self.cache_expires = self.ai.time + self.cache_longevity
            return result


class EconomyStrengthInt(Interpreter):
    cache_longevity = 5.0

    def call_body(self):
        # count opposing workers and mules
        # sub-interp
        pass


class EconomyStrengthVespeneInt(Interpreter):
    cache_longevity = 5.0

    def call_body(self):
        # count vespene harvesting buildings
        pass


class SomeOperation(Operation):
    desired_units = []
    eco_interpreter: EconomyStrengthInt

    def __init__(self, parent_op: Optional['Operation'], ai: BotAI, blackboard: Blackboard):
        super().__init__(parent_op, ai, blackboard)
        self.eco_interpreter = EconomyStrengthInt(self.ai)

    def on_step_body(self, iteration):
        if self.eco_interpreter() > 0.5:
            # we are in a better position economically
            pass
        else:
            # we are in a worse position economically
            pass
