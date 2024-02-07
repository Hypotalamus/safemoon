class ExponentialAverageEstimator:
    def __init__(self, alpha=None):
        if alpha is None:
            alpha = 0.9
        self.alpha = alpha
        self.est = 0
        self.prev_est = 0

    def get_estimation(self):
        return self.est
    
    def get_prev_estimation(self):
        return self.prev_est
    
    def get_velocity_estimation(self):
        return self.est - self.prev_est       

    def update_estimation(self, new_val):
        self.prev_est = self.est
        self.est = self.alpha * new_val + (1 - self.alpha) * self.prev_est