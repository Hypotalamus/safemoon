from model.types.estimator import Estimator

class DFL_est(Estimator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_price_est(self):
        return self.impl.get_estimation()

    def get_dfl_est(self):
        prev_price = self.impl.get_prev_estimation()
        delta_price = self.impl.get_velocity_estimation()
        try:
            dfl_est = float(delta_price) / float(prev_price) * 100
            dfl_est = max( min(dfl_est, 1000), -1000 )
        except ZeroDivisionError:
            dfl_est = 0

        return dfl_est

    def update_estimation(self, new_price):
        self.impl.update_estimation(new_price)