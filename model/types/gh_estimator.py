from filterpy.gh import GHFilter


class G_H_Estimator:
    def __init__(self, g=None, h=None):
        if g is None:
            g = 0.8
        if h is None:
            h = 0.2
        self.filter = GHFilter(x=0., dx=0.0, dt=1.0, g=g, h=h)
        self.prev_est = 0.0

    def get_estimation(self):
        return max(self.filter.x, 0)
    
    def get_prev_estimation(self):
        return self.prev_est
    
    def get_velocity_estimation(self):
        return self.filter.dx       

    def update_estimation(self, new_val):
        self.prev_est = self.get_estimation()
        self.filter.update(z=new_val)