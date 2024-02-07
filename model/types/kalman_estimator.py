import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

class KalmanEstimator:
    def __init__(self, proc_std=None, meas_std=None, guess_std=None):
        if proc_std is None:
            proc_std = 0.1
        if meas_std is None:
            meas_std = 0.3
        if guess_std is None:
            guess_std = 5
        dt = 1.0
        # initialize filter
        #======================================================
        self.filter = KalmanFilter(dim_x=2, dim_z=1)
        # set state transition matrix
        self.filter.F = np.array([[1, dt],
                                  [0,  1]])
        # set process noise matrix
        self.filter.Q = Q_discrete_white_noise(dim=2, dt=dt, var=proc_std**2)
        # set control input
        self.filter.u = 0.0
        # set measurement matrix
        self.filter.H = np.array([[1.0, 0.0]])
        # set measurement noise matrix
        self.filter.R = np.array([[meas_std**2]])
        # set initial state
        self.filter.x = np.array([0.0, 0.0])
        # set initial guess
        self.filter.P = np.diag([guess_std**2, guess_std**2])    
        #======================================================
        self.prev_est = 0

    def get_estimation(self):
        return max(self.filter.x[0], 0)
    
    def get_prev_estimation(self):
        return self.prev_est
    
    def get_velocity_estimation(self):
        return self.filter.x[1]       

    def update_estimation(self, new_val):
        self.prev_est = self.get_estimation()
        self.filter.predict()
        self.filter.update(new_val)