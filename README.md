# Equity Research — Multi-market Stock Research Starter

A GitHub-ready Streamlit starter for a private stock research workspace, with a dark research-terminal UI, historical price charts, a TradingView embed, financial statement retrieval, and an optional Supabase database schema.

## Included
- Seven market presets: Singapore, US, UK, South Korea, Japan, Hong Kong, China
- Historical price selector up to 10 years, subject to provider coverage
- Plotly price charts and basic financial-statement tables
- TradingView chart widget embed
- Optional Streamlit OIDC login and email allowlist
- Supabase/PostgreSQL starter schema for profiles, watchlists, saved screens and invitations
- CSV exports for retrieved financial statement data

## Run locally
Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Create a **private** GitHub repository.
2. Upload the contents of this folder (not the enclosing folder).
3. In Streamlit Community Cloud, create an app pointing to `app.py`.
4. Add secrets in the app's settings; never commit real secrets.
5. If using OIDC, configure the identity provider's redirect URI to `https://YOUR-APP.streamlit.app/oauth2callback`.
6. Test with an authorized account and an unauthorized account before inviting users.

Streamlit's hosting policies and private-app limits can change. Confirm current plan limits before relying on a free private deployment.

## Authentication notes
- When `[auth] client_id` is configured, the app requires Streamlit's OIDC login.
- Optional `[access] allowed_emails` limits access to listed email addresses.
- If auth is not configured, the app runs in local/demo mode and shows a warning. **Do not treat an unauthenticated deployment as private.**
- OIDC must be configured in the hosting platform; this project does not create identity-provider credentials for you.
- The Supabase schema is a foundation only. App-level persistence is not yet connected. Never expose a Supabase service-role key to browser/client code.

## Market data notes
The current adapter uses `yfinance` to access Yahoo Finance data. This is convenient for a prototype but is **not an official exchange feed**, can be delayed or incomplete, may change without notice, and may be subject to provider terms. Do not assume redistribution or commercial use is permitted. Coverage differs by ticker and market.

The app requests up to 10 years of price history where available; it does **not** guarantee ten years of data for every security. Current financial-statement retrieval generally returns only the provider's available periods and is not a guarantee of ten years of financials.

For production, implement provider adapters for official exchange/issuer data and licensed alternatives, document provenance and timestamps per field, validate adjusted vs unadjusted prices, corporate actions, currencies, fiscal-year alignment, and restatements.

## TradingView
The app embeds a TradingView chart widget. Widget availability, symbol naming, and data rights vary by exchange and plan. Some symbols may require ticker-prefix adjustments. This is not a full licensed TradingView Charting Library integration; the full library has separate access/licensing requirements.

## Security checklist before inviting users
- Configure OIDC and an explicit email allowlist.
- Use a private GitHub repository and keep secrets out of Git.
- Enable Supabase RLS and test cross-user isolation.
- Add server-side authorization for every database operation.
- Set backups/retention and review hosting logs.
- Do not store brokerage credentials or sensitive personal information in this prototype.

## Project structure
```text
app.py
components/
  ui.py
services/
  auth.py
  charts.py
  market_data.py
  tradingview.py
database/
  schema.sql
.streamlit/
  config.toml
  secrets.toml.example
requirements.txt
README.md
.gitignore
```

## Disclaimer
For research and educational purposes only. Not investment advice. Verify material facts against official exchange filings and issuer disclosures.
