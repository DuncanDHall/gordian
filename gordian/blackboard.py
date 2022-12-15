from enum import Enum
from typing import Tuple, Union

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from utils import ReversibleDict, EventList

UnitOrUpgradeId = Union[UnitTypeId, UpgradeId]


class Blackboard:
    def __init__(self, build_list: list[UnitOrUpgradeId]):
        self.unit_roles: UnitRoles[int, Role] = UnitRoles()
        self.wish_list: Wishlist = Wishlist(build_list)
        # self.build_plan: BuildPlan = BuildPlan()
        self.vespene_mining_percent = 0.28


class Role(Enum):
    IDLE = 0
    MINING_MINERALS = 1
    MINING_GAS = 2
    BUILDING = 3


class UnitRoles(ReversibleDict[int, Role]):
    """Associates unit tags with roles to inform re-tasking decisions"""
    def tags_for_role(self, role: Role):
        return self.inv.get(role, [])

    def __getitem__(self, tag: int) -> Role:
        return super().get(tag, Role.IDLE)


class Wishlist(EventList[UnitOrUpgradeId]):

    def __init__(self, seq=()):
        super().__init__()
        self.did_change = False
        self.callback = self.did_change_callback
        for item in seq:
            self.append(item)

    def did_change_callback(self):
        self.did_change = True

