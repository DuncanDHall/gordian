from blackboard import Role
from managers.manager_base import Manager


class RoleManager(Manager):
    def on_step(self, iteration: int):
        for idle_worker in self.ai.workers.filter(lambda w: self.blackboard.unit_roles[w.tag] == Role.IDLE):
            self.blackboard.unit_roles[idle_worker.tag] = Role.MINING_MINERALS

        # TODO check blackboard and current unit orders/status for other cases for role change
