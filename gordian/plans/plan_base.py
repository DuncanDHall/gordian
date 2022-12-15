from abc import ABCMeta, abstractmethod

from blackboard import Blackboard
from sc2.bot_ai import BotAI


class Plan(metaclass=ABCMeta):
    ai: BotAI
    blackboard: Blackboard

    def __init__(self, ai: BotAI, blackboard: Blackboard):
        self.ai = ai
        self.blackboard = blackboard
        self.assigned_units = self.claim_units()

    def on_initiation(self):
        pass

    @abstractmethod
    def on_step(self, iteration: int):
        pass

    @abstractmethod
    def claim_units(self):
        pass
