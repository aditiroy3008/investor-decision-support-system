import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="ITC Investment Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)
col1 , col2 = st.columns([1,5])

with col1:
    st.image("itc_logo.png", width=80)

with col2:
    st.markdown("""
    <h1 style='color:#0B2E75;font-size:52px;font-weight:800;'>
    ITC Investment Analytics Dashboard
    </h1>
    <h2 style='color:#0B2E75;font-size:15px;font-weight:400;margin-top:-10px;'>
    "Explore ITC's stock performance, financial health,technical indicators and investment outlook."
     </h2>
    """, unsafe_allow_html=True)
    

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

   with st.spinner("Loading ITC market data..."):
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

.main {
    padding-top: 1rem;
}

h1, h2, h3 {
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
# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.sidebar.columns([1,2])

with col1:
    st.image("itc_logo.png", width=70)

with col2:
    st.markdown("""
    <h3 style='margin-top:15px;color:#0B2E75;'>
    ITC Limited
    </h3>
    """, unsafe_allow_html=True)
page = st.sidebar.selectbox(
    "📊 Analysis Modules",
    [
        "🏠 Welcome",
        "🏢 Company Analysis",
        "📈 Technical Analysis",
        "💰 Financial Analysis",
        "🎯 Recommendation",
        "⚔️ Peer Comparison"
    ]
)
st.sidebar.markdown("---")

st.sidebar.success("""
📊 Live Market Data

Source: Yahoo Finance
""")


# -----------------------------------
# HOME PAGE
# -----------------------------------    
if page == "🏠 Welcome":
    st.markdown("---")

    st.info(
        """
📊 Welcome to the ITC Investment Analytics Dashboard.

This platform provides:

• Company Analysis

• Technical Analysis

• Financial Analysis

• Investment Recommendation

• Peer Comparison

Use the Analysis Modules menu on the left to begin exploring the dashboard.
"""
    )
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
        f"{dividend_yield:.2f}%"
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

        dy = dividend_yield 

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

elif page == "🎯 Recommendation":
    st.header("🎯 Investment Recommendation")

    col1, col2, col3 = st.columns(3)

    with col1:
            st.metric("Current Price", f"₹{current_price:.2f}")

    with col2:
                        st.metric("PE Ratio", f"{pe_ratio:.2f}")

    with col3:
                        st.metric(
            "Dividend Yield",
            f"{dividend_yield:.2f}%"
                )
    st.markdown("---")
    st.success("""                            
     ## BUY
    ITC demonstrates:

    ✅ Strong dividend yield

    ✅ Reasonable valuation

    ✅ Stable market position

    ✅ Consistent profitability

    Overall outlook remains positive for long-term investors.
    
""")
    score = 0

    if pe_ratio:

            if pe_ratio < 20:
                score += 20

            elif pe_ratio < 30:
                score += 15

            else:
                score += 5

    if dividend_yield:

            dy = dividend_yield 

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

elif page == "⚔️ Peer Comparison":

    st.header("⚔️ Peer Comparison")

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

    peer_stock = yf.Ticker(peers[peer])
    peer_info = peer_stock.info

    peer_price = peer_info.get(
        "currentPrice",
        peer_info.get("regularMarketPrice", 0)
    )

    peer_pe = peer_info.get(
        "trailingPE",
        0
    )

    peer_dividend = peer_info.get(
        "dividendYield",
        0
    )

    peer_market_cap = (
        peer_info.get(
            "marketCap",
            0
        ) / 10000000
    )

    st.subheader("📊 Quick Comparison")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🏢 ITC")

        st.metric(
            "Current Price",
            f"₹{current_price:.2f}"
        )

        st.metric(
            "PE Ratio",
            f"{pe_ratio:.2f}"
        )

        st.metric(
            "Dividend Yield",
            f"{dividend_yield:.2f}%"
        )

        st.metric(
            "Market Cap",
            f"₹{market_cap_cr:,.0f} Cr"
        )

    with col2:

        st.markdown(f"### 🏢 {peer}")

        st.metric(
            "Current Price",
            f"₹{peer_price:.2f}"
        )

        st.metric(
            "PE Ratio",
            f"{peer_pe:.2f}"
        )

        st.metric(
            "Dividend Yield",
            f"{f"{peer_dividend:.2f}%"}%"
        )

        st.metric(
            "Market Cap",
            f"₹{peer_market_cap:,.0f} Cr"
        )

    st.markdown("---")

    st.subheader("📋 Fundamental Comparison")

    compare_df = pd.DataFrame({

        "Metric": [
            "Current Price",
            "PE Ratio",
            "Dividend Yield (%)",
            "Market Cap (Cr)"
        ],

        "ITC": [
            round(current_price, 2),
            round(pe_ratio, 2),
            round(dividend_yield , 2),
            round(market_cap_cr, 0)
        ],

        peer: [
            round(peer_price, 2),
            round(peer_pe, 2),
           round(peer_dividend , 2),
            round(peer_market_cap, 0)
        ]
    })

    st.dataframe(
        compare_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("📊 Visual Comparison")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="ITC",
            x=["PE Ratio", "Dividend Yield"],
            y=[
                    pe_ratio,
                    dividend_yield 
]
        )
    )

    fig.add_trace(
        go.Bar(
            name=peer,
            x=["PE Ratio", "Dividend Yield"],
            y=[
                peer_pe,
                peer_dividend 
            ]
        )
    )

    fig.update_layout(
        title=f"ITC vs {peer}",
        barmode="group",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🏆 Comparison Verdict")

    score_itc = 0
    score_peer = 0

    if pe_ratio < peer_pe:
        score_itc += 1
    else:
        score_peer += 1

    if dividend_yield > peer_dividend:
        score_itc += 1
    else:
        score_peer += 1

    if market_cap_cr > peer_market_cap:
        score_itc += 1
    else:
        score_peer += 1

    if score_itc > score_peer:

        st.success(
            f"🏆 ITC appears stronger than {peer} based on key fundamentals."
        )

    elif score_peer > score_itc:

        st.warning(
            f"🏆 {peer} appears stronger than ITC based on key fundamentals."
        )

    else:

        st.info(
            "Both companies appear equally strong."
        )
# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "Investor Decision Support System | Developed by Aditi Prakash | Powered by Yahoo Finance"
)