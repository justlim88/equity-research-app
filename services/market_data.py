from __future__ import annotations
import pandas as pd
import streamlit as st

MARKET_OPTIONS = {
    "Singapore": "SG", "United States": "US", "United Kingdom": "UK",
    "South Korea": "KR", "Japan": "JP", "Hong Kong": "HK", "China": "CN",
}

@st.cache_data(ttl=900, show_spinner=False)
def get_history(symbol: str, period: str = "10Y") -> pd.DataFrame:
    try:
        import yfinance as yf
        period_map = {"1M":"1mo", "3M":"3mo", "6M":"6mo", "1Y":"1y", "3Y":"3y", "5Y":"5y", "10Y":"10y"}
        df = yf.Ticker(symbol.strip()).history(period=period_map.get(period, "10y"), auto_adjust=False)
        if df is None or df.empty:
            return pd.DataFrame()
        df.index = pd.to_datetime(df.index).tz_localize(None) if getattr(df.index, "tz", None) else pd.to_datetime(df.index)
        return df.dropna(subset=["Close"])
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_company_info(symbol: str) -> dict:
    try:
        import yfinance as yf
        info = yf.Ticker(symbol.strip()).get_info() or {}
        cap = info.get("marketCap")
        return {
            "name": info.get("longName") or info.get("shortName") or symbol,
            "exchange": info.get("fullExchangeName") or info.get("exchange") or "Unknown exchange",
            "currency": info.get("currency") or "Provider currency",
            "market_cap": cap,
            "market_cap_display": f"{cap:,.0f}" if isinstance(cap, (int, float)) else "Not provided",
            "source": "Yahoo Finance via yfinance",
        }
    except Exception:
        return {"name": symbol, "exchange": "Unknown exchange", "currency": "Provider currency",
                "market_cap": None, "market_cap_display": "Not provided", "source": "Yahoo Finance via yfinance"}

@st.cache_data(ttl=3600, show_spinner=False)
def get_financials(symbol: str) -> pd.DataFrame:
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol.strip())
        annual = ticker.income_stmt
        if annual is None or annual.empty:
            annual = ticker.financials
        if annual is None or annual.empty:
            return pd.DataFrame()
        df = annual.copy()
        df.columns = [pd.to_datetime(c).strftime("%Y-%m-%d") if not isinstance(c, str) else c[:10] for c in df.columns]
        df.index.name = "Metric"
        return df.reset_index()
    except Exception:
        return pd.DataFrame()

def search_symbols(query: str, market: str):
    """Small provider-backed symbol search. yfinance search results vary by market."""
    if not query.strip():
        return []
    try:
        import yfinance as yf
        results = yf.Search(query, max_results=8).quotes or []
        market_codes = {"Singapore": ["SES", "SGX"], "United States": ["NMS", "NYQ", "NASDAQ", "NYSE"],
                        "United Kingdom": ["LSE"], "South Korea": ["KSC"], "Japan": ["JPX"],
                        "Hong Kong": ["HKG"], "China": ["SHH", "SHZ"]}
        allowed = market_codes.get(market, [])
        rows = []
        for item in results:
            symbol = item.get("symbol", "")
            exchange = str(item.get("exchange", "")).upper()
            if allowed and not any(code in exchange for code in allowed):
                continue
            rows.append({"symbol": symbol, "name": item.get("longname") or item.get("shortname") or symbol})
        return rows or [{"symbol": query.upper().strip(), "name": query.upper().strip()}]
    except Exception:
        return [{"symbol": query.upper().strip(), "name": query.upper().strip()}]

def get_demo_watchlist():
    return pd.DataFrame([
        {"Symbol":"AAPL", "Company":"Apple Inc.", "Market":"US", "Status":"Example"},
        {"Symbol":"MSFT", "Company":"Microsoft Corporation", "Market":"US", "Status":"Example"},
        {"Symbol":"D05.SI", "Company":"DBS Group Holdings", "Market":"SG", "Status":"Example"},
        {"Symbol":"7203.T", "Company":"Toyota Motor", "Market":"JP", "Status":"Example"},
    ])

def provider_status():
    try:
        import yfinance
        return f"yfinance package installed (version {yfinance.__version__}); access depends on network/provider availability."
    except Exception:
        return "yfinance unavailable; install requirements.txt and check network access."
