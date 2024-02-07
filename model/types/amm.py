class AMM:
    def __init__(self, init_USDT=1e6, init_SFM=1e6):
        self.reinit(init_USDT, init_SFM)

    def reinit(self, init_USDT, init_SFM):
        self.USDT_balance = init_USDT
        self.SFM_balance = init_SFM       

    def get_raw_price(self):
        try:
            return self.USDT_balance / self.SFM_balance
        except ZeroDivisionError:
            return 0
    
    def swap_usdt_to_sfm(self, usdt_amount):
        k = self.USDT_balance * self.SFM_balance
        self.USDT_balance += usdt_amount
        sfm_amount = self.SFM_balance - k / self.USDT_balance
        self.SFM_balance -= sfm_amount
        return sfm_amount
    
    def swap_sfm_to_usdt(self, sfm_amount):
        k = self.USDT_balance * self.SFM_balance
        self.SFM_balance += sfm_amount
        usdt_amount = self.USDT_balance - k / self.SFM_balance
        self.USDT_balance -= usdt_amount
        return usdt_amount

    def addLiquidity(self, usdt_amount, sfm_amount):
        l = min(usdt_amount/self.USDT_balance, sfm_amount/self.SFM_balance)
        self.USDT_balance += l * self.USDT_balance
        self.SFM_balance += l * self.SFM_balance