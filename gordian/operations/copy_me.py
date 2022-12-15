from operations.operation_base import Operation


class CopyMe(Operation):
    desired_units: []

    def on_step_body(self, iteration):
        pass
