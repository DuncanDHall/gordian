from abc import ABCMeta, abstractmethod

from blackboard import BlackBoard
from sc2.bot_ai import BotAI


class Manager:
    ai: BotAI
    blackboard: BlackBoard
    __metaclass__ = ABCMeta

    def __init__(self, ai: BotAI, blackboard: BlackBoard):
        self.ai = ai
        self.blackboard = blackboard

    def on_before_start(self):
        pass

    def on_start(self):
        pass

    @abstractmethod
    def on_step(self, iteration: int):
        pass
