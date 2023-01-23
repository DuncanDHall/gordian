import typing

from operations.operation_base import Operation, UnitDesire
from operations.root_operation_base import RootOperation
from operations.speed_mine import SpeedMineOp
from sc2.ids.unit_typeid import UnitTypeId


class PvXGlobalOp(RootOperation):
    unit_assignment_desires = []
    child_op_types = [
        # TODO
        # BuildWishlistOp,
        SpeedMineOp,
        # WishlistWorkersOp,
        # DefendBaseOp,
        # ScoutOp,
        # DamageOpponentOp
    ]

    # set any global parameters using self.blackboard
