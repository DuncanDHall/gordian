import datetime
import os
import pathlib
import pickle

from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race, Difficulty
from sc2.ids.ability_id import AbilityId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.unit import UnitOrder

MAP = 'Flat32'


class PositionCapturer(BotAI):
    structure_positions = {}
    already_recorded_tags = set()

    async def on_step(self, iteration: int):
        if iteration % 10 == 0:
            self.capture_structure_positions()
        for worker in self.workers:
            if len(worker.orders) == 0:
                continue
            current_order: UnitOrder = worker.orders[0]
            # print(current_order)
            if current_order.ability.id == AbilityId.ATTACK:
                if isinstance(current_order.target, int) and current_order.target in self.townhalls.tags:
                    await self.chat_send('Saving building locations...')
                    self.log_structure_positions()
                    worker.stop()

    def capture_structure_positions(self):
        for structure in self.structures:
            if structure.tag in self.already_recorded_tags:
                continue
            if structure.type_id not in self.structure_positions:
                self.structure_positions[structure.type_id] = []
            self.structure_positions[structure.type_id].append(structure.position)
            self.already_recorded_tags.add(structure.tag)

    def log_structure_positions(self):
        path = pathlib.Path('../layouts').joinpath(MAP)
        os.makedirs(path, exist_ok=True)
        with open(path.joinpath(datetime.datetime.now().isoformat()), 'wb') as f:
            pickle.dump(self.structure_positions, f)


if __name__ == '__main__':
    run_game(maps.get(MAP), [
        Bot(Race.Protoss, PositionCapturer()),
        Computer(Race.Protoss, Difficulty.VeryEasy)
    ], realtime=True)

