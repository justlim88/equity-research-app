import streamlit.components.v1 as components

MARKET_PREFIX = {
    "Singapore": "SGX", "United States": "NASDAQ", "United Kingdom": "LSE",
    "South Korea": "KRX", "Japan": "TSE", "Hong Kong": "HKEX", "China": "SSE",
}

def render_tradingview_widget(symbol: str, market: str, height: int = 500):
    # Symbol mapping can differ by venue/provider. Users may need to adjust the prefix for a ticker.
    normalized = symbol.strip().upper()
    if ":" not in normalized:
        normalized = f"{MARKET_PREFIX.get(market, 'NASDAQ')}:{normalized}"
    safe_symbol = normalized.replace("\\", "").replace("'", "")
    html = f"""
    <div class="tradingview-widget-container" style="height:{height}px;width:100%">
      <div id="tradingview_chart" style="height:calc(100% - 32px);width:100%"></div>
      <div class="tradingview-widget-copyright">
        <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
          <span>Chart powered by TradingView</span>
        </a>
      </div>
    </div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{safe_symbol}",
        "interval": "D",
        "timezone": "Asia/Singapore",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart",
        "hide_side_toolbar": false,
        "withdateranges": true
      }});
    </script>
    """
    components.html(html, height=height, scrolling=False)
