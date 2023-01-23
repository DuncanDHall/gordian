import collections
import copy
import typing
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Generator
from dataclasses import dataclass
from typing import final, Optional, Union, List, Any

import sc2math
from blackboard import Blackboard
from interpreter import Interpreter
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit

UnitTag = int


@dataclass
class UnitDesire:
    count: int
    type: UnitTypeId
    importance: int
    location: Optional[Point2] = None  # for spatially sensitive recruitment
    unit_tags: Optional[set[UnitTag]] = None

    def desire_is_met(self) -> bool:
        return self.count <= len(self.unit_tags) if self.unit_tags else 0


class Operation(metaclass=ABCMeta):
    debug: bool = True
    parent_op: Optional['Operation']
    interpreter: Interpreter
    blackboard: Blackboard
    location: Optional[Point2]
    assigned_unit_tags: list[UnitTag]  # tags for all units assigned to this operation
    child_op_types: list[typing.Type['Operation']] = []
    child_ops: set['Operation']
    _unit_delegations: dict[UnitTag, 'Operation']  # which child op each unit is delegated to
    unit_assignment_desires: list[UnitDesire] = []
    debug_color: tuple[int]

    @property
    def assigned_units(self) -> list[Unit]:
        return [self.interpreter.unit(tag) for tag in self.assigned_unit_tags]

    def __init__(self, parent_op: Optional['Operation'], interpreter: Interpreter, blackboard: Blackboard,
                 location: Optional[Point2] = None):
        """For Operation implementations, optionally set self.child_ops in the __init__() and then call
        super().__init__()"""
        self.parent_op = parent_op
        self.interpreter = interpreter
        self.blackboard = blackboard
        self.location = location
        self._unit_delegations = {}

        # pull unit_assignment_desires from class property to instance property
        # TODO test this method actually does this ^
        self.unit_assignment_desires = copy.deepcopy(self.__class__.unit_assignment_desires)
        self.unit_assignment_desires.sort(key=lambda d: d.importance, reverse=True)
        for desire in self.unit_assignment_desires:
            desire.unit_tags = set()

        # set up child_ops according to spec in child class
        self.child_ops = {ChildOpType.init_with_parent(self) for ChildOpType in self.child_op_types}

    @classmethod
    def init_with_parent(cls, parent_op: 'Operation', location: Optional[Point2] = None) -> 'Operation':
        op = cls(parent_op, parent_op.interpreter, parent_op.blackboard, location)
        return op

    # MARK: unit assignment by parent op

    @final
    def assign_unit(self, tag: UnitTag):
        self.assigned_unit_tags.append(tag)
        unit = self.interpreter.unit(tag)
        for desire in self.unit_assignment_desires:
            if unit.type_id == desire.type and not desire.desire_is_met():
                desire.unit_tags.add(tag)
                break
        self._delegate_un_delegated_units()

    @final
    def un_assign_unit(self, tag: UnitTag):
        self._un_delegate_unit(tag)
        unit = self.interpreter.unit(tag)
        for desire in reversed(self.unit_assignment_desires):
            if unit.type_id == desire.type:
                desire.unit_tags.remove(tag)
        self.assigned_unit_tags.remove(tag)

    @final
    def unit_desire_amount(self, tag: UnitTag) -> int:
        """Calculates a desire score for that unit from desire fulfillment status, location, etc. """
        # TODO tune these weights / rework this function entirely
        unit = self.interpreter.unit(tag)
        desires = [d for d in self.unit_assignment_desires if d.type == unit.type_id]
        location_weight = 0.1
        importance_weight = 1
        scarcity_weight = 1

        if not desires:
            return -1

        total = 0
        for desire in desires:
            location_factor = (
                -1 * location_weight * sc2math.linear_distance(unit.position, self.location.position)
                if self.location else 0
            )
            importance_factor = importance_weight * desire.importance
            scarcity_factor = scarcity_weight * (desire.count - len(desire.unit_tags))
            total += location_factor + importance_factor + scarcity_factor

        return total

    @final
    def least_desired_units(self) -> Generator[tuple[UnitTag, int]]:
        """Return currently assigned units in order of least importance, and its level of importance"""
        for desire in sorted(self.unit_assignment_desires, key=lambda d: d.importance, reverse=True):
            if desire.unit_tags is None:
                continue
            for tag in desire.unit_tags:
                yield tag, desire.importance

    # MARK: unit delegation to children

    @final
    def _delegate_unit(self, tag: UnitTag, op: 'Operation'):
        self._unit_delegations[tag] = op
        op.assign_unit(tag)

    @final
    def _un_delegate_unit(self, tag: UnitTag):
        for op, delegations in self._unit_delegations:
            if tag in delegations:
                delegations.remove(tag)
            op.un_assign_unit(tag)

    @final
    def _delegate_un_delegated_units(self):
        """Make intelligent delegations of un delegated assigned units across ops"""
        if not self.child_ops:
            return
        for un_delegated_unit_tag in filter(lambda au: au not in self._unit_delegations, self.assigned_unit_tags):
            bids = [(op.unit_desire_amount(un_delegated_unit_tag), op) for op in self.child_ops]
            top_bid, top_bidder = max(bids)
            if top_bid > 0:
                self._delegate_unit(un_delegated_unit_tag, top_bidder)

    # MARK: game steps

    def on_before_start(self):
        for child_op in self.child_ops:
            child_op.on_before_start()

    def on_start(self):

        self.assigned_unit_tags = []
        for child_op in self.child_ops:
            child_op.on_start()

    def on_step(self, iteration: int):
        # TODO: self.check_for_destroyed_unit_assignments()
        for child_op in self.child_ops:
            child_op.on_step(iteration)
        if self.debug:
            self.draw_assignee_debug_labels()

    debug_color = (200, 200, 200)

    def draw_assignee_debug_labels(self):
        importance_lookup = {
            t: d.importance
            for d in self.unit_assignment_desires
            for t in d.unit_tags
        }
        for assignee in self.assigned_units:
            if all([assignee.tag not in op.assigned_unit_tags for op in self.child_ops]):
                importance = importance_lookup.get(assignee.tag, "-1")
                label = f'#{assignee.tag}\n{type(self).__name__}:{importance}'
                self.interpreter.client.debug_text_3d(label, assignee, self.debug_color, size=16)

    # MARK: misc

    @final
    def _add_child_op(self, op: 'Operation'):
        """Handles all the plumbing of adopting a child operation"""
        # add to child_ops
        # delegate units to child
        pass
