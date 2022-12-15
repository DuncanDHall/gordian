from managers.manager_base import Manager
from sc2.units import Units


class WorkerSplitter(Manager):
    def on_before_start(self):
        mf: Units = self.ai.mineral_field
        for w in self.ai.workers:
            w.gather(mf.closest_to(w))

    def on_step(self, iteration: int):
        pass
