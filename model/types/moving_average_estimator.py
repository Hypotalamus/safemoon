from collections import deque

class MovingAverageEstimator:
    def __init__(self, win_len=None):
        if win_len is None:
            win_len=14
        self.win_len = win_len
        self.dec = deque(maxlen=win_len)
        self.prev_est = None

    def get_estimation(self):
        try:
            est = sum(self.dec)/len(self.dec)
        except ZeroDivisionError:
            est = 0
        return est
    
    def get_prev_estimation(self):
        if len(self.dec) < 2:
            return 0
        else:
            return self.prev_est
    
    def get_velocity_estimation(self):
        if len(self.dec) < 2:
            return 0
        else:
            est = self.get_estimation()
            prev_est = self.get_prev_estimation()
            return est - prev_est        

    def update_estimation(self, new_val):
        self.prev_est = self.get_estimation()
        self.dec.appendleft(new_val)