from dataclasses import dataclass
from typing import List, Callable, Any
from radcad.utils import default
from model.utils import get_marketing_inflow, get_churnrate_from_profit, get_apy_over_market_inflow


@dataclass
class Parameters:
    ############################################
    # Параметры, формирующие спрос на токен
    ############################################
    const_inflow_USD: List[float]=default([200.]) # Средства, которые приходят в проект независимо от прочих факторов
    APY_market_pct: List[float]=default([10.0]) # Средний APY по крипторынку
    const_outflow_pct: List[float]=default([0.5]) # % пользователей, продающих токен по личным причинам

    ############################################
    # Параметры токена
    ############################################
    tSupply: List[int]=default([10**10]) # Полное предложение токена
    decimals: List[int]=default([9]) # Количество знаков после запятой
    rebaseFee_pct: List[float]=default([5.0]) # Комиссия, удерживаемая при продаже токена в пользу ребейса
    liquidityFee_pct: List[float]=default([5.0]) # Комиссия, идущая в пул ликвидности

    ############################################
    # Начальные параметры пула ликвидности; 0.001$ - начальная цена токена
    ############################################
    init_liquidity_USDT: List[float]=default([1e5])
    init_liquidity_SFM: List[float]=default([1e8])

    ############################################
    # Вызываемые функции
    ############################################
    var_inflow_USD: List[Callable[[int], float]]=default([get_marketing_inflow]) # Средства, приходящие в проект за счет рекламы
    inflow_from_apy_over_market_USD: List[Callable[[float], float]]=default([get_apy_over_market_inflow]) # Средства, приходящие в проект за счет ожидаемой прибыли
    profit_to_churnrate: List[Callable[[float], float]]=default([get_churnrate_from_profit]) # Отток пользователей при данной ожидаемой прибыли

    ############################################
    # Параметры оценщиков
    ############################################
    apy_est_kwargs: List[dict[str, Any]]=default([
        {'impl': 'moving_avg', 'win_len': 14},
        {'impl': 'exp_avg', 'alpha': 0.3},
        {'impl': 'g_h', 'g': 0.5, 'h': 0.01},
        {'impl': 'kalman', 'proc_std': 50.0, 'meas_std': 2.0, 'guess_std': 10.0}
        ]) # Параметры для оценщика APY
    dfl_est_kwargs: List[dict[str, Any]]=default([
        {'impl': 'moving_avg', 'win_len': 14},
        {'impl': 'exp_avg', 'alpha': 0.3},
        {'impl': 'g_h', 'g': 0.5, 'h': 0.01},
        {'impl': 'kalman', 'proc_std': 50.0, 'meas_std': 2.0, 'guess_std': 10.0}
        ]) # Параметры для оценщика инфляции
    
    # Размах случайной компоненты. Случайная величина будет из диапазона X * [1 - rnd_mag/2; 1 + rnd_mag/2]
    rand_mag: List[float]=default([0.3])

parameters = Parameters().__dict__