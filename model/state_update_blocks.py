from model.parts.policy_functions import *
from model.parts.state_update_functions import *


partial_state_update_blocks = [

    # Инициализация симуляции
    {
        'policies': {
            'initialize_sim': p_initialize_sim,
        },
        'variables': {
            'holding_SFMs': s_update_holding,            
        }
    },

    # Рассчитываю текущие показатели доходности
    {
        'policies': {
            'calculate_profit': p_calculate_profit,
        },
        'variables': {
            'raw_APY': s_update_raw_apy,
            'APY': s_update_apy,
            'raw_price': s_update_raw_price,
            'price_est': s_update_price_est,
            'deflation': s_update_deflation,
        }
    },

    # Приток пользователей
    {
        'policies': {
            'account_inflow': p_account_inflow,
        },
        'variables': {
            'holding_SFMs': s_update_holding,
        }
    },

    # Отток пользователей
    {
        'policies': {
            'account_outflow': p_account_outflow,
        },
        'variables': {
            'holding_SFMs': s_update_holding,
        }
    },    
]