from typing import List, Dict, Optional

import sc2math
from managers.manager import Manager
from blackboard import Role
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
from sc2.unit import Unit

MINING_RADIUS = 1.325


class MiningBooster(Manager):
    mining_stations: Optional[Dict[int, Point2]] = None

    def on_start(self):
        self.mining_stations = self.calculate_mining_stations()

    def on_step(self, iteration: int):
        workers = self.ai.workers
        for worker in workers:
            if self.should_speed_mine(worker):
                self.speed_mine(worker)
        pass

    def speed_mine(self, miner: Unit):
        if miner.is_carrying_resource:
            townhall = self.ai.townhalls.closest_to(miner.position)
            target = townhall.position.towards(miner.position, townhall.radius + miner.radius)
            if 0.75 < miner.distance_to(target) < 2:
                miner.move(target)
                # miner.return_resource(queue=True)
                miner(AbilityId.SMART, townhall, queue=True)
        elif miner.order_target:
            current_patch = self.ai.mineral_field.find_by_tag(miner.order_target)
            if current_patch is None:
                miner.stop()
                return
            target = self.mining_stations[current_patch.tag]
            if 0.75 < miner.distance_to(target) < 2:
                miner.move(target)
                miner.gather(current_patch, queue=True)

    def should_speed_mine(self, worker: Unit) -> bool:
        return (
            # minerals only for now
            self.blackboard.unit_roles[worker.tag] == Role.MINING_MINERALS
            # has not already been queued to speed mine
            and len(worker.orders) == 1
            # actually mining or returning
            and worker.orders[0].ability.id in [AbilityId.HARVEST_RETURN, AbilityId.HARVEST_GATHER]
        )

    def calculate_mining_stations(self) -> Dict[int, Point2]:
        base_centers: List[Point2] = self.ai.expansion_locations_list
        mining_stations: Dict[int, Point2] = {}

        for mf in self.ai.mineral_field:
            center = mf.position.closest(base_centers)
            target = mf.position.towards(center, MINING_RADIUS)
            close = self.ai.mineral_field.closer_than(MINING_RADIUS, target)
            for mf2 in close:
                if mf2.tag != mf.tag:
                    points = sc2math.get_intersections(mf.position, MINING_RADIUS, mf2.position, MINING_RADIUS)
                    if len(points) == 2:
                        target = center.closest(points)
            mining_stations[mf.tag] = target
        return mining_stations


class WorkerAssigner(Manager):
    def on_step(self, iteration: int):
        self.ai.distribute_workers()

        # mineral_patches = self.ai.mineral_field
        # available_patches = mineral_patches.filter(lambda p: any([p.distance_to(t) for t in self.ai.townhalls <= 8]))
        # available_patches.sort(key=lambda p: p.mineral_contents)
        # unassigned_miners = self.blackboard.unit_roles[Role.IDLE]
        # unfilled_patches = available_patches.filter(
        #     lambda p: len(self.blackboard.assigned_gather_targets.inv[p.tag]) < 2
        # )

