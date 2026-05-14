
import feedparser
import streamlit as st
import yfinance as yf
# ================= LIVE STOCK NEWS =================

st.markdown("""
<h1 style='margin-bottom:0px;'>
📰 Live Stock News Portal
</h1>

<p style='color:gray; font-size:18px;'>
Real-time financial headlines and market updates
</p>
""", unsafe_allow_html=True)
import datetime

st.info(
    f"🕒 News Updated: "
    f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.markdown("---")

# Sidebar stock selection
stock_list = [
    "AAPL", "MSFT", "TSLA", "AMZN",
    "GOOGL", "META", "NVDA", "NFLX"
]

ticker = st.sidebar.selectbox(
    "📈 Select Stock",
    stock_list
)

# Page title
st.subheader(f"📊 {ticker} Financial Headlines")

# Google RSS Feed
feed_url = f"https://news.google.com/rss/search?q={ticker}+stock"

news_feed = feedparser.parse(feed_url)

# ================= SHOW NEWS =================

if news_feed.entries:

    for entry in news_feed.entries[:10]:

        with st.container(border=True):

            st.markdown(f"""
            ### 📰 {entry.title}
            """)

            st.caption(entry.published)

            st.link_button(
                "🔗 Read Full Article",
                entry.link
            )

else:

    st.warning("⚠️ No live news available currently.")
if st.button("🔄 Refresh News"):
    st.rerun()
