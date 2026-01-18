📈 Trading Dashboard with Local AI Advisor

A Python-based Trading Dashboard built using Streamlit, designed to help traders manage risk, track performance, and analyze trading strategies — all in one place.
The application includes a local AI-powered performance advisor that analyzes historical trades and provides actionable insights without using any external APIs or exposing secrets, making it completely offline and GitHub-safe.

🚀 Key Features
📊 Portfolio Dashboard

Real-time overview of total P&L, win rate, and open positions

Interactive P&L curve visualization using Plotly

📐 Position Sizing Calculator

Fixed Fractional Risk Management

ATR-based Volatility Position Sizing

Kelly Criterion Capital Allocation

Built-in risk warnings for overexposure

📒 Trade Journal

Store and manage trades using SQLite database

Automatic P&L calculation

Filter trades by open and closed positions

🧪 Backtest Manager

Save strategy backtest results

Compare strategy performance visually

Track win rate, total P&L, and trade count

🤖 Local AI Trading Advisor

Analyzes historical trade data

Evaluates win rate, risk-to-reward ratio, and profitability

Provides intelligent, rule-based trading recommendations

Works fully offline (no API keys, no internet dependency)

🛠 Tech Stack

Python

Streamlit – Web dashboard UI

SQLite – Lightweight database

Pandas – Data analysis

Plotly – Interactive visualizations

Custom Local AI Engine – Rule-based performance analysis

🔐 Security & Privacy

No API keys used

No external AI services

Safe to push directly to GitHub

Fully local and offline-first architecture
