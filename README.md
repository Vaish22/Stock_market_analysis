# 📈 Market Analysis Terminal

A real-time stock market analysis dashboard with time-series technical indicators, built with **Streamlit**, **Plotly**, and **yfinance**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Real-time market data** via yfinance (with simulated GBM fallback)
- **Candlestick charts** with interactive zoom, pan, and hover
- **9 Technical Indicators**: SMA, EMA, Bollinger Bands, VWAP, RSI, MACD, Volume
- **8 Pre-loaded tickers**: AAPL, MSFT, NVDA, GOOGL, AMZN, TSLA, META, JPM
- **Multiple timeframes**: 1W, 1M, 3M, 6M, 1Y, 2Y
- **Period statistics**: Return, Volatility, Sharpe Ratio, Max Drawdown
- **Dark terminal-style UI** with custom theming
- **Auto-refresh** toggle for live monitoring

## Quick Start (Local)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/stock-market-analysis.git
cd stock-market-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deploy to Streamlit Community Cloud (Free)

### Step 1 — Push to GitHub

```bash
cd stock-market-analysis

# Initialize git repo
git init
git add .
git commit -m "Initial commit: stock market analysis terminal"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/stock-market-analysis.git
git branch -M main
git push -u origin main
```

### Step 2 — Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub** account
3. Click **"New app"**
4. Fill in:
   - **Repository**: `YOUR_USERNAME/stock-market-analysis`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

Your app will be live at:
```
https://YOUR_USERNAME-stock-market-analysis.streamlit.app
```

### Step 3 — Done!

Every time you push to `main`, Streamlit Cloud will automatically redeploy.

---

## Project Structure

```
stock-market-analysis/
├── .streamlit/
│   └── config.toml          # Streamlit theme & server config
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## How It Works

| Component           | Technology                    |
|----------------------|-------------------------------|
| Frontend / UI        | Streamlit + Custom CSS        |
| Charts               | Plotly (candlestick, subplots)|
| Market Data          | yfinance API                  |
| Fallback Data        | Geometric Brownian Motion     |
| Technical Indicators | NumPy / Pandas (custom)       |

### Technical Indicators Explained

| Indicator        | Description                                                    |
|------------------|----------------------------------------------------------------|
| SMA (20, 50)     | Simple Moving Average — trend direction                        |
| EMA (12, 26)     | Exponential Moving Average — weighted recent prices            |
| Bollinger Bands  | Volatility envelope (±2σ around 20-period SMA)                 |
| VWAP             | Volume-Weighted Average Price — institutional benchmark        |
| RSI (14)         | Relative Strength Index — momentum (>70 overbought, <30 sold) |
| MACD (12,26,9)   | Moving Average Convergence/Divergence — trend + momentum       |

## Customization

### Add more tickers

Edit the `TICKERS` dict in `app.py`:

```python
TICKERS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft",
    # Add your own:
    "AMD": "Advanced Micro Devices",
    "NFLX": "Netflix Inc.",
}
```

### Add API keys (optional)

If you want to use premium data providers, create `.streamlit/secrets.toml`:

```toml
[api]
alpha_vantage_key = "YOUR_KEY_HERE"
polygon_key = "YOUR_KEY_HERE"
```

Access in code via `st.secrets["api"]["alpha_vantage_key"]`.

---

## License

MIT — free for personal and commercial use.
