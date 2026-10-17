import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    :root { color-scheme: dark; }
    .stApp { background: #0b0e14; color: #e6eaf2; }
    [data-testid="stSidebar"] { background: #10141d; border-right: 1px solid #242a36; }
    [data-testid="stHeader"] { background: rgba(11,14,20,.92); }
    h1,h2,h3 { letter-spacing: -.025em; }
    div[data-testid="stMetric"] { background: #111722; border: 1px solid #252d3b; padding: 14px 16px; border-radius: 12px; }
    div[data-testid="stMetricLabel"] { color: #9aa6b8; }
    .stButton>button, .stDownloadButton>button { border-radius: 8px; }
    div[data-testid="stDataFrame"] { border: 1px solid #252d3b; border-radius: 10px; overflow: hidden; }
    .block-container { padding-top: 1.7rem; max-width: 1600px; }
    </style>
    """, unsafe_allow_html=True)

def metric_card(column, label, value, help_text=""):
    with column:
        st.metric(label, value)
        if help_text:
            st.caption(help_text)

def sidebar():
    with st.sidebar:
        st.markdown("## ◈ EQUITY RESEARCH")
        st.caption("Multi-market workspace")
        st.divider()
        st.markdown("**Workspace**")
        st.markdown("⌂  Overview")
        st.markdown("◉  Company research")
        st.markdown("▤  Financial statements")
        st.markdown("⌁  Chart analysis")
        st.markdown("☷  Stock screener")
        st.markdown("☆  Watchlists")
        st.divider()
        st.markdown("**Markets**")
        st.caption("SG · US · UK · KR · JP · HK · CN")
        st.divider()
        st.caption("Prototype build · Verify data before use")
        if st.user.get("is_logged_in", False):
            st.caption(f"Signed in: {st.user.get('email', 'user')}")
            if st.button("Sign out", use_container_width=True):
                st.logout()
    return {}
