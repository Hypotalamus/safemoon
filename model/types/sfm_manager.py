MAX = 2**256 - 1

class SFM_manager:
    def __init__(self, tSupply=10**12, decimals=9, rebaseFee=0.05, liquidityFee=0.05):
        self.reinit(tSupply, decimals, rebaseFee, liquidityFee)

    def reinit(self, tSupply=10**12, decimals=9, rebaseFee=0.05, liquidityFee=0.05):       
        self.tSupply = tSupply
        self.decimals = decimals
        self.rebaseFee = rebaseFee
        self.liquidityFee = liquidityFee
        self.total = tSupply * 10**decimals
        self.rTotal = MAX - MAX % self.total
        self.apy = 0

    def make_sale(self, sfm_amount, sfm_holding, amm):
        rebaseFee_part = sfm_amount * self.rebaseFee
        liquidityFee_part = sfm_amount * self.liquidityFee
        swap_part = sfm_amount - rebaseFee_part - liquidityFee_part
        # 1. Fill liquidity pool
        self._addLiquidity(liquidityFee_part, amm)
        # 2. Swap tokens
        _ = amm.swap_sfm_to_usdt(swap_part)
        remaining_sfm = sfm_holding - sfm_amount
        # 3. Rebase remaining SFMs
        new_sfm_holding = self._rebase(rebaseFee_part, remaining_sfm)
        return new_sfm_holding

    def get_raw_apy(self):
        return self.apy
    
    def _addLiquidity(self, sfm_amount, amm):
        sfm_to_usdt_amount = sfm_amount / 2
        sfm_to_pool_amount = sfm_amount - sfm_to_usdt_amount
        usdt_to_pool_amount = amm.swap_sfm_to_usdt(sfm_to_usdt_amount)
        # Small amount of USDT will be leftover in contract. See Certik's audit.
        amm.addLiquidity(usdt_to_pool_amount, sfm_to_pool_amount)        

    def _rebase(self, rebaseFee, remaining_sfm):
        rate_old = self._getRate()
        rFee = rebaseFee * 10**self.decimals * rate_old
        self.rTotal -= rFee
        rate_new = self._getRate()
        assert rate_new > 1e-12, "Error. Rate became too small during rebasing."
        self.apy = (rate_old - rate_new) / rate_new * 100 * 365
        return remaining_sfm * rate_old / rate_new

    def _getRate(self):
        return self.rTotal / self.total