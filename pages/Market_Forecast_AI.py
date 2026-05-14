
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from datetime import datetime, timedelta

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Market Forecast AI",
    layout="wide"
)

# =========================================
# SIDEBAR STOCK SELECTION
# =========================================

stock_list = [
    "AAPL", "MSFT", "TSLA", "AMZN",
    "GOOGL", "META", "NVDA",
    "AMD", "NFLX", "INTC",
    "IBM", "ORCL", "QCOM",
    "RELIANCE.NS", "TCS.NS",
    "INFY.NS", "HDFCBANK.NS"
]

ticker = st.sidebar.selectbox(
    "📊 Select Stock",
    stock_list
)

# =========================================
# SIDEBAR AI STATUS
# =========================================

st.sidebar.markdown("---")

st.sidebar.subheader("🧠 Live AI Engine")

training_status = st.sidebar.empty()

training_status.info(
    "⚡ Initializing LSTM Model..."
)

# =========================================
# TITLE SECTION
# =========================================

st.markdown(f"""
<h1 style="
    font-size:42px;
    margin-bottom:0px;
">
📈 Market Forecast AI
</h1>

<p style="
    color:#9ca3af;
    font-size:18px;
    margin-top:0px;
">
Live AI-powered stock forecasting and market trend intelligence
</p>

<h3 style="
    color:#60a5fa;
    margin-top:25px;
">
Currently Analyzing: {ticker}
</h3>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================================
# DOWNLOAD LIVE DATA
# =========================================

data = yf.download(
    ticker,
    period="1y",
    progress=False
)

# Fix Multi-index issue
try:
    data.columns = data.columns.get_level_values(0)
except:
    pass

# =========================================
# VALIDATION
# =========================================

if data.empty:

    st.error(
        "⚠️ Unable to fetch live stock data."
    )

    st.stop()

# =========================================
# CLOSE PRICE DATA
# =========================================

close_data = data[['Close']]

close_value = close_data.iloc[-1]

# Handle Series issue
if hasattr(close_value, "__iter__"):
    latest_price = float(close_value.iloc[0])
else:
    latest_price = float(close_value)

# =========================================
# DATE INFO
# =========================================

latest_trading_date = data.index[-1].date()

today = datetime.now().date()

forecast_date = today + timedelta(days=1)

# =========================================
# DATA SCALING
# =========================================

scaler = MinMaxScaler(feature_range=(0, 1))

scaled_data = scaler.fit_transform(close_data)

# =========================================
# CREATE LSTM SEQUENCES
# =========================================

sequence_length = 60

X = []
y = []

for i in range(sequence_length, len(scaled_data)):

    X.append(
        scaled_data[i-sequence_length:i, 0]
    )

    y.append(
        scaled_data[i, 0]
    )

X = np.array(X)
y = np.array(y)

# =========================================
# RESHAPE FOR LSTM
# =========================================

X = np.reshape(
    X,
    (X.shape[0], X.shape[1], 1)
)

# =========================================
# BUILD LSTM MODEL
# =========================================

model = Sequential()

model.add(
    LSTM(
        units=50,
        return_sequences=True,
        input_shape=(X.shape[1], 1)
    )
)

model.add(
    LSTM(units=50)
)

model.add(
    Dense(units=1)
)

# =========================================
# COMPILE MODEL
# =========================================

model.compile(
    optimizer='adam',
    loss='mean_squared_error'
)

# =========================================
# TRAIN MODEL
# =========================================

training_status.warning(
    "⚡ Training LSTM Model..."
)

with st.spinner("Training Deep Learning Forecast Model..."):

    model.fit(
        X,
        y,
        epochs=10,
        batch_size=32,
        verbose=0
    )

training_status.success(
    "✅ Live LSTM Model Ready"
)

st.sidebar.success(
    "📡 Live Forecast Active"
)

st.sidebar.caption(
    "AI engine is generating tomorrow market forecast."
)

# =========================================
# TOMORROW FORECAST
# =========================================

last_60_days = scaled_data[-60:]

future_input = np.array(last_60_days)

future_input = np.reshape(
    future_input,
    (1, 60, 1)
)

predicted_price = model.predict(
    future_input,
    verbose=0
)

predicted_price = scaler.inverse_transform(
    predicted_price
)

tomorrow_prediction = float(
    predicted_price[0][0]
)

# =========================================
# CHANGE %
# =========================================

change = tomorrow_prediction - latest_price

percent = (change / latest_price) * 100

# =========================================
# MARKET INFO
# =========================================

st.info(f"""
📅 Latest Trading Session: {latest_trading_date}

🔮 Forecast Target Date: {forecast_date}
""")

# =========================================
# SIMPLE METRICS
# =========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Current Price",
        value=f"${latest_price:.2f}"
    )

with col2:
    st.metric(
        label="🔮 Predicted Tomorrow Price",
        value=f"${tomorrow_prediction:.2f}"
    )

with col3:
    st.metric(
        label="📈 Expected Change",
        value=f"{percent:.2f}%"
    )



# =========================================
# AI INSIGHT
# =========================================

st.markdown("---")

if percent > 0:

    st.success("""
    🟢 LSTM AI predicts bullish momentum for the next trading session.

    Market trend indicates possible upward continuation.
    """)

else:

    st.error("""
    🔴 LSTM AI predicts bearish momentum for the next trading session.

    Market trend indicates possible downside pressure.
    """)

# =========================================
# FORECAST GRAPH
# =========================================

st.subheader(
    f"📊 {ticker} AI Forecast Chart"
)

fig = go.Figure()

# Historical Line
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=close_data['Close'].values.flatten(),
        mode='lines',
        name='Historical Price'
    )
)

# Tomorrow Prediction Point
# =========================================
# CONNECT FORECAST LINE
# =========================================

forecast_x = [
    data.index[-1],
    forecast_date
]

forecast_y = [
    latest_price,
    tomorrow_prediction
]

fig.add_trace(
    go.Scatter(
        x=forecast_x,
        y=forecast_y,

        mode='lines+markers+text',

        line=dict(
            color='red',
            width=4,
            dash='dash'
        ),

        marker=dict(
            size=12,
            color='red'
        ),

        text=[
            "Current",
            "🔮 Forecast"
        ],

        textposition="top center",

        name='AI Forecast'
    )
)

fig.update_layout(

    template="plotly_dark",
    height=700,

    xaxis_title="Date",
    yaxis_title="Stock Price",

    title=f"{ticker} Deep Learning Forecast",

    xaxis_range=[
        data.index[-30],
        forecast_date + timedelta(days=2)
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)
