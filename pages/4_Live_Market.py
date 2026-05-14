import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Live Market", layout="wide")

# Sidebar input
stock_list = [
    "AAPL", "MSFT", "TSLA", "AMZN", "GOOGL",
    "META", "NFLX", "NVDA", "AMD", "INTC",
    "IBM", "ORCL", "CRM", "UBER", "PYPL",
    "SHOP", "QCOM", "SONY", "TATAMOTORS.NS",
    "RELIANCE.NS", "INFY.NS", "TCS.NS",
    "WIPRO.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "BHARTIARTL.NS", "ADANIENT.NS",
    "MARUTI.NS", "ASIANPAINT.NS", "ITC.NS",
    "ZOMATO.NS", "BAJFINANCE.NS", "AXISBANK.NS"
]

ticker = st.sidebar.selectbox(
    "📈 Select Stock",
    stock_list,
    index=0
)



col1, col2 = st.columns([6, 1])

ticker_data = yf.Ticker(ticker)
try:
    info = ticker_data.info
except:
    info = {}

company_name = info.get("longName", ticker)
sector = info.get("sector", "N/A")

with col1:
    st.markdown(f"""
    <h2>📡 Live {company_name} ({ticker}) Stocks </h2>
    <p style="color:gray; font-size:14px;">
        Sector: {sector}
    </p>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🔄"):
        st.rerun()

st.info(f"⏱ Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")
st.markdown("---")
# Fetch data
data = yf.download(ticker, period="1mo", progress=False)

show_chart = st.sidebar.toggle("📊 Live Trend View")
if show_chart:
    st.sidebar.subheader("📉 Mini Chart")
    st.sidebar.line_chart(data['Close'])

# 🔥 FIX 1: Handle multi-index columns (IMPORTANT)
if isinstance(data.columns, type(data.columns)) and len(data.columns) > 0:
    try:
        data.columns = data.columns.get_level_values(0)
    except:
        pass

# 🔥 FIX 2: Check data
if data is None or data.empty:
    st.error("⚠️ Unable to fetch live data. Try AAPL / TSLA / MSFT")
    st.stop()

# 🔥 FIX 3: Safe value extraction
close_series = data["Close"]

# If still Series of Series → flatten
if hasattr(close_series.iloc[-1], "__iter__"):
    close_price = float(close_series.iloc[-1][0])
    prev_price  = float(close_series.iloc[-2][0]) if len(close_series) > 1 else close_price
else:
    close_price = float(close_series.iloc[-1])
    prev_price  = float(close_series.iloc[-2]) if len(close_series) > 1 else close_price

change = close_price - prev_price
percent = (change / prev_price) * 100

# Volume fix
vol_series = data["Volume"]
volume = int(vol_series.iloc[-1]) if not hasattr(vol_series.iloc[-1], "__iter__") else int(vol_series.iloc[-1][0])

# ---------------- UI ----------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Price", f"${close_price:.2f}", f"{percent:.2f}%")
col2.metric("📈 Change", f"${change:.2f}")
col3.metric("📊 Volume", f"{volume:,}")

st.divider()
tab1, tab2, tab3 , tab4, tab5 = st.tabs(["📊 Chart", "📉 Market Signal", "💡 Recommendation","📉 Advanced Analytics", "⚖️ Compare Stocks"])
with tab1:
    st.subheader(f"📊 {ticker} Chart")

    # 🔥 Moving Averages
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"]
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA20'],
        name='MA20',
        line=dict(color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA50'],
        name='MA50',
        line=dict(color='blue')
    ))

    fig.update_layout(template="plotly_dark", height=600)

    st.plotly_chart(fig, use_container_width=True)

# ================= MARKET SIGNAL =================

with tab2:
    st.subheader(f"📊 {ticker} Market Signal")

    signal = "BUY" if percent > 0 else "SELL"

    risk = "High" if abs(percent) > 2 else "Medium"

    trend = "Bullish 📈" if percent > 0 else "Bearish 📉"

    momentum = "Positive" if change > 0 else "Negative"

    # ================= MAIN SIGNAL =================

    # ================= MAIN SIGNAL =================

    if signal == "BUY":

        st.success("🟢 STRONG BUY")

        st.info("""
        📈 Market trend indicates bullish momentum.

        • Positive short-term movement detected  
        • Buyers currently dominating market  
        • Momentum strength increasing
        """)

    else:

        st.error("🔴 STRONG SELL")

        st.warning("""
        📉 Market trend indicates bearish pressure.

        • Negative short-term momentum detected  
        • Sellers currently dominating market  
        • Weak price movement observed
        """)

    st.divider()

    # ================= INSIGHTS =================

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"""
        📈 Trend Analysis

        • Current Trend: {trend}
        • Momentum: {momentum}
        • Daily Change: {percent:.2f}%
        """)

    with col2:

        st.warning(f"""
        ⚠ Risk Assessment

        • Risk Level: {risk}
        • Volatility Active
        • Monitor price fluctuations carefully
        """)

    st.divider()

    # ================= MOVING AVERAGE INSIGHT =================

    ma20 = data['MA20'].iloc[-1]
    current_price = data['Close'].iloc[-1]

    if current_price > ma20:

        st.success(f"""
        ✅ Price is trading ABOVE MA20

        This indicates bullish strength and upward momentum.
        """)

    else:

        st.error(f"""
        ❌ Price is trading BELOW MA20

        This may indicate bearish pressure and weakness.
        """)

with tab3:
    st.subheader("💡 Recommendation")

    # Momentum logic
    momentum = "positive" if percent > 0 else "negative"

    # Volume analysis
    avg_volume = data["Volume"].mean()

    latest_volume = (
        float(data["Volume"].iloc[-1][0])
        if hasattr(data["Volume"].iloc[-1], "__iter__")
        else float(data["Volume"].iloc[-1])
    )

    volume_status = (
        "increasing 📈"
        if latest_volume > avg_volume
        else "stable 📊"
    )

    # Risk logic
    volatility = data["Close"].pct_change().std() * 100

    if volatility > 3:
        risk = "High 🔴"
    elif volatility > 1.5:
        risk = "Medium 🟠"
    else:
        risk = "Low 🟢"

    # Recommendation card
    st.markdown(f"""
    <div style="
        background-color:#111827;
        padding:20px;
        border-radius:12px;
        border:1px solid #374151;
    ">

    <h3 style="color:#60A5FA;">
        📌 Trading Recommendation
    </h3>

    <p style="font-size:18px;">
        ✔ Good for short-term traders
    </p>

    <p style="font-size:18px;">
        ✔ Momentum is {momentum} {'📈' if momentum == 'positive' else '📉'}
    </p>

    <p style="font-size:18px;">
        ✔ Volume is {volume_status}
    </p>

    <p style="font-size:18px;">
        ⚠ Risk Level: {risk}
    </p>

    </div>
    """, unsafe_allow_html=True)

with tab4:

    st.subheader(f"📉 Advanced Analytics— {company_name}")

    st.markdown(f"""
    Analyze real-time technical indicators and market behavior of 
    **{company_name} ({ticker})** using volatility, returns,
    Bollinger Bands, and momentum indicators.
    """)

    st.divider()

    # ================= VOLATILITY =================

    st.markdown(f"""
    ### 📊  {ticker} Volatility Analysis

    This graph shows the volatility of {company_name} stock price.

    Higher volatility means the stock price is changing rapidly,
    indicating higher market risk and stronger price movement.
    """)

    data['Volatility'] = data['Close'].pct_change().rolling(5).std()

    st.line_chart(data['Volatility'])

    st.divider()

    # ================= RETURNS =================

    st.markdown(f"""
    ### 📈  {ticker} Daily Returns

    This graph represents daily percentage returns of the stock.

    Positive values indicate gains, while negative values show losses.
    It helps investors understand short-term stock performance trends.
    """)

    data['Returns'] = data['Close'].pct_change()

    st.area_chart(data['Returns'])

    st.divider()

    # ================= BOLLINGER =================

    st.markdown(f"""
    ### 📉  {ticker} Bollinger Bands

    Bollinger Bands help identify whether the stock is overbought
    or oversold based on price movement and volatility.

    - Upper Band → possible overbought zone
    - Lower Band → possible oversold zone
    """)

    data['Upper'] = data['MA20'] + (2 * data['Close'].rolling(20).std())
    data['Lower'] = data['MA20'] - (2 * data['Close'].rolling(20).std())

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        name='Close Price'
    ))

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data['Upper'],
        name='Upper Band'
    ))

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data['Lower'],
        name='Lower Band'
    ))

    fig2.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ================= MOMENTUM =================

    st.markdown(f"""
    ### 🚀  {ticker} Momentum Indicator

    Momentum analysis measures the speed of stock price movement.

    Positive momentum indicates bullish strength,
    while negative momentum may indicate bearish pressure.
    """)

    data['Momentum'] = data['Close'] - data['Close'].shift(5)

    st.bar_chart(data['Momentum'])

# ================= COMPARE STOCKS =================

with tab5:
    st.subheader("⚖️ Compare Stocks")

    st.markdown("""
    Compare multiple live stocks using:
    • Price trends
    • Returns
    • Volatility
    """)

    compare_stocks = st.multiselect(
        "Select Stocks",
        stock_list,
        default=["AAPL", "MSFT", "TSLA"]
    )

    if compare_stocks:
        # Fetch live data
        compare_data = yf.download(
            compare_stocks,
            period="1mo",
            progress=False
        )["Close"]

        # ================= PRICE GRAPH =================

        st.markdown("### 📈 Stock Price Comparison")

        st.markdown("""
        Compare live closing prices of selected companies.
        """)

        st.line_chart(compare_data)

        st.divider()

        # ================= RETURNS =================

        returns = compare_data.pct_change().mean() * 100

        st.markdown("### 📊 Average Returns")

        st.markdown("""
        Higher returns indicate better stock performance.
        """)

        st.bar_chart(returns)

        st.divider()

        # ================= VOLATILITY =================

        volatility = compare_data.pct_change().std() * 100

        st.markdown("### 📉 Volatility Comparison")

        st.markdown("""
        Higher volatility means higher market risk.
        """)

        st.bar_chart(volatility)

        st.divider()

        # ================= INSIGHTS =================

        best_stock = returns.idxmax()
        safest_stock = volatility.idxmin()

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"""
            📈 Best Performing Stock

            {best_stock}
            """)

        with col2:
            st.info(f"""
            🛡 Lowest Risk Stock

            {safest_stock}
            """)


