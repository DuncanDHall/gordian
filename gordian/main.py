from interpreter import Interpreter
from operations.global_ops.pvx_op import PvXGlobalOp
from operations.operation_base import Operation
from operations.root_operation_base import RootOperation
from sc2 import maps
from sc2.ids.unit_typeid import UnitTypeId
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI

from blackboard import Blackboard, UnitOrUpgradeId
from sc2.unit import Unit


class Gordian(BotAI):
    interpreter: Interpreter
    root_op: RootOperation

    def __init__(self, wishlist: list[UnitOrUpgradeId]):
        blackboard = Blackboard(wishlist)
        self.interpreter = Interpreter(self)
        self.root_op = PvXGlobalOp(self.interpreter, blackboard)

    async def on_before_start(self):
        self.root_op.on_before_start()

    async def on_start(self):
        self.root_op.on_start()

    async def on_step(self, iteration: int):
        self.root_op.on_step(iteration)

    async def on_unit_destroyed(self, unit_tag: int):
        # TODO notify operations (recursively)
        pass

    async def on_unit_created(self, unit: Unit):
        # TODO assign to root operation
        pass


if __name__ == '__main__':
    bot = Bot(Race.Protoss, Gordian([
        UnitTypeId.PYLON,
        UnitTypeId.PYLON,
        UnitTypeId.PYLON,
        UnitTypeId.PYLON,
        UnitTypeId.PYLON,
        # UnitTypeId.STALKER,
    ]))
    run_game(maps.get("Flat128"), [
        bot,
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=True)

