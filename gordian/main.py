from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI

from managers.manager import Manager
from managers.economy import SpeedMining
from blackboard import BlackBoard, UnitRoles
from scheduling import Scheduler


class Gordian(BotAI):
    scheduler: Scheduler

    def __init__(self):
        blackboard = BlackBoard()
        managers: list[Manager] = [
            SpeedMining(self, blackboard)
        ]
        self.scheduler = Scheduler(managers, blackboard)

    async def on_step(self, iteration: int):
        self.scheduler.on_step(iteration)


if __name__ == '__main__':
    run_game(maps.get("Simple64"), [
        Bot(Race.Protoss, Gordian()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=True)

