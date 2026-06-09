import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="An Investor Decision Support System for ITC Ltd",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------
# DATA FUNCTION
# -----------------------------------

@st.cache_data(ttl=300)
def get_stock_data():

    stock = yf.Ticker("ITC.NS")

    return {
        "info": stock.info,
        "history": stock.history(
            period="1y",
            auto_adjust=True
        )
    }

# -----------------------------------
# LOAD DATA
# -----------------------------------

try:

    data = get_stock_data()

    info = data["info"]
    hist = data["history"]

except Exception as e:

    st.error(f"Unable to load market data: {e}")
    st.stop()

# -----------------------------------
# VARIABLES
# -----------------------------------

company_name = info.get(
    "longName",
    "ITC Ltd"
)

current_price = info.get(
    "currentPrice",
    info.get("regularMarketPrice", 0)
)

market_cap = info.get(
    "marketCap",
    0
)

market_cap_cr = market_cap / 10000000

pe_ratio = info.get(
    "trailingPE",
    0
)

dividend_yield = info.get(
    "dividendYield",
    0
)

# -----------------------------------
# CSS
# -----------------------------------

st.markdown("""
<style>

.big-title {
    font-size: 48px;
    font-weight: 800;
    color: #0B2E75;
}

[data-testid="metric-container"] {
    border: 1px solid #D1D5DB;
    border-radius: 12px;
    padding: 15px;
    background-color: white;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
<div class="big-title">
📈 ITC Investor Insights Platform
</div>
""", unsafe_allow_html=True)

