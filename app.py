# Run command:
# python -m streamlit run Python\Trade_dashboard\app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from database import init_db, add_trade, get_trades, add_backtest, get_backtests
from position_sizer import fixed_fractional, atr_based, kelly_criterion, risk_warning
from local_ai import trading_ai

# ---------------- INIT ----------------
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

st.title("📈 Trading Dashboard")

tabs = st.tabs([
    "📊 Dashboard",
    "📐 Position Sizer",
    "📒 Trade Journal",
    "🧪 Backtests"
])

# ---------------- DASHBOARD ----------------
with tabs[0]:
    st.subheader("Portfolio Overview")

    trades = get_trades()

    if not trades.empty:
        total_pnl = trades["pnl"].sum()
        win_rate = (trades["pnl"] > 0).mean() * 100
        open_positions = trades[trades["status"] == "Open"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total P&L", f"₹{total_pnl:.2f}")
        col2.metric("Win Rate", f"{win_rate:.2f}%")
        col3.metric("Open Trades", len(open_positions))

        fig = px.line(
            trades,
            x=trades.index,
            y="pnl",
            title="Trade P&L Curve",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trades available yet.")

    # -------- AI SECTION --------
    st.divider()
    st.subheader("🤖 AI Trading Performance Advisor (Local)")

    if st.button("Analyze My Trading Performance"):
        with st.spinner("AI analyzing your trades..."):
            advice = trading_ai(trades)

        st.success("Analysis Complete")
        st.text(advice)

# ---------------- POSITION SIZER ----------------
with tabs[1]:
    st.subheader("Position Sizing Calculator")

    account_size = st.number_input(
        "Account Size (₹)",
        min_value=1000,
        step=1000,
        value=100000
    )

    risk_pct = st.number_input(
        "Risk % per Trade",
        min_value=0.1,
        max_value=5.0,
        step=0.1,
        value=1.0
    )

    st.write(risk_warning(risk_pct))

    col1, col2 = st.columns(2)
    entry = col1.number_input("Entry Price", min_value=0.0, value=100.0)
    stop = col2.number_input("Stop Loss", min_value=0.0, value=95.0)

    atr = st.number_input("ATR (Volatility)", min_value=0.1, value=2.0)

    win_rate_kelly = st.number_input(
        "Win Rate (Kelly)",
        min_value=0.1,
        max_value=0.9,
        step=0.05,
        value=0.5
    )

    wlr = st.number_input(
        "Win/Loss Ratio",
        min_value=0.5,
        step=0.1,
        value=1.5
    )

    st.markdown("### 📌 Results")

    st.write(
        "Fixed Fractional Quantity:",
        int(fixed_fractional(account_size, risk_pct, entry, stop))
    )

    st.write(
        "ATR Based Quantity:",
        int(atr_based(account_size, risk_pct, atr))
    )

    st.write(
        "Kelly Capital Allocation (₹):",
        int(kelly_criterion(win_rate_kelly, wlr, account_size))
    )

# ---------------- TRADE JOURNAL ----------------
with tabs[2]:
    st.subheader("Trade Journal")

    with st.form("trade_form"):
        symbol = st.text_input("Symbol (e.g. NIFTY, BTC)")
        entry = st.number_input("Entry Price", min_value=0.0)
        exit_price = st.number_input(
            "Exit Price (0 if open)",
            min_value=0.0,
            value=0.0
        )
        qty = st.number_input("Quantity", min_value=1, step=1)
        date = st.date_input("Date", datetime.today())

        submit = st.form_submit_button("Add Trade")

        if submit:
            add_trade(
                symbol,
                entry,
                exit_price if exit_price > 0 else None,
                qty,
                str(date)
            )
            st.success("Trade added successfully")

    trades = get_trades()

    if not trades.empty:
        status_filter = st.selectbox(
            "Filter Trades",
            ["All", "Open", "Closed"]
        )

        if status_filter != "All":
            trades = trades[trades["status"] == status_filter]

        st.dataframe(trades, use_container_width=True)

# ---------------- BACKTEST MANAGER ----------------
with tabs[3]:
    st.subheader("Backtest Manager")

    with st.form("backtest_form"):
        strategy = st.text_input("Strategy Name")

        win_rate_bt = st.number_input(
            "Win Rate",
            min_value=0.1,
            max_value=0.9,
            step=0.05,
            value=0.55
        )

        total_pnl_bt = st.number_input(
            "Total P&L",
            step=100
        )

        trades_bt = st.number_input(
            "Number of Trades",
            min_value=1,
            step=1
        )

        submit_bt = st.form_submit_button("Save Backtest")

        if submit_bt:
            add_backtest(
                strategy,
                win_rate_bt,
                total_pnl_bt,
                int(trades_bt)
            )
            st.success("Backtest saved")

    bt = get_backtests()

    if not bt.empty:
        fig = px.bar(
            bt,
            x="strategy",
            y="total_pnl",
            title="Strategy Performance"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(bt, use_container_width=True)