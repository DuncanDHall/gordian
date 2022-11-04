from enum import Enum

import bidict as bidict

from utils import ReversibleDict


class BlackBoard:
    def __init__(self):
        self.unit_roles = UnitRoles()


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
        if tag in self:
            return self[tag]
        return Role.IDLE