st.caption(
    "Comprehensive ITC stock analysis using live Yahoo Finance data"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.markdown("""
<h2 style='text-align:center;color:#0B2E75;'>
📈 ITC Analysis
</h2>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🏢 Company Analysis",
        "📈 Technical Analysis",
        "💰 Financial Analysis",
        "🤖 Recommendation",
        "⚔️ Peer Comparison"
    ]
)

# -----------------------------------
# HOME PAGE
# -----------------------------------

if page == "🏠 Home":

    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#0B2E75,#1565C0);
    padding:35px;
    border-radius:20px;
    color:white;
    ">
    <h1>ITC Limited Investment Dashboard</h1>

    <p>
    Comprehensive analysis of ITC Ltd covering
    fundamentals, valuation, technical indicators,
    financial strength and investment outlook.
    </p>

    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Price",
            f"₹{current_price:.2f}"
        )

    with col2:
        st.metric(
            "Market Cap",
            f"₹{market_cap_cr:,.0f} Cr"
        )

    with col3:
        st.metric(
            "PE Ratio",
            round(pe_ratio, 2)
        )

    with col4:
        st.metric(
            "Dividend Yield",
            f"{dividend_yield:.2f}%"
        )
    st.markdown("---")

    st.subheader("📈 ITC Stock Performance (1 Year)")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            name="ITC"
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=450,
        xaxis_title="Date",
        yaxis_title="Price (₹)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    st.markdown("---")
    st.subheader("🏢 About ITC Limited")

    summary = info.get(
        "longBusinessSummary",
        "Information unavailable."
    )

    st.write(summary[:1000])

# -----------------------------------
# COMPANY ANALYSIS
# -----------------------------------

elif page == "🏢 Company Analysis":

    st.header(company_name)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Price",
            f"₹{current_price:.2f}"
        )

    with col2:
        st.metric(
            "Market Cap",
            f"₹{market_cap_cr:,.0f} Cr"
        )

    with col3:
        st.metric(
            "PE Ratio",
            round(pe_ratio, 2)
        )

    with col4:
        st.metric(
            "Dividend Yield",
            f"{dividend_yield*100:.2f}%"
        )

    st.markdown("---")

    st.subheader("Company Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Sector:** {info.get('sector','N/A')}"
        )

        st.write(
            f"**Industry:** {info.get('industry','N/A')}"
        )

        st.write(
            f"**Country:** {info.get('country','N/A')}"
        )

    with col2:

        st.write(
            f"**52 Week High:** ₹{info.get('fiftyTwoWeekHigh','N/A')}"
        )

        st.write(
            f"**52 Week Low:** ₹{info.get('fiftyTwoWeekLow','N/A')}"
        )

        st.write(
            f"**Website:** {info.get('website','N/A')}"
        )

    st.markdown("---")

    st.subheader("Business Overview")

    summary = info.get(
        "longBusinessSummary",
        "Information unavailable."
    )

    st.write(summary)
    # -----------------------------------
# -----------------------------------
# TECHNICAL ANALYSIS
# -----------------------------------

elif page == "📈 Technical Analysis":

    st.header("📈 Technical Analysis")

    # Moving Average
    hist["30DMA"] = hist["Close"].rolling(30).mean()

    latest_price = float(
    hist["Close"]
    .dropna()
    .iloc[-1]
              )
    latest_dma = float(
        hist["30DMA"]
        .dropna()
        .iloc[-1]
    )

    volatility = (
        hist["Close"]
        .pct_change()
        .std()
        * (252 ** 0.5)
        * 100
    )

    # ==========================
    # KPI CARDS
    # ==========================

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Current Price",
            f"₹{latest_price:.2f}"
        )

    with col2:
        st.metric(
            "📊 30 Day MA",
            f"₹{latest_dma:.2f}"
        )

    with col3:
        st.metric(
            "⚡ Volatility",
            f"{volatility:.2f}%"
        )

    st.markdown("---")

    # ==========================
    # PRICE CHART
    # ==========================

    st.subheader("📊 Price vs 30-Day Moving Average")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            name="Stock Price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["30DMA"],
            mode="lines",
            name="30 DMA"
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ==========================
    # TREND ANALYSIS
    # ==========================

    st.subheader("📈 Trend Analysis")

    if latest_price > latest_dma:

        st.success(
            f"""
            Bullish Signal

            Current Price: ₹{latest_price:.2f}

            30 DMA: ₹{latest_dma:.2f}
            """
        )

    else:

        st.warning(
            f"""
            Bearish Signal

            Current Price: ₹{latest_price:.2f}

            30 DMA: ₹{latest_dma:.2f}
            """
        )

    st.subheader("📉 Volatility Analysis")

    st.metric(
        "Annual Volatility",
        f"{volatility:.2f}%"
    )

    if volatility < 20:
        st.success("Low Volatility")

    elif volatility < 35:
        st.warning("Moderate Volatility")

    else:
        st.error("High Volatility")
    st.markdown("---")

    st.subheader("📌 Moving Average Interpretation")

    if latest_price > latest_dma:

        st.success(
            f"""
    Current Price: ₹{latest_price:.2f}

    30 DMA: ₹{latest_dma:.2f}

    Bullish Signal:
    Price is trading above its 30-day moving average,
    indicating positive momentum.
    """
        )

    else:

        st.warning(
            f"""
    Current Price: ₹{latest_price:.2f}

    30 DMA: ₹{latest_dma:.2f}

    Bearish Signal:
    Price is trading below its 30-day moving average,
    indicating weaker short-term momentum.
    """
        )

# -----------------------------------
# FINANCIAL ANALYSIS
# -----------------------------------

elif page == "💰 Financial Analysis":

    st.header("💰 Financial Analysis")

    roe = info.get(
        "returnOnEquity",
        "N/A"
    )

    eps = info.get(
        "trailingEps",
        "N/A"
    )

    debt_equity = info.get(
        "debtToEquity",
        "N/A"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if roe != "N/A":

            st.metric(
                "ROE",
                f"{roe*100:.2f}%"
            )

        else:

            st.metric(
                "ROE",
                "N/A"
            )

    with col2:

        st.metric(
            "EPS",
            eps
        )

    with col3:

        st.metric(
            "Debt / Equity",
            debt_equity
        )

    st.markdown("---")

    score = 0

    if pe_ratio:

        if pe_ratio < 20:
            score += 20

        elif pe_ratio < 30:
            score += 15

        else:
            score += 5

    if dividend_yield:

        dy = dividend_yield * 100

        if dy > 4:
            score += 20

        elif dy > 2:
            score += 15

        else:
            score += 5

    hist["30DMA"] = (
        hist["Close"]
        .rolling(30)
        .mean()
    )

    latest_price = hist["Close"].iloc[-1]
    latest_dma = hist["30DMA"].iloc[-1]

    if latest_price > latest_dma:
        score += 20

    else:
        score += 10

    if market_cap_cr > 100000:
        score += 20

    else:
        score += 10

    one_year_return = round(
        (
            (
                hist["Close"].iloc[-1]
                /
                hist["Close"].iloc[0]
            ) - 1
        ) * 100,
        2
    )

    if one_year_return > 20:
        score += 20

    elif one_year_return > 0:
        score += 10

    score = min(score, 100)

    st.metric(
        "Financial Health Score",
        f"{score}/100"
    )
    st.subheader("📌 Financial Interpretation")

    if roe != "N/A" and roe > 0.15:
     st.success("Strong Return on Equity indicates efficient use of shareholder capital.")

# -----------------------------------
# RECOMMENDATION
# -----------------------------------

elif page == "🤖 Recommendation":

    st.header(
        "🤖 Investment Recommendation"
    )

    score = 0

    if pe_ratio:

        if pe_ratio < 20:
            score += 20

        elif pe_ratio < 30:
            score += 15

        else:
            score += 5

    if dividend_yield:

        dy = dividend_yield * 100

        if dy > 4:
            score += 20

        elif dy > 2:
            score += 15

        else:
            score += 5

    hist["30DMA"] = (
        hist["Close"]
        .rolling(30)
        .mean()
    )

    latest_price = hist["Close"].iloc[-1]
    latest_dma = hist["30DMA"].iloc[-1]

    if latest_price > latest_dma:
        score += 20

    else:
        score += 10

    if market_cap_cr > 100000:
        score += 20

    else:
        score += 10

    one_year_return = round(
        (
            (
                hist["Close"].iloc[-1]
                /
                hist["Close"].iloc[0]
            ) - 1
        ) * 100,
        2
    )

    if one_year_return > 20:
        score += 20

    elif one_year_return > 0:
        score += 10

    score = min(score, 100)

    if score >= 80:

        st.success("🟢 BUY")

    elif score >= 60:

        st.warning("🟡 HOLD")

    else:

        st.error("🔴 SELL")

    st.progress(score / 100)

    st.metric(
        "Confidence",
        f"{score}%"
    )

# -----------------------------------
# PEER COMPARISON
# -----------------------------------

elif page == "⚔️ Peer Comparison":

    st.header("⚔️ ITC Peer Comparison")

    peers = {
        "HUL": "HINDUNILVR.NS",
        "Nestle India": "NESTLEIND.NS",
        "Britannia": "BRITANNIA.NS",
        "Dabur": "DABUR.NS"
    }

    peer = st.selectbox(
        "Select Competitor",
        list(peers.keys())
    )

    peer_stock = yf.Ticker(
        peers[peer]
    )

    peer_info = peer_stock.info

    compare_df = pd.DataFrame({

        "Metric": [
            "Current Price",
            "PE Ratio",
            "Market Cap (Cr)"
        ],

        "ITC": [

            round(current_price, 2),

            round(pe_ratio, 2),

            round(
                market_cap_cr,
                0
            )
        ],

        peer: [

            round(
                peer_info.get(
                    "currentPrice",
                    0
                ),
                2
            ),

            round(
                peer_info.get(
                    "trailingPE",
                    0
                ),
                2
            ),

            round(
                peer_info.get(
                    "marketCap",
                    0
                ) / 10000000,
                0
            )
        ]
    })

    st.dataframe(
        compare_df,
        use_container_width=True
    )

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "Investor Decision Support System | Developed by Aditi Prakash | Powered by Yahoo Finance"
)