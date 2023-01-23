from typing import Dict, Optional, Union

import sc2math
from operations.operation_base import Operation, UnitDesire
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit

MINING_RADIUS = 1.325


class SpeedMineOp(Operation):
    mining_stations: Optional[dict[int, Point2]]
    unit_assignment_desires = [
        UnitDesire(200, UnitTypeId.PROBE, 2),
        UnitDesire(200, UnitTypeId.SCV, 2),
        UnitDesire(200, UnitTypeId.DRONE, 2),
    ]
    debug_color = (255, 139, 108)

    def on_start(self):
        self.mining_stations = self._calculate_mining_stations()
        super().on_start()

    def on_step(self, iteration: int):
        for worker in self.assigned_units:
            if self._should_speed_mine(worker):
                self.speed_mine(worker)
        super().on_step(iteration)

    def speed_mine(self, miner: Unit):
        if miner.is_carrying_resource:
            # maybe queue a move before returning to townhall
            townhall = self.interpreter.townhalls.closest_to(miner.position)
            target = townhall.position.towards(miner.position, townhall.radius + miner.radius)
            if 0.75 < miner.distance_to(target) < 2:
                miner.move(target)
                # miner.return_resource(queue=True)
                miner(AbilityId.SMART, townhall, queue=True)
        elif miner.order_target:
            current_patch = self.interpreter.mineral_fields.find_by_tag(miner.order_target)
            if current_patch is None:
                # TODO do we need to do anything when a patch mines out?
                return
            target = self.mining_stations[current_patch.tag]
            if 0.75 < miner.distance_to(target) < 2:
                miner.move(target)
                miner.gather(current_patch, queue=True)

    @staticmethod
    def _should_speed_mine(worker: Unit) -> bool:
        return (
            # has not already been queued to speed mine
            len(worker.orders) == 1
            # actually mining or returning
            and worker.orders[0].ability.id in [AbilityId.HARVEST_RETURN, AbilityId.HARVEST_GATHER]
        )

    def _calculate_mining_stations(self) -> dict[int, Point2]:
        base_centers: list[Point2] = self.interpreter.expansion_locations
        mining_stations: dict[int, Point2] = {}

        for mf in self.interpreter.mineral_fields:
            center = mf.position.closest(base_centers)
            target = mf.position.towards(center, MINING_RADIUS)
            close = self.interpreter.mineral_fields.closer_than(MINING_RADIUS, target)
            for mf2 in close:
                if mf2.tag != mf.tag:
                    points = sc2math.get_intersections(mf.position, MINING_RADIUS, mf2.position, MINING_RADIUS)
                    if len(points) == 2:
                        target = center.closest(points)
            mining_stations[mf.tag] = target
        return mining_stations
