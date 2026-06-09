import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
@st.cache_data(ttl=300)
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)

    return {
        "info": stock.info,
        "history": stock.history(
            period="1y",
            auto_adjust=True
        )
    }
# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Investor Decision Support System",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.big-title {
    font-size: 52px;
    font-weight: 800;
    color: #0B2E75;
}

[data-testid="metric-container"] {
    border: 1px solid #D1D5DB;
    padding: 15px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
<div style="padding:10px 0px;">
    <h1 style="color:#0B2E75; margin-bottom:0;">
        📈 Investor Decision Support System
    </h1>
    <p style="font-size:18px; color:gray;">
        Real-time stock analysis, comparison and investment insights
    </p>
</div>
""", unsafe_allow_html=True)
st.info("🟢 Market Data Source: Yahoo Finance | Live Data")

st.write("")

# -----------------------------------
# INPUT
# -----------------------------------
companies = {
    "ITC": "ITC.NS",
    "HUL": "HINDUNILVR.NS",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS"
}

st.sidebar.title("📈 Investor Dashboard")

company1 = st.sidebar.selectbox(
    "Select Company",
    list(companies.keys())
)

company2 = st.sidebar.selectbox(
    "Compare With",
    list(companies.keys()),
    index=1
)
if company1 == company2:
        st.warning(
            "Please select two different companies."
        )
        st.stop()



ticker1 = companies[company1]
ticker2 = companies[company2]

analyze = st.sidebar.button("🚀 Analyze")
st.sidebar.markdown("---")

st.sidebar.info(
    """
📊 Data Source:
Yahoo Finance

🔄 Data Type:
Real-Time Market Data
"""
)
# -----------------------------------
# ANALYSIS
# -----------------------------------

if analyze:
    try:
        data1 = get_stock_data(ticker1)
        data2 = get_stock_data(ticker2)

        info = data1["info"]
        

        info1 = data1["info"]
        info2 = data2["info"]

        hist = data1["history"]
        hist1 = data1["history"]
        hist2 = data2["history"]
        tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Technical Analysis",
    "⚔️ Comparison",
    "🤖 Recommendation"
])

        company_name = info.get("longName", "N/A")
        current_price = info.get("currentPrice", 0)
        market_cap = info.get("marketCap", 0)
        pe_ratio = info.get("trailingPE", 0)
        dividend_yield = info.get("dividendYield", 0)

        market_cap_cr = market_cap / 10000000

        st.markdown("---")
        
        with tab1:
            

                st.subheader(company_name)
                st.info(
                    f"""
                📊 Sector: {info.get('sector','N/A')}

                🏭 Industry: {info.get('industry','N/A')}

                🌍 Country: {info.get('country','N/A')}
                """
                )

                # -----------------------------------
                # KPI SECTION
                # -----------------------------------

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Current Price",
                        f"₹{current_price}"
                    )

                with col2:
                    st.metric(
                        "Market Cap",
                        f"₹{market_cap_cr:,.0f} Cr"
                    )

                with col3:
                    st.metric(
                        "PE Ratio",
                        pe_ratio
                    )

                with col4:
                    st.metric(
                        "Dividend Yield",
                        f"{dividend_yield}%"
                    )

                # -----------------------------------
        # COMPANY OVERVIEW
        # -----------------------------------

        
        with tab1:
                
                fifty_two_high = info.get("fiftyTwoWeekHigh", 0)
                fifty_two_low = info.get("fiftyTwoWeekLow", 0)

                if (
                    fifty_two_high
                    and fifty_two_low
                    and fifty_two_high != fifty_two_low
                ):
                    price_position = (
                        (current_price - fifty_two_low)
                        /
                        (fifty_two_high - fifty_two_low)
                    ) * 100

                    st.progress(price_position / 100)

                    st.write(
                        f"Current price is {price_position:.1f}% of the 52-week range"
                    )
                    summary = info.get(
                    "longBusinessSummary",
                    "No company information available."
                )

                    st.write(summary[:500] + "...")

                    with st.expander("Read Full Company Overview"):
                        st.write(summary)
                        # -----------------------------------
                # STOCK DATA
                # -----------------------------------
                hist = data1["history"]
                                  

                # Create 30 DMA column
                hist["30DMA"] = hist["Close"].rolling(window=30).mean()

                latest_price = hist["Close"].iloc[-1]
                latest_dma = hist["30DMA"].iloc[-1]

                

                with tab2:
                        st.subheader("📈 Stock Price vs 30-Day Moving Average")

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
                                name="30 Day Moving Average"
                            )
                        )

                        fig.update_layout(
                            template="plotly_white",
                            height=600,
                            xaxis_title="Date",
                            yaxis_title="Price (₹)"
                        )

                        st.plotly_chart(fig, use_container_width=True)
                        st.subheader("📉 Volatility Analysis")

                        volatility = (
                            hist["Close"]
                            .pct_change()
                            .std()
                            * (252 ** 0.5)
                            * 100
                        )

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
                # -----------------------------------
                # MOVING AVERAGE ANALYSIS
                # -----------------------------------

                with tab2 :
                    st.subheader("📊 30-Day Moving Average Analysis")

                    if latest_price > latest_dma:
                            st.success(
                                f"Bullish Signal\n\nCurrent Price: ₹{latest_price:.2f}\n\n30 DMA: ₹{latest_dma:.2f}"
                            )
                    else:
                            st.warning(
                                f"Bearish Signal\n\nCurrent Price: ₹{latest_price:.2f}\n\n30 DMA: ₹{latest_dma:.2f}"
                            )

        # -----------------------------------
        # FINANCIAL HEALTH SCORE
        # -----------------------------------

        
        with tab4:
            st.subheader("🏥 Financial Health Score")

            score = 0

            # PE Ratio
            if pe_ratio:
                if pe_ratio < 20:
                    score += 20
                elif pe_ratio < 30:
                    score += 15
                else:
                    score += 5

            # Dividend Yield
            if dividend_yield:
                dy = dividend_yield * 100 if dividend_yield <= 1 else dividend_yield

                if dy > 4:
                    score += 20
                elif dy > 2:
                    score += 15
                else:
                    score += 5

            # Trend
            if latest_price > latest_dma:
                score += 20
            else:
                score += 10

            # Market Cap
            if market_cap_cr > 100000:
                score += 20
            else:
                score += 10
            # 1 year return 
            hist = data1["history"]

            hist1 = data1["history"]
            hist2 = data2["history"]



            return1 = round(
                    ((hist1["Close"].iloc[-1] / hist1["Close"].iloc[0]) - 1) * 100,
                    2
                )

            return2 = round(
                    ((hist2["Close"].iloc[-1] / hist2["Close"].iloc[0]) - 1) * 100,
                    2
                )
            if return1 > 20:
                        score += 20
            elif return1 > 0:
                        score += 10
            else:
                        score += 0

            score = min(score, 100)

                # Grade
            if score >= 85:
                    grade = "A"
            elif score >= 70:
                    grade = "B"
            elif score >= 55:
                    grade = "C"
            else:
                    grade = "D"

                # Risk
            beta = info.get("beta", 1)

            if beta < 0.8:
                    risk = "Low Risk"
            elif beta < 1.2:
                    risk = "Moderate Risk"
            else:
                    risk = "High Risk"

                # Layout
            col1, col2 = st.columns([2, 3])

            with col1:
                    st.metric("Financial Health Score", f"{score}/100")
                    st.metric("Investment Grade", grade)
                    st.metric("Risk Level", risk)

            with col2:
                        fig_gauge = go.Figure(
                            go.Indicator(
                                mode="gauge+number",
                                value=score,
                                title={"text": "Health Score"},
                                gauge={
                                    "axis": {"range": [0, 100]},
                                    "bar": {"color": "#0B2E75"},
                                    "steps": [
                                        {"range": [0, 55], "color": "#FF4C4C"},
                                        {"range": [55, 70], "color": "#FFB84C"},
                                        {"range": [70, 85], "color": "#FFFF4C"},
                                        {"range": [85, 100], "color": "#4CAF50"}
                                    ]
                                }
                            )
                        )

                        fig_gauge.update_layout(
                            template="plotly_white",
                            height=300,
                            width=500
                        )
                        st.plotly_chart(
                        fig_gauge,
                        use_container_width=False
                    )

                        # -----------------------------------
                        # AI RECOMMENDATION
                        # -----------------------------------

                
            st.subheader("🤖 AI Investment Recommendation")

            if score >= 80:
                    st.success("🟢 BUY")
            elif score >= 60:
                    st.warning("🟡 HOLD")
            else:
                    st.error("🔴 SELL")
            st.subheader("🎯 Recommendation Confidence")

            confidence = score

            st.progress(confidence / 100)
            st.metric("Confidence Level", f"{confidence}%")
            strengths = []
            weaknesses = []

                # PE Ratio
            if pe_ratio < 20:
                strengths.append("Low PE Ratio (Attractive Valuation)")
            else:
                weaknesses.append("High PE Ratio (Expensive Valuation)")

            # Dividend Yield
            if dividend_yield > 2:
                strengths.append("Good Dividend Yield")
            else:
                weaknesses.append("Low Dividend Yield")

            # Market Cap
            if market_cap_cr > 100000:
                strengths.append("Large Market Cap (Stable Company)")
            else:
                weaknesses.append("Smaller Market Cap")

            # 30 DMA Trend
            if latest_price > latest_dma:
                strengths.append("Trading Above 30-Day Moving Average")
            else:
                weaknesses.append("Trading Below 30-Day Moving Average")

            # 1 Year Return
            if return1 > 0:
                strengths.append(f"Positive 1-Year Return ({return1:.2f}%)")
            else:
                weaknesses.append(f"Negative 1-Year Return ({return1:.2f}%)")   
            

            st.subheader("💪 Top Strengths")

            strength_text = "\n".join([f"\n ✓ {item}" for item in strengths])
            st.success(strength_text)

            st.subheader("⚠️ Top Weaknesses")

            weakness_text = "\n".join([f"\n ✗ {item}" for item in weaknesses])
            st.warning(weakness_text)   
            st.subheader("📝 Overall Analysis")

            analysis = []

            if pe_ratio < 20:
                analysis.append("attractive valuation")

            if dividend_yield > 2:
                analysis.append("strong dividend income")

            if latest_price > latest_dma:
                analysis.append("bullish trend")

            if return1 > 0:
                analysis.append("positive yearly performance")

            st.info(
                f"The company shows {', '.join(analysis)}.\n "
                f"\nFinancial Health Score: {score}/100."
            )    

                        # -----------------------------------
                        # EXTRA INFORMATION
                        # -----------------------------------

                    
            with tab1:
                        st.subheader("📌 Additional Information")

                        col1, col2 = st.columns(2)

                        with col1:
                                    st.write(f"**Sector:** {info.get('sector','N/A')}")
                                    st.write(f"**Industry:** {info.get('industry','N/A')}")
                                    st.write(f"**Country:** {info.get('country','N/A')}")

                        with col2:
                                    st.write(f"**52 Week High:** ₹{info.get('fiftyTwoWeekHigh','N/A')}")
                                    st.write(f"**52 Week Low:** ₹{info.get('fiftyTwoWeekLow','N/A')}")
                                    st.write(f"**Website:** {info.get('website','N/A')}")
                        st.subheader("📊 Key Investment Metrics")

                        col1, col2, col3 = st.columns(3)

                        roe = info.get("returnOnEquity", "N/A")
                        eps = info.get("trailingEps", "N/A")
                        debt_equity = info.get("debtToEquity", "N/A")

                        with col1:
                            if roe != "N/A":
                                st.metric("ROE", f"{roe*100:.2f}%")
                            else:
                                st.metric("ROE", "N/A")

                        with col2:
                            st.metric("EPS", eps)

                        with col3:
                            st.metric("Debt/Equity", debt_equity)
                # -----------------------------------
                # STOCK COMPARISON
                # -----------------------------------

            
                        with tab3:
                            st.subheader("⚔️ Stock Comparison")

                            stock1 = yf.Ticker(ticker1)
                            stock2 = yf.Ticker(ticker2)

                            info1 = stock1.info
                            info2 = stock2.info
                            hist1 = stock1.history(period="1y")
                            hist2 = stock2.history(period="1y")

                            c1, c2 = st.columns(2)

                            with c1:
                                            st.metric(
                                                "Current Price",
                                                f"₹{info1.get('currentPrice', 'N/A')}"
                                            )
                                            st.metric(
                                                "PE Ratio",
                                                info1.get('trailingPE', 'N/A')
                                            )
                                            st.metric(
                                                "Dividend Yield",
                                                info1.get('dividendYield', 'N/A')
                                            )

                            with c2:
                                            
                                            st.metric(
                                                "Current Price",
                                                f"₹{info2.get('currentPrice', 'N/A')}"
                                            )
                                            st.metric(
                                                "PE Ratio",
                                                info2.get('trailingPE', 'N/A')
                                            )
                                            st.metric(
                                                "Dividend Yield",
                                                info2.get('dividendYield', 'N/A')
                                            )
                            return1 = round(
                                ((hist1["Close"].iloc[-1] / hist1["Close"].iloc[0]) - 1) * 100,
                                2
                            )

                            return2 = round(
                                ((hist2["Close"].iloc[-1] / hist2["Close"].iloc[0]) - 1) * 100,
                                2
                            )

                            compare_df = pd.DataFrame({
                                "Metric": [
                                    "Current Price",
                                    "PE Ratio",
                                    "Dividend Yield",
                                    "Market Cap (Cr)",
                                    "1Y Return (%)"
                                ],
                                company1: [
                                    round(info1.get("currentPrice", 0), 2),
                                    round(info1.get("trailingPE", 0), 2),
                                    round(info1.get("dividendYield", 0), 2),
                                    round(info1.get("marketCap", 0) / 10000000, 0),
                                    return1
                                ],
                                company2: [
                                    round(info2.get("currentPrice", 0), 2),
                                    round(info2.get("trailingPE", 0), 2),
                                    round(info2.get("dividendYield", 0), 2),
                                    round(info2.get("marketCap", 0) / 10000000, 0),
                                    return2
                                ],
                                "Winner": [
                                    company1 if info1.get("currentPrice",0) > info2.get("currentPrice",0) else company2,
                                    company1 if info1.get("trailingPE",999) < info2.get("trailingPE",999) else company2,
                                    company1 if info1.get("dividendYield",0) > info2.get("dividendYield",0) else company2,
                                    company1 if info1.get("marketCap",0) > info2.get("marketCap",0) else company2,
                                    company1 if return1 > return2 else company2
                                ]
                            })

                            st.dataframe(compare_df, use_container_width=True, hide_index=True)
                                            
                            st.subheader("📈 Percentage Growth Comparison")

                            

                            # Normalize both stocks to 100
                            hist1["Growth"] = (hist1["Close"] / hist1["Close"].iloc[0]) * 100
                            hist2["Growth"] = (hist2["Close"] / hist2["Close"].iloc[0]) * 100

                            fig_compare = go.Figure()

                            fig_compare.add_trace(
                                go.Scatter(
                                    x=hist1.index,
                                    y=hist1["Growth"],
                                    mode="lines",
                                    name=company1
                                )
                            )

                            fig_compare.add_trace(
                                go.Scatter(
                                    x=hist2.index,
                                    y=hist2["Growth"],
                                    mode="lines",
                                    name=company2
                                )
                            )

                            fig_compare.update_layout(
                                title="1-Year Percentage Growth Comparison",
                                template="plotly_white",
                                height=500,
                                xaxis_title="Date",
                                yaxis_title="Growth Index (Base = 100)"
                            )

                            st.plotly_chart(fig_compare, use_container_width=True)
                                    
                            
                            st.subheader("🏆 Comparison Verdict")
                            score1 = 0
                            score2 = 0

                                    # Current Price
                            if info1.get("currentPrice", 0) > info2.get("currentPrice", 0):
                                        score1 += 1
                            else:
                                        score2 += 1

                                    # PE Ratio (lower is better)
                            if info1.get("trailingPE", 999) < info2.get("trailingPE", 999):
                                        score1 += 1
                            else:
                                        score2 += 1

                                    # Dividend Yield (higher is better)
                            if info1.get("dividendYield", 0) > info2.get("dividendYield", 0):
                                        score1 += 1
                            else:
                                        score2 += 1

                                    # Market Cap (higher is better)
                            if info1.get("marketCap", 0) > info2.get("marketCap", 0):
                                        score1 += 1
                            else:
                                        score2 += 1

                                    # 1 Year Return
                            if return1 > return2:
                                        score1 += 1
                            else:
                                        score2 += 1

                            st.write(f"**{company1} Score:** {score1}")
                            st.write(f"**{company2} Score:** {score2}")

                            if score1 > score2:
                                        st.success(f"🏆 {company1} appears stronger based on current fundamentals.")
                            elif score2 > score1:
                                        st.success(f"🏆 {company2} appears stronger based on current fundamentals.")
                            else:
                                        st.info("Both companies appear equally strong.")


    except Exception as e:
     st.error(f"Error: {e}")
st.markdown("---")

st.caption(
            "Investor Decision Support System | Developed by Aditi Prakash | Powered by Yahoo Finance"
        )