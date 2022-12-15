from abc import ABCMeta, abstractmethod

from blackboard import Blackboard
from sc2.bot_ai import BotAI


class Manager(metaclass=ABCMeta):
    ai: BotAI
    blackboard: Blackboard

    def __init__(self, ai: BotAI, blackboard: Blackboard):
        self.ai = ai
        self.blackboard = blackboard

    def on_before_start(self):
        pass

    def on_start(self):
        pass

    @abstractmethod
    def on_step(self, iteration: int):
        pass
