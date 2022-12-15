from managers.manager_base import Manager


class ManagerScheduler:
    managers: list[Manager]

    def __init__(self, managers, blackboard):
        self.managers = managers
        self.blackboard = blackboard

    def on_step(self, iteration: int):
        # could prioritize managers depending on the blackboard
        for manager in self.managers:
            manager.on_step(iteration)

