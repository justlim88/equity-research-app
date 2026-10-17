import streamlit as st

def require_access():
    """OIDC auth when configured; local demo mode when auth is not configured."""
    auth_configured = bool(st.secrets.get("auth", {}).get("client_id", ""))
    if auth_configured:
        if not st.user.is_logged_in:
            st.title("Equity Research")
            st.write("Sign in with your approved account to continue.")
            st.button("Sign in", on_click=st.login, type="primary")
            st.stop()
        email = str(st.user.get("email", "")).strip().lower()
        allowlist = [str(x).strip().lower() for x in st.secrets.get("access", {}).get("allowed_emails", [])]
        if not allowlist:
            st.error("Access is not configured. Add invited email addresses to [access].allowed_emails in app secrets before deployment.")
            st.stop()
        if email not in allowlist:
            st.error("This account has not been invited to this workspace.")
            st.stop()
    else:
        st.sidebar.warning("Local/demo mode: authentication is not configured.")
