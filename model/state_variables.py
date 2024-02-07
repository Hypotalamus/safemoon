from radcad.types import StateVariables


initial_state: StateVariables = {
    'holding_SFMs': 0.0, # Количество токенов, хранящихся у пользователей
    'APY': 0.0, # Текущее APY
    'raw_APY': 0.0, # Неотфильтрованное значение APY
    'raw_price': 0.0, # Текущая рыночная цена SFM
    'price_est': 0.0, # Оценка текущей цены SFM (отфильтрованная)
    'deflation': 0.0, # Текущее изменение цены ( инфляция / дефляция )
}