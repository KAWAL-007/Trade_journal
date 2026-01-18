import pandas as pd

def trading_ai(trades: pd.DataFrame) -> str:
    if trades.empty:
        return "No trades available to analyze."

    total_trades = len(trades)
    wins = trades[trades["pnl"] > 0]
    losses = trades[trades["pnl"] <= 0]

    win_rate = len(wins) / total_trades * 100
    avg_win = wins["pnl"].mean() if not wins.empty else 0
    avg_loss = losses["pnl"].mean() if not losses.empty else 0
    total_pnl = trades["pnl"].sum()

    advice = []

    advice.append(f"Total Trades: {total_trades}")
    advice.append(f"Win Rate: {win_rate:.2f}%")
    advice.append(f"Total P&L: ₹{total_pnl:.2f}")

    if win_rate < 40:
        advice.append("❌ Low win rate. Consider improving trade selection.")
    elif win_rate > 60:
        advice.append("✅ Strong win rate. Strategy is working well.")

    if abs(avg_loss) > avg_win:
        advice.append("⚠ Losses are larger than wins. Improve risk management.")
    else:
        advice.append("✅ Risk-to-reward ratio looks healthy.")

    if total_pnl < 0:
        advice.append("📉 Overall performance is negative. Reduce position size.")
    else:
        advice.append("📈 You are profitable. Focus on consistency.")

    advice.append("\n📌 Recommendation:")
    advice.append("Stick to your setup, avoid overtrading, and review losing trades weekly.")

    return "\n".join(advice)