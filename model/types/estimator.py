from model.types.moving_average_estimator import MovingAverageEstimator
from model.types.exponential_average_estimator import ExponentialAverageEstimator
from model.types.gh_estimator import G_H_Estimator
from model.types.kalman_estimator import KalmanEstimator

class Estimator:
    def __init__(self, **kwargs):
        self.reinit(**kwargs)

    def reinit(self, **kwargs):
        if "impl" in kwargs:
            impl_val = kwargs["impl"]
            match impl_val:
                case "moving_avg":
                    win_len = None
                    if "win_len" in kwargs:
                        win_len = kwargs["win_len"]
                    self.impl = MovingAverageEstimator(win_len=win_len)
                case "exp_avg":
                    alpha = None
                    if "alpha" in kwargs:
                        alpha = kwargs["alpha"]
                    self.impl = ExponentialAverageEstimator(alpha=alpha)
                case "g_h":
                    g, h = None, None
                    if "g" in kwargs:
                        g = kwargs["g"]
                    if "h" in kwargs:
                        h = kwargs["h"]
                    self.impl = G_H_Estimator(g=g, h=h)
                case "kalman":
                    proc_std, meas_std, guess_std = None, None, None
                    if "proc_std" in kwargs:
                        proc_std = kwargs["proc_std"]
                    if "meas_std" in kwargs:
                        meas_std = kwargs["meas_std"]
                    if "guess_std" in kwargs:
                        guess_std = kwargs["guess_std"]
                    self.impl = KalmanEstimator(proc_std=proc_std, meas_std=meas_std, guess_std=guess_std)
                case _:
                    self.impl = MovingAverageEstimator()
        else:
            self.impl = MovingAverageEstimator()