import copy
from asyncio import PriorityQueue
from enum import Enum
from typing import Tuple, Union, Set, List, Optional

import unit_categories
from blackboard import UnitOrUpgradeId, Wishlist, Blackboard
from manager_base import Manager
from sc2.bot_ai import BotAI
from sc2.dicts.unit_trained_from import UNIT_TRAINED_FROM
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

BuildPlan = PriorityQueue[Tuple[float, UnitOrUpgradeId]]
# EventsPlan = PriorityQueue[Tuple[float, Union[]]]

VESPENE_PROPORTION = 6 / 22
MINERAL_MINE_RATE = 1.0
VESPENE_MINE_RATE = 0.9433962264

MIN_MINERAL_COST = 25


# class SimEventType(Enum):
#     SIM_START = 0,
#     STARTED = 1,
#     BUSY = 2,
#     READY = 3
#
#
# class SimEvent:
#     time: float
#     game_type_id: Optional[UnitOrUpgradeId]
#     event_type: SimEventType
#
#     def __init__(self, time: float, game_type_id: UnitOrUpgradeId, event_type: SimEventType):
#         self.time = time
#         self.game_type_id = game_type_id
#         self.event_type = event_type
#
#
# class SimState:
#     time: float
#     minerals: int
#     vespene: int
#     workers: list[UnitTypeId]
#     supply_used: float
#     supply_cap: float
#     all_structures: list[UnitTypeId]
#     incomplete_structures: list[UnitTypeId]
#     idle_structures: list[UnitTypeId]
#     busy_structures: list[UnitTypeId]
#     upgrades: set[UpgradeId]
#     events: list[SimEvent]
#
#     def __init__(self, ai: BotAI):
#         self._ai = ai
#         self.time = ai.time
#         self.minerals = ai.minerals
#         self.vespene = ai.vespene
#         self.workers = [w.type_id for w in ai.workers]
#         self.supply_used = ai.supply_used
#         self.supply_cap = ai.supply_cap
#         self.all_structures = [s.type_id for s in ai.structures]
#         self.incomplete_structures = [s.type_id for s in ai.structures if not s.is_ready]  # TODO remove?
#         self.idle_structures = [s.type_id for s in ai.structures if not s.is_active and s.is_ready]
#         self.busy_structures = [s.type_id for s in ai.structures if s.is_active and s.is_ready]
#         self.upgrades = ai.state.upgrades
#
#         self.events = self._get_starting_events()
#         self.next_event_index = 0
#
#         self.save_point: Optional[SimState] = None
#
#     def _get_starting_events(self) -> list[SimEvent]:
#         # add sim_start event
#         pass
#
#     def add_events_for(self, game_type_id_to_start: UnitOrUpgradeId):
#         # calculate delta_t between current state and next time can start
#         # delta_t = self.time_till_can_afford(game_type_id_to_start)
#         # events.insert(event_index, SimEvent(state.time + delta_t, game_type_id_to_start, SimEventType.STARTED))
#         pass
#
#     @property
#     def resource_incomes(self) -> Tuple[float, float]:
#         vespene_miners = int(len(self.workers) * VESPENE_PROPORTION + 0.5)
#         mineral_miners = len(self.workers) - vespene_miners
#         return mineral_miners * MINERAL_MINE_RATE, vespene_miners * VESPENE_MINE_RATE
#
#     def can_start(self, game_type_id: UnitOrUpgradeId) -> bool:
#         cost = self._ai.calculate_cost(game_type_id)
#         # check resource requirements
#         if cost.minerals > self.minerals or cost.vespene > self.vespene:
#             return False
#         # check supply requirements
#         if isinstance(game_type_id, UnitTypeId):
#             supply_cost = self._ai.calculate_supply_cost(game_type_id)
#             if supply_cost and supply_cost > self.supply_cap - self.supply_used:
#                 return False
#         # check building requirements
#         if self._ai.tech_requirement_progress(game_type_id) < 1:
#             return False
#         # check research requirements
#         # TODO: upgrades
#         # check production requirements
#         if game_type_id in unit_categories.WARRIORS:
#             if UNIT_TRAINED_FROM[game_type_id] not in self.idle_structures:
#                 return False
#         return True
#
#     def sim_forward(self, steps: int = 1):
#         """Simulates through the next event, updating the state accordingly"""
#         if self.next_event_index + steps > len(self.events):
#             raise IndexError('Simulation does not have that many events')
#
#         for _ in range(steps):
#             next_event = self.events[self.next_event_index]
#
#             # resource income
#             delta_t: float = next_event.time - self.time
#             self.time = next_event.time
#             mineral_income, vespene_income = self.resource_incomes
#             self.minerals += int(delta_t * mineral_income)
#             self.vespene += int(delta_t * vespene_income)
#
#             # resource and production costs/availability adjustments
#             if next_event.event_type == SimEventType.STARTED:
#                 cost = self._ai.calculate_cost(next_event.game_type_id)
#                 self.minerals -= cost.minerals
#                 self.vespene -= cost.vespene
#                 self.supply_used += self._ai.calculate_supply_cost(next_event.game_type_id)
#                 if next_event.game_type_id in unit_categories.WARRIORS:
#                     production_structure_id = [
#                         p for p in UNIT_TRAINED_FROM[next_event.game_type_id]
#                         if p in self.idle_structures
#                     ][0]
#                     self.idle_structures.remove(production_structure_id)
#                     self.busy_structures.append(production_structure_id)
#                 elif next_event.game_type_id in unit_categories.STRUCTURES:
#                     self.incomplete_structures.append(next_event.game_type_id)
#                 elif next_event.game_type_id in UpgradeId:
#                     pass
#             elif next_event.event_type == SimEventType.BUSY:
#                 if next_event.game_type_id in unit_categories.WARRIORS:
#                     raise TypeError('Warriors should not be SimEvent.BUSY')
#                 elif next_event.game_type_id in unit_categories.STRUCTURES:
#                     self.idle_structures.remove(next_event.game_type_id)
#                     self.busy_structures.append(next_event.game_type_id)
#                 elif next_event.game_type_id in UpgradeId:
#                     raise TypeError('Upgrades should not be SimEvent.BUSY')
#             elif next_event.event_type == SimEventType.READY:
#                 if next_event.game_type_id in unit_categories.WARRIORS:
#                     raise TypeError('Warriors should not be SimEvent.READY')
#                 elif next_event.game_type_id in unit_categories.STRUCTURES:
#                     self.busy_structures.remove(next_event.game_type_id)
#                     self.idle_structures.append(next_event.game_type_id)
#                 elif next_event.game_type_id in UpgradeId:
#                     self.upgrades.add(next_event.game_type_id)
#
#             # validation and state saving
#             self._validate_sim_state()
#             if self.minerals < MIN_MINERAL_COST:
#                 self._save_state()
#
#             self.next_event_index += 1
#
#     def time_till_can_afford(self, game_type_id_to_start) -> float:
#         pass
#
#     def reset_to_saved_point(self):
#         if self.save_point is None:
#             return
#         self.__dict__.update(self.save_point.__dict__)
#
#     def _save_state(self):
#         self.save_point = copy.deepcopy(self)
#         self.save_point.__dict__.pop('events')
#         self.save_point.__dict__.pop('save_point')
#
#     def _validate_sim_state(self):
#         assert (self.time > 0.0, 'Negative time')
#         assert (self.minerals > 0, 'Negative minerals')
#         assert (self.vespene > 0, 'Negative vespene')
#         assert (self.supply_used > self.supply_cap, 'Over supply cap')
#         assert (
#             len(self.all_structures) ==
#             len(self.incomplete_structures) + len(self.idle_structures) + len(self.busy_structures),
#             'Structure accounting is off...'
#         )
#
#     def get_build_plan(self) -> BuildPlan:
#         pass
#
#
# class BuildSolver(Manager):
#     """Calculates the timings of various items on the wishlist"""
#
#     def on_step(self, iteration: int):
#         wish_list = self.blackboard.wish_list
#         if not wish_list.did_change:
#             return
#         self.blackboard.build_plan = self.calculate_build_plan(self.blackboard.wish_list)
#         wish_list.did_change = False
#
#     def calculate_build_plan(self, wish_list: Wishlist) -> BuildPlan:
#         # get starting state
#         state = SimState(self.ai)
#
#         # foreach UnitOrBuildId in wish_list
#         for quantity, game_type_id_to_start in wish_list:
#             # reset state to last cache where minerals = 0 (assumption: everything costs minerals)
#             state.reset_to_saved_point()
#
#             while not state.can_start(game_type_id_to_start):
#                 # plan the sim forward
#                 state.sim_forward()
#             # insert entry(ies) into events_plan at a calculated time before this point
#             state.add_events_for(game_type_id_to_start)
#
#         # translate events_plan into build_plan
#         return state.get_build_plan()
#
#         # TODO when to inject pylons?


