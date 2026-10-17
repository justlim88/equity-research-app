from __future__ import annotations

import streamlit as st
from components.ui import apply_styles, sidebar, metric_card
from services.auth import require_access
from services.market_data import (
    MARKET_OPTIONS, search_symbols, get_history, get_company_info,
    get_financials, get_demo_watchlist, provider_status,
)
from services.charts import price_chart, financial_chart
from services.tradingview import render_tradingview_widget

st.set_page_config(
    page_title="Equity Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()
require_access()
selection = sidebar()

st.title("Equity Research")
st.caption("A multi-market research workspace · Data sources and timestamps are shown where available.")

with st.container():
    a, b, c, d = st.columns(4)
    metric_card(a, "Markets", "7", "SG · US · UK · KR · JP · HK · CN")
    metric_card(b, "Historical prices", "Up to 10Y", "Provider coverage varies by symbol")
    metric_card(c, "Charting", "TradingView", "Widget integration + Plotly")
    metric_card(d, "Data status", "Provider-backed", "Verify before making decisions")

st.divider()

left, right = st.columns([1.55, 1], gap="large")
with left:
    st.subheader("Company research")
    market = st.selectbox("Market", list(MARKET_OPTIONS.keys()), index=1)
    query = st.text_input("Search ticker or company", placeholder="e.g. AAPL, MSFT, D05.SI")
    suggestions = search_symbols(query, market) if query else []
    if suggestions:
        labels = {f"{x['symbol']} — {x['name']}": x["symbol"] for x in suggestions}
        chosen_label = st.selectbox("Matching symbols", list(labels.keys()))
        symbol = labels[chosen_label]
    else:
        defaults = {"Singapore": "D05.SI", "United States": "AAPL", "United Kingdom": "SHEL.L",
                    "South Korea": "005930.KS", "Japan": "7203.T", "Hong Kong": "0700.HK", "China": "600519.SS"}
        symbol = st.text_input("Ticker symbol", value=defaults.get(market, "AAPL"), help="Enter a provider-supported ticker.")
    period = st.select_slider("Price history", options=["1M", "3M", "6M", "1Y", "3Y", "5Y", "10Y"], value="10Y")
    if symbol:
        info = get_company_info(symbol)
        hist = get_history(symbol, period)
        st.markdown(f"### {info.get('name', symbol)}")
        st.caption(f"{symbol} · {info.get('exchange', market)} · {info.get('currency', 'Currency varies')} · {info.get('source', 'Yahoo Finance via yfinance')}")
        if not hist.empty:
            latest = float(hist["Close"].dropna().iloc[-1])
            previous = float(hist["Close"].dropna().iloc[-2]) if len(hist) > 1 else latest
            change = latest - previous
            change_pct = (change / previous * 100) if previous else 0
            m1, m2, m3 = st.columns(3)
            metric_card(m1, "Latest close", f"{latest:,.2f}", info.get("currency", "Provider currency"))
            metric_card(m2, "Daily change", f"{change:+,.2f}", f"{change_pct:+.2f}%")
            metric_card(m3, "Market cap", info.get("market_cap_display", "Not provided"), "Provider-reported")
            st.plotly_chart(price_chart(hist, symbol), use_container_width=True, config={"displaylogo": False, "responsive": True})
            st.caption(f"History: {hist.index.min().date()} to {hist.index.max().date()} · {len(hist):,} observations. Price history is provider-supplied and may be delayed or adjusted.")
        else:
            st.warning("No price history was returned. Check the ticker format, provider availability, or network access.")
with right:
    st.subheader("TradingView chart")
    st.caption("Embedded chart widget. TradingView widget terms and data availability apply.")
    render_tradingview_widget(symbol if symbol else "NASDAQ:AAPL", market)
    st.subheader("Research checklist")
    st.markdown(
        "- [ ] Confirm ticker, listing venue and currency\n"
        "- [ ] Check annual and quarterly filings\n"
        "- [ ] Compare at least two data sources\n"
        "- [ ] Review corporate actions and share-count changes\n"
        "- [ ] Record thesis, valuation and downside risks"
    )

st.divider()
tabs = st.tabs(["Financials", "Watchlist", "Data coverage", "About"])
with tabs[0]:
    st.subheader("Financial statements")
    st.info("Financial statement availability depends on the data provider. This screen displays the fields returned by the current provider; it does not guarantee a complete 10-year financial history.")
    if symbol:
        financials = get_financials(symbol)
        if financials is not None and not financials.empty:
            st.dataframe(financials, use_container_width=True)
            st.download_button("Download financials CSV", financials.to_csv().encode("utf-8"), file_name=f"{symbol}_financials.csv", mime="text/csv")
            numeric_cols = [c for c in financials.columns if c.lower() in ("total revenue", "operating income", "net income", "gross profit")]
            if numeric_cols:
                st.plotly_chart(financial_chart(financials, numeric_cols[0]), use_container_width=True)
        else:
            st.warning("No financial statements returned by the configured provider for this ticker.")
with tabs[1]:
    st.subheader("Starter watchlist")
    watchlist = get_demo_watchlist()
    st.dataframe(watchlist, use_container_width=True, hide_index=True)
    st.caption("This is a starter/demo watchlist. Persistent per-user watchlists are enabled after Supabase is configured; see README.")
with tabs[2]:
    st.subheader("Market coverage")
    st.dataframe(
        [{"Market": k, "Default ticker example": v, "Provider": "Yahoo Finance / yfinance (unofficial)"}
         for k, v in {"Singapore": "D05.SI", "United States": "AAPL", "United Kingdom": "SHEL.L",
                      "South Korea": "005930.KS", "Japan": "7203.T", "Hong Kong": "0700.HK",
                      "China": "600519.SS"}.items()],
        use_container_width=True, hide_index=True,
    )
    st.warning("Ticker availability, history length, fundamentals, exchange coverage and permitted usage vary. This project does not imply official exchange data access.")
    st.write("Provider connectivity:", provider_status())
with tabs[3]:
    st.subheader("About this project")
    st.write("A GitHub-ready starter for a private, multi-market equity research app. It combines Streamlit, Plotly, a TradingView embed, optional OIDC authentication, and an optional Supabase persistence layer.")
    st.write("Not investment advice. Market data may be delayed, incomplete, adjusted, or inaccurate. Verify important information against official exchange filings and issuer disclosures.")
