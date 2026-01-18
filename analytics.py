import pandas as pd

def performance_metrics(trades: pd.DataFrame):
    if trades.empty:
        return {}

    closed = trades[trades["status"] == "Closed"]

    wins = closed[closed["pnl"] > 0]
    losses = closed[closed["pnl"] < 0]

    gross_profit = wins["pnl"].sum()
    gross_loss = abs(losses["pnl"].sum())

    equity = closed["pnl"].cumsum()
    drawdown = equity - equity.cummax()
    max_dd = drawdown.min()

    return {
        "Total Trades": len(closed),
        "Win Rate %": round((len(wins) / len(closed)) * 100, 2) if len(closed) else 0,
        "Profit Factor": round(gross_profit / gross_loss, 2) if gross_loss != 0 else "∞",
        "Max Drawdown": round(max_dd, 2),
        "Avg Win": round(wins["pnl"].mean(), 2) if not wins.empty else 0,
        "Avg Loss": round(losses["pnl"].mean(), 2) if not losses.empty else 0
    }
