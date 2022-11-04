from managers.role_manager import RoleManager
from managers.worker_splitting import WorkerSplitter
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI

from managers.manager import Manager
from managers.economy import MiningBooster, WorkerAssigner
from blackboard import BlackBoard, UnitRoles
from scheduling import Scheduler


class Gordian(BotAI):
    scheduler: Scheduler

    def __init__(self):
        blackboard = BlackBoard()
        self.managers: list[Manager] = [
            RoleManager(self, blackboard),
            WorkerSplitter(self, blackboard),
            MiningBooster(self, blackboard)
        ]
        self.scheduler = Scheduler(self.managers, blackboard)

    async def on_before_start(self):
        for manager in self.managers:
            manager.on_before_start()

    async def on_start(self):
        for manager in self.managers:
            manager.on_start()

    async def on_step(self, iteration: int):
        self.scheduler.on_step(iteration)


if __name__ == '__main__':
    run_game(maps.get("Flat32"), [
        Bot(Race.Protoss, Gordian()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=True)

