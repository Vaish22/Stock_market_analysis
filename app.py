"""
Stock Market Analysis Terminal
Real-time time-series analysis with technical indicators.
Built with Streamlit · Plotly · NumPy · Pandas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf

# ══════════════════════════════════════════════════════════════════════════════
# Page Config
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Market Analysis Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# Custom CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global */
.stApp {
    background-color: #080a10;
    color: #e2e8f0;
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0c0e16;
    border-right: 1px solid #1a1f2e;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown label,
section[data-testid="stSidebar"] label {
    color: #a0aec0 !important;
    font-family: 'DM Sans', sans-serif;
}

/* Headers */
h1, h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: #f7fafc !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(15,18,30,0.95), rgba(20,24,36,0.9));
    border: 1px solid #1a1f2e;
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] p {
    color: #5a6478 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    color: #f7fafc !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Buttons / pills */
.stRadio > div {
    flex-direction: row !important;
    gap: 4px;
}
div[data-baseweb="radio"] > label {
    background: rgba(15,18,30,0.8);
    border: 1px solid #1a1f2e;
    border-radius: 8px;
    padding: 6px 14px !important;
    color: #5a6478;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
}

/* Multiselect */
.stMultiSelect [data-baseweb="tag"] {
    background-color: rgba(72,229,160,0.12) !important;
    border: 1px solid rgba(72,229,160,0.3);
    color: #48e5a0 !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: #0c0e16;
    border-radius: 8px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #5a6478;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    border-radius: 6px;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background-color: #1a2840 !important;
    color: #7cb9e8 !important;
    border: 1px solid #2d5a8a;
}

/* Divider */
hr { border-color: #1a1f2e !important; }

/* Hide streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Live dot animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #48e5a0;
    box-shadow: 0 0 8px #48e5a0;
    animation: pulse 2s ease infinite;
    margin-right: 8px;
    vertical-align: middle;
}
.live-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #48e5a0;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.footer-note {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #2a2f3e;
    margin-top: 32px;
    padding-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Data Fetching (with fallback to simulated data)
# ══════════════════════════════════════════════════════════════════════════════
TICKERS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA Corp",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com",
    "TSLA": "Tesla Inc.",
    "META": "Meta Platforms",
    "JPM": "JPMorgan Chase",
}

FALLBACK_PARAMS = {
    "AAPL": {"base": 218.5, "vol": 0.018, "drift": 0.0003},
    "MSFT": {"base": 442.8, "vol": 0.016, "drift": 0.0002},
    "NVDA": {"base": 137.2, "vol": 0.032, "drift": 0.0005},
    "GOOGL": {"base": 178.6, "vol": 0.020, "drift": 0.0002},
    "AMZN": {"base": 205.3, "vol": 0.022, "drift": 0.0003},
    "TSLA": {"base": 352.8, "vol": 0.038, "drift": 0.0001},
    "META": {"base": 612.4, "vol": 0.025, "drift": 0.0004},
    "JPM": {"base": 252.1, "vol": 0.014, "drift": 0.0002},
}


def generate_simulated_data(ticker: str, days: int = 400) -> pd.DataFrame:
    """Geometric Brownian Motion fallback when yfinance is unavailable."""
    params = FALLBACK_PARAMS.get(ticker, {"base": 100, "vol": 0.02, "drift": 0.0002})
    np.random.seed(hash(ticker) % 2**31)
    price = params["base"]
    records = []
    for i in range(days):
        date = datetime.now() - timedelta(days=days - i)
        rand = np.random.randn()
        open_price = price
        intra_vol = params["vol"] * 0.6
        high = open_price * (1 + abs(np.random.randn()) * intra_vol)
        low = open_price * (1 - abs(np.random.randn()) * intra_vol)
        price = price * np.exp(
            (params["drift"] - 0.5 * params["vol"] ** 2) + params["vol"] * rand
        )
        close = max(low, min(high, price))
        volume = int((800_000 + np.random.random() * 1_200_000) * (1 + abs(rand) * 0.5))
        records.append({
            "Date": date,
            "Open": round(open_price, 2),
            "High": round(max(open_price, close, high), 2),
            "Low": round(min(open_price, close, low), 2),
            "Close": round(close, 2),
            "Volume": volume,
        })
        price = close
    return pd.DataFrame(records).set_index("Date")


@st.cache_data(ttl=300, show_spinner=False)
def fetch_stock_data(ticker: str, period: str = "2y") -> tuple[pd.DataFrame, bool]:
    """Try yfinance first, fall back to simulated data."""
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty:
            raise ValueError("Empty dataframe")
        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
        return df, True
    except Exception:
        return generate_simulated_data(ticker), False


# ══════════════════════════════════════════════════════════════════════════════
# Technical Indicators
# ══════════════════════════════════════════════════════════════════════════════
def calc_sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(window=period).mean()


def calc_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calc_macd(series: pd.Series):
    ema12 = calc_ema(series, 12)
    ema26 = calc_ema(series, 26)
    macd_line = ema12 - ema26
    signal_line = calc_ema(macd_line, 9)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calc_bollinger(series: pd.Series, period: int = 20, mult: float = 2.0):
    middle = calc_sma(series, period)
    std = series.rolling(window=period).std()
    upper = middle + mult * std
    lower = middle - mult * std
    return upper, middle, lower


def calc_vwap(df: pd.DataFrame) -> pd.Series:
    tp = (df["High"] + df["Low"] + df["Close"]) / 3
    cum_tp_vol = (tp * df["Volume"]).cumsum()
    cum_vol = df["Volume"].cumsum()
    return cum_tp_vol / cum_vol


# ══════════════════════════════════════════════════════════════════════════════
# Chart Builder
# ══════════════════════════════════════════════════════════════════════════════
COLORS = {
    "bg": "#080a10",
    "card": "#0c0e16",
    "grid": "#141820",
    "border": "#1a1f2e",
    "text_dim": "#3e4555",
    "text_mid": "#5a6478",
    "text": "#a0aec0",
    "text_bright": "#e2e8f0",
    "green": "#48e5a0",
    "red": "#f56565",
    "sma20": "#f6ad55",
    "sma50": "#ed64a6",
    "ema12": "#63b3ed",
    "ema26": "#b794f4",
    "vwap": "#fbd38d",
    "bb": "#5a6478",
    "macd": "#63b3ed",
    "signal": "#f6ad55",
}


def build_chart(df: pd.DataFrame, indicators: list[str]) -> go.Figure:
    show_rsi = "RSI" in indicators
    show_macd = "MACD" in indicators
    show_volume = "Volume" in indicators

    # Determine subplot layout
    rows = 1
    row_heights = [0.6]
    if show_volume:
        rows += 1
        row_heights.append(0.12)
    if show_rsi:
        rows += 1
        row_heights.append(0.14)
    if show_macd:
        rows += 1
        row_heights.append(0.14)

    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights,
    )

    current_row = 1

    # ── Candlestick ──────────────────────────────────────────────────────────
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        increasing_line_color=COLORS["green"], decreasing_line_color=COLORS["red"],
        increasing_fillcolor=COLORS["green"], decreasing_fillcolor=COLORS["red"],
        name="OHLC", whiskerwidth=0.4,
    ), row=current_row, col=1)

    # ── Moving Averages ──────────────────────────────────────────────────────
    if "SMA 20" in indicators:
        sma20 = calc_sma(df["Close"], 20)
        fig.add_trace(go.Scatter(
            x=df.index, y=sma20, mode="lines", name="SMA 20",
            line=dict(color=COLORS["sma20"], width=1.5),
        ), row=current_row, col=1)

    if "SMA 50" in indicators:
        sma50 = calc_sma(df["Close"], 50)
        fig.add_trace(go.Scatter(
            x=df.index, y=sma50, mode="lines", name="SMA 50",
            line=dict(color=COLORS["sma50"], width=1.5),
        ), row=current_row, col=1)

    if "EMA 12" in indicators:
        ema12 = calc_ema(df["Close"], 12)
        fig.add_trace(go.Scatter(
            x=df.index, y=ema12, mode="lines", name="EMA 12",
            line=dict(color=COLORS["ema12"], width=1.5),
        ), row=current_row, col=1)

    if "EMA 26" in indicators:
        ema26 = calc_ema(df["Close"], 26)
        fig.add_trace(go.Scatter(
            x=df.index, y=ema26, mode="lines", name="EMA 26",
            line=dict(color=COLORS["ema26"], width=1.5),
        ), row=current_row, col=1)

    # ── Bollinger Bands ──────────────────────────────────────────────────────
    if "Bollinger Bands" in indicators:
        bb_upper, bb_middle, bb_lower = calc_bollinger(df["Close"])
        fig.add_trace(go.Scatter(
            x=df.index, y=bb_upper, mode="lines", name="BB Upper",
            line=dict(color=COLORS["bb"], width=1, dash="dash"), showlegend=False,
        ), row=current_row, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=bb_lower, mode="lines", name="BB Lower",
            line=dict(color=COLORS["bb"], width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(90,100,120,0.06)", showlegend=False,
        ), row=current_row, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=bb_middle, mode="lines", name="Bollinger",
            line=dict(color=COLORS["bb"], width=1, dash="dot"),
        ), row=current_row, col=1)

    # ── VWAP ─────────────────────────────────────────────────────────────────
    if "VWAP" in indicators:
        vwap = calc_vwap(df)
        fig.add_trace(go.Scatter(
            x=df.index, y=vwap, mode="lines", name="VWAP",
            line=dict(color=COLORS["vwap"], width=1.5, dash="dashdot"),
        ), row=current_row, col=1)

    # ── Volume ───────────────────────────────────────────────────────────────
    if show_volume:
        current_row += 1
        colors = [COLORS["green"] if c >= o else COLORS["red"] for c, o in zip(df["Close"], df["Open"])]
        fig.add_trace(go.Bar(
            x=df.index, y=df["Volume"], name="Volume",
            marker_color=colors, opacity=0.4,
        ), row=current_row, col=1)
        fig.update_yaxes(title_text="Vol", row=current_row, col=1,
                         title_font=dict(size=10, color=COLORS["text_dim"]))

    # ── RSI ──────────────────────────────────────────────────────────────────
    if show_rsi:
        current_row += 1
        rsi = calc_rsi(df["Close"])
        fig.add_trace(go.Scatter(
            x=df.index, y=rsi, mode="lines", name="RSI (14)",
            line=dict(color=COLORS["ema26"], width=1.5),
            fill="tozeroy", fillcolor="rgba(183,148,244,0.06)",
        ), row=current_row, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="rgba(245,101,101,0.3)",
                      row=current_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="rgba(72,229,160,0.3)",
                      row=current_row, col=1)
        fig.update_yaxes(range=[0, 100], title_text="RSI", row=current_row, col=1,
                         title_font=dict(size=10, color=COLORS["text_dim"]))

    # ── MACD ─────────────────────────────────────────────────────────────────
    if show_macd:
        current_row += 1
        macd_line, signal_line, histogram = calc_macd(df["Close"])
        hist_colors = [COLORS["green"] if v >= 0 else COLORS["red"] for v in histogram]
        fig.add_trace(go.Bar(
            x=df.index, y=histogram, name="Histogram",
            marker_color=hist_colors, opacity=0.35,
        ), row=current_row, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=macd_line, mode="lines", name="MACD",
            line=dict(color=COLORS["macd"], width=1.5),
        ), row=current_row, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=signal_line, mode="lines", name="Signal",
            line=dict(color=COLORS["signal"], width=1.5),
        ), row=current_row, col=1)
        fig.add_hline(y=0, line_color=COLORS["border"], row=current_row, col=1)
        fig.update_yaxes(title_text="MACD", row=current_row, col=1,
                         title_font=dict(size=10, color=COLORS["text_dim"]))

    # ── Layout ───────────────────────────────────────────────────────────────
    fig.update_layout(
        height=220 + rows * 180,
        plot_bgcolor=COLORS["card"],
        paper_bgcolor=COLORS["bg"],
        font=dict(family="JetBrains Mono, monospace", color=COLORS["text_mid"], size=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=10, color=COLORS["text"]),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=60, r=20, t=40, b=20),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
    )

    # Style all axes
    for i in range(1, rows + 1):
        fig.update_xaxes(
            gridcolor=COLORS["grid"], showgrid=True, zeroline=False,
            linecolor=COLORS["border"], tickfont=dict(size=9),
            row=i, col=1,
        )
        fig.update_yaxes(
            gridcolor=COLORS["grid"], showgrid=True, zeroline=False,
            linecolor=COLORS["border"], tickfont=dict(size=9),
            row=i, col=1,
        )

    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Sidebar Controls
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.markdown("---")

    ticker = st.selectbox(
        "**Ticker**",
        options=list(TICKERS.keys()),
        format_func=lambda t: f"{t}  —  {TICKERS[t]}",
        index=2,  # Default: NVDA
    )

    st.markdown("")
    timeframe = st.radio(
        "**Timeframe**",
        options=["1W", "1M", "3M", "6M", "1Y", "2Y"],
        index=3,
        horizontal=True,
    )

    st.markdown("")
    indicators = st.multiselect(
        "**Technical Indicators**",
        options=["SMA 20", "SMA 50", "EMA 12", "EMA 26",
                 "Bollinger Bands", "VWAP", "Volume", "RSI", "MACD"],
        default=["SMA 20", "SMA 50", "Volume"],
    )

    st.markdown("")
    auto_refresh = st.toggle("Auto-refresh (5 min)", value=False)
    if auto_refresh:
        st.markdown(
            '<p style="font-size:10px;color:#3e4555;">Page will re-fetch data every 5 minutes.</p>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        '<p style="font-size:10px;color:#2a2f3e;text-align:center;">'
        'Market Analysis Terminal v1.0<br>Not financial advice.</p>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Main Content
# ══════════════════════════════════════════════════════════════════════════════

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(
        '<span class="live-dot"></span>'
        '<span class="live-label">Live Feed</span>',
        unsafe_allow_html=True,
    )
    st.markdown("# Market Analysis Terminal")
with col_h2:
    st.markdown(
        f'<p style="text-align:right;font-family:JetBrains Mono,monospace;'
        f'font-size:11px;color:#5a6478;margin-top:28px;">'
        f'{datetime.now().strftime("%b %d, %Y · %H:%M:%S")}</p>',
        unsafe_allow_html=True,
    )

# Fetch data
with st.spinner("Fetching market data..."):
    raw_df, is_live = fetch_stock_data(ticker)

# Filter by timeframe
tf_map = {"1W": 5, "1M": 21, "3M": 63, "6M": 126, "1Y": 252, "2Y": 504}
n_days = tf_map.get(timeframe, 126)
df = raw_df.tail(n_days).copy()

if df.empty:
    st.error("No data available for this ticker/timeframe.")
    st.stop()

# Data source badge
source = "yfinance · Real Market Data" if is_live else "Simulated · Geometric Brownian Motion"
badge_color = "#48e5a0" if is_live else "#f6ad55"
st.markdown(
    f'<p style="font-family:JetBrains Mono,monospace;font-size:10px;'
    f'color:{badge_color};letter-spacing:1.5px;text-transform:uppercase;'
    f'margin-bottom:4px;">Source: {source}</p>',
    unsafe_allow_html=True,
)

# ── Metrics Row ──────────────────────────────────────────────────────────────
latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest
change = latest["Close"] - prev["Close"]
change_pct = (change / prev["Close"]) * 100

high_52w = raw_df.tail(252)["High"].max()
low_52w = raw_df.tail(252)["Low"].min()
avg_vol_30 = int(raw_df.tail(30)["Volume"].mean())
rsi_val = calc_rsi(df["Close"]).iloc[-1]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(
    f"{ticker} — {TICKERS[ticker]}",
    f"${latest['Close']:.2f}",
    f"{change:+.2f}  ({change_pct:+.2f}%)",
    delta_color="normal",
)
c2.metric("52-Week High", f"${high_52w:.2f}")
c3.metric("52-Week Low", f"${low_52w:.2f}")
c4.metric("Avg Vol (30d)", f"{avg_vol_30:,.0f}")
rsi_label = "Overbought" if rsi_val > 70 else ("Oversold" if rsi_val < 30 else "Neutral")
c5.metric("RSI (14)", f"{rsi_val:.1f}", rsi_label)

st.markdown("")

# ── Chart ────────────────────────────────────────────────────────────────────
fig = build_chart(df, indicators)
st.plotly_chart(fig, use_container_width=True, config={
    "displayModeBar": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "displaylogo": False,
})

# ── Data Table (Expandable) ──────────────────────────────────────────────────
with st.expander("📊 View Raw Data"):
    display_df = df.copy()
    display_df.index = display_df.index.strftime("%Y-%m-%d") if hasattr(display_df.index, "strftime") else display_df.index
    display_df["Volume"] = display_df["Volume"].apply(lambda x: f"{x:,.0f}")
    for col in ["Open", "High", "Low", "Close"]:
        display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")
    st.dataframe(display_df.tail(50).iloc[::-1], use_container_width=True)

# ── Summary Statistics ───────────────────────────────────────────────────────
with st.expander("📈 Period Statistics"):
    sc1, sc2, sc3, sc4 = st.columns(4)
    period_return = ((df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1) * 100
    daily_returns = df["Close"].pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252) * 100
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() > 0 else 0
    max_dd = ((df["Close"] / df["Close"].cummax()) - 1).min() * 100

    sc1.metric("Period Return", f"{period_return:+.2f}%")
    sc2.metric("Annualized Vol", f"{volatility:.1f}%")
    sc3.metric("Sharpe Ratio", f"{sharpe:.2f}")
    sc4.metric("Max Drawdown", f"{max_dd:.1f}%")

# Footer
st.markdown(
    '<p class="footer-note">'
    'Built with Streamlit · Plotly · yfinance · Pandas<br>'
    'Technical indicators computed in real-time · Not financial advice'
    '</p>',
    unsafe_allow_html=True,
)

# Auto-refresh mechanism
if auto_refresh:
    import time
    time.sleep(300)
    st.rerun()
