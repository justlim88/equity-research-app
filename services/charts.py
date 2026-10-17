import pandas as pd
import plotly.graph_objects as go

def price_chart(history: pd.DataFrame, symbol: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history.index, y=history["Close"], name="Close", mode="lines",
                             line={"color":"#72a7ff", "width":2}, hovertemplate="%{x|%Y-%m-%d}<br>%{y:,.2f}<extra></extra>"))
    if "Volume" in history:
        fig.add_trace(go.Bar(x=history.index, y=history["Volume"], name="Volume", yaxis="y2", opacity=.18))
    fig.update_layout(
        title=f"{symbol} · Historical price", template="plotly_dark", height=390,
        margin={"l":8,"r":8,"t":45,"b":8}, paper_bgcolor="#0b0e14", plot_bgcolor="#0b0e14",
        xaxis={"showgrid":False, "rangeslider":{"visible":False}},
        yaxis={"title":"Price", "gridcolor":"#202938"},
        yaxis2={"overlaying":"y","side":"right","showgrid":False,"visible":False},
        legend={"orientation":"h","y":1.08,"x":1,"xanchor":"right"},
    )
    return fig

def financial_chart(financials: pd.DataFrame, metric: str):
    if metric not in financials.columns:
        return go.Figure()
    values = pd.to_numeric(financials[metric], errors="coerce")
    fig = go.Figure(go.Bar(x=financials["Metric"], y=values, name=metric))
    fig.update_layout(title=metric, template="plotly_dark", height=300, margin={"l":8,"r":8,"t":45,"b":8},
                      paper_bgcolor="#0b0e14", plot_bgcolor="#0b0e14", yaxis={"gridcolor":"#202938"})
    return fig
