def s_update_apy(params, substep, state_history, previous_state, policy_input):
    new_apy = policy_input['new_apy']
    return "APY", new_apy

def s_update_raw_apy(params, substep, state_history, previous_state, policy_input):
    new_raw_apy = policy_input['new_raw_apy']
    return "raw_APY", new_raw_apy

def s_update_raw_price(params, substep, state_history, previous_state, policy_input):
    new_raw_price = policy_input['new_raw_price']
    return "raw_price", new_raw_price

def s_update_price_est(params, substep, state_history, previous_state, policy_input):
    new_price_est = policy_input['new_price_est']
    return "price_est", new_price_est

def s_update_deflation(params, substep, state_history, previous_state, policy_input):
    new_dfl = policy_input['new_dfl']
    return "deflation", new_dfl

def s_update_holding(params, substep, state_history, previous_state, policy_input):
    new_sfm_holding = policy_input['new_sfm_holding']
    return "holding_SFMs", new_sfm_holding