class MVPBuildSolver(Manager):
    """TODO replace this with a smarter solver (see above)"""
    def on_step(self, iteration: int):
        wish_list = self.blackboard.wish_list
        if not wish_list.did_change:
            return
        self.blackboard.build_plan = self.calculate_build_plan(self.blackboard.wish_list)
        wish_list.did_change = False

    def calculate_build_plan(self, wish_list: list[UnitOrUpgradeId]):
        """THIS IS SUPER NAIVE - does not account for production requirements,
        tech requirements, supply, or anything really"""
        build_plan: list[Tuple[float, UnitOrUpgradeId]] = []
        t: float = self.ai.time
        minerals = self.ai.minerals
        vespene = self.ai.vespene
        worker_count = len(self.ai.workers)
        mineral_ratio = 0.72727272
        vespene_ratio = 0.27272727

        for item_id in wish_list:
            # calculate next time can afford
            cost = self.ai.calculate_cost(item_id)
            delta_t = max(
                (cost.minerals - minerals) / mineral_ratio * worker_count,
                (cost.vespene - vespene) / vespene_ratio * worker_count,
                0
            )

            # fast forward to that time
            minerals += delta_t * mineral_ratio * worker_count
            vespene += delta_t * vespene_ratio * worker_count
            t += delta_t

            # pay the cost
            minerals -= cost.minerals
            vespene -= cost.vespene
            build_plan.append((t, item_id))

        return build_plan
