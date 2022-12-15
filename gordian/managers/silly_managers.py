from manager_base import Manager


class WorkerRushManager(Manager):
    def on_step(self, iteration: int):
        if iteration == 0:
            for worker in self.ai.workers:
                worker.attack(self.ai.enemy_start_locations[0])