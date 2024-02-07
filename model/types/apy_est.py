from model.types.estimator import Estimator

class APY_est(Estimator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_estimation(self):
        return self.impl.get_estimation()

    def update_estimation(self, new_apy):
        self.impl.update_estimation(new_apy)