import numpy as np
from model.utils import randomize

from model.types.amm import AMM
from model.types.sfm_manager import SFM_manager
from model.types.apy_est import APY_est
from model.types.dfl_est import DFL_est

amm = AMM()
sfm_manager = SFM_manager()
apy_est = APY_est()
dfl_est = DFL_est()

def p_initialize_sim(params, substep, state_history, previous_state):
    init_liquidity_USDT = params['init_liquidity_USDT']
    init_liquidity_SFM = params['init_liquidity_SFM']
    tSupply = params['tSupply']
    decimals = params['decimals']
    rebaseFee = params['rebaseFee_pct'] / 100
    liquidityFee = params['liquidityFee_pct'] / 100
    apy_est_kwargs = params['apy_est_kwargs']
    dfl_est_kwargs = params['dfl_est_kwargs']

    sfm_holding = previous_state['holding_SFMs']

    if previous_state['timestep'] == 0:
        np.random.seed(seed=previous_state['simulation']+previous_state['run'])
        amm.reinit(init_liquidity_USDT, init_liquidity_SFM)
        sfm_manager.reinit(tSupply, decimals, rebaseFee, liquidityFee)
        apy_est.reinit(**apy_est_kwargs)
        dfl_est.reinit(**dfl_est_kwargs)   

    return {
        'new_sfm_holding': sfm_holding,         
    }

def p_calculate_profit(params, substep, state_history, previous_state):

    new_raw_apy = sfm_manager.get_raw_apy()
    new_apy = apy_est.get_estimation()
    new_raw_price = amm.get_raw_price()
    new_price_est = dfl_est.get_price_est()
    new_dfl = dfl_est.get_dfl_est()
    if previous_state['timestep'] == 150 and previous_state['subset'] == 3:
        print(f"Final covariance state matrix: {apy_est.impl.filter.P}")
        print(f"Final covariance state matrix: {dfl_est.impl.filter.P}")

    return {
        'new_raw_apy': new_raw_apy,
        'new_apy': new_apy,
        'new_dfl': new_dfl,
        'new_raw_price': new_raw_price,
        'new_price_est': new_price_est, 
    }

def p_account_inflow(params, substep, state_history, previous_state):
    get_var_inflow = params['var_inflow_USD']
    get_apy_inflow = params['inflow_from_apy_over_market_USD']
    rand_mag = params['rand_mag']
    const_inflow_USD = params['const_inflow_USD']
    apy_market_pct = params['APY_market_pct']

    day = previous_state['timestep']
    apy = previous_state['APY']
    deflation = previous_state['deflation']
    sfm_holding = previous_state['holding_SFMs']

    marketing_inflow = get_var_inflow(day)
    marketing_inflow = randomize(marketing_inflow, rand_mag)
    const_inflow = randomize(const_inflow_USD, rand_mag)
    apy_over_market = apy + deflation - apy_market_pct
    apy_over_market_inflow = get_apy_inflow(apy_over_market)
    apy_over_market_inflow = randomize(apy_over_market_inflow, rand_mag)
    total_inflow = marketing_inflow + const_inflow + apy_over_market_inflow
    new_sfm_holding = amm.swap_usdt_to_sfm(total_inflow)
    new_sfm_holding += sfm_holding

    return {
        'new_sfm_holding': new_sfm_holding 
    }

def p_account_outflow(params, substep, state_history, previous_state):
    const_outflow = params['const_outflow_pct'] / 100
    apy_market_pct = params['APY_market_pct']
    get_apy_outflow = params['profit_to_churnrate']
    rand_mag = params['rand_mag']    

    sfm_holding = previous_state['holding_SFMs']
    apy = previous_state['APY']
    deflation = previous_state['deflation']

    const_outflow = randomize(const_outflow, rand_mag)
    apy_over_market = apy + deflation - apy_market_pct
    apy_over_market_outflow = get_apy_outflow(apy_over_market)
    apy_over_market_outflow = randomize(apy_over_market_outflow, rand_mag)
    total_churn_rate = min(const_outflow + apy_over_market_outflow, 1)
    total_outflow = sfm_holding * total_churn_rate
    new_sfm_holding = sfm_manager.make_sale(total_outflow, sfm_holding, amm)

    new_raw_apy = sfm_manager.get_raw_apy()
    new_raw_price = amm.get_raw_price()
    apy_est.update_estimation(new_raw_apy)
    dfl_est.update_estimation(new_raw_price)

    return {
        'new_sfm_holding': new_sfm_holding
    }