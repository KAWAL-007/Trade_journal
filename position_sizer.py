import numpy as np

def fixed_fractional(account_size, risk_pct, entry, stop):
    risk_amount = account_size * (risk_pct / 100)
    risk_per_unit = abs(entry - stop)
    if risk_per_unit <= 0:
        return 0
    return int(risk_amount // risk_per_unit)


def atr_based(account_size, risk_pct, atr, atr_multiplier=1.5):
    risk_amount = account_size * (risk_pct / 100)
    stop_distance = atr * atr_multiplier
    if stop_distance <= 0:
        return 0
    return int(risk_amount // stop_distance)

def kelly_criterion(win_rate, win_loss_ratio, account_size):
    try:
        kelly_pct = win_rate - ((1 - win_rate) / win_loss_ratio)
        kelly_pct = max(0, min(kelly_pct, 0.25))  # cap at 25%
        return account_size * kelly_pct
    except Exception:
        return 0


def risk_warning(risk_pct):
    if risk_pct > 2:
        return "⚠️ Risk above recommended 2%"
    return "✅ Risk within safe limits"
