from typing import Optional

from blackboard import Blackboard
from interpreter import Interpreter
from operations.operation_base import Operation


class RootOperation(Operation):
    unit_assignment_desires = []
    debug_color = (20, 230, 230)

    # TODO consider some default child_ops here

    def __init__(self, interpreter: Interpreter, blackboard: Blackboard):
        super().__init__(
            parent_op=None,
            interpreter=interpreter,
            blackboard=blackboard,
            location=None
        )

    def on_step(self, iteration: int):
        self.claim_un_assigned_units()
        super().on_step(iteration)

    def claim_un_assigned_units(self):
        """This is the only time an operation assigns units to itself, because it has no parent"""
        assigned_unit_tags = set(self.assigned_unit_tags)
        for tag in self.interpreter.units.tags:
            if tag not in assigned_unit_tags:
                self.assign_unit(tag)
