import unittest

from blackboard import UnitRoles, Role


class TestBlackboardUnitRoles(unittest.TestCase):
    def setUp(self) -> None:
        self.unit_roles = UnitRoles()
        self.unit_roles[0] = Role.IDLE
        self.unit_roles[1] = Role.IDLE
        self.unit_roles[2] = Role.MINING_MINERALS

    def test_get_unit_role(self) -> None:
        assert self.unit_roles[0] == Role.IDLE
        assert self.unit_roles[2] == Role.MINING_MINERALS

    def test_get_unit_tags_for_role(self) -> None:
        print(self.unit_roles)
        assert len(self.unit_roles.tags_for_role(Role.IDLE)) == 2
        assert len(self.unit_roles.tags_for_role(Role.MINING_MINERALS)) == 1
