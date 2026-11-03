"""
buffett_app.py — Warren Buffett 10-K Quantitative Screening & Provenance Lab
FIN 43900: Advanced Financial Modeling / AI in Finance (Lab 18)
"""

import os
import re
import pandas as pd
import numpy as np
import streamlit as st

import buffett

# -----------------------------------------------------------------------------
# Configuration and Styling
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Buffett 10-K Provenance Engine",
    page_icon="🏛️",
    layout="wide"
)

# Custom Berkshire-inspired Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1e3d59;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .moat-wide {
        background-color: #d4edda;
        color: #155724;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .moat-narrow {
        background-color: #fff3cd;
        color: #856404;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .moat-none {
        background-color: #f8d7da;
        color: #721c24;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Title & Required Subtitle Disclaimer
# -----------------------------------------------------------------------------

st.title("🏛️ Warren Buffett 10-K Value Investing Skill")
st.markdown(
    "**data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.**"
)
st.caption("Keyless XBRL fact ingestion · Pure code computation · Deterministic checks · Model provenance auditor")
st.write("---")

# -----------------------------------------------------------------------------
# Sidebar: Controls & Case Studies
# -----------------------------------------------------------------------------

st.sidebar.header("🎯 Case Studies & Controls")

# Quick Selection Buttons
col_b1, col_b2 = st.sidebar.columns(2)
with col_b1:
    if st.button("🛒 COST (Costco)", use_container_width=True):
        st.session_state["ticker_sym"] = "COST"
    if st.button("🏨 MAR (Marriott)", use_container_width=True):
        st.session_state["ticker_sym"] = "MAR"
    if st.button("🍎 AAPL (Apple)", use_container_width=True):
        st.session_state["ticker_sym"] = "AAPL"

with col_b2:
    if st.button("🏛️ JPM (JPMorgan)", use_container_width=True):
        st.session_state["ticker_sym"] = "JPM"
    if st.button("⚡ TSLA (Tesla)", use_container_width=True):
        st.session_state["ticker_sym"] = "TSLA"

default_ticker = st.session_state.get("ticker_sym", "COST")

ticker_input = st.sidebar.text_input(
    "Enter Stock Ticker:",
    value=default_ticker
).strip().upper()

st.sidebar.markdown("---")
st.sidebar.subheader("🧪 Anti-Hallucination Lab")
provenance_preset = st.sidebar.radio(
    "Test Provenance Scenarios:",
    [
        "✅ Grounded 10-K Memo (100% Truth)",
        "🚨 Injected Unprinted Numbers (40.0% ROE)",
        "💣 Wall Street Consensus Hype ($915 target, 52x P/E)"
    ]
)

# -----------------------------------------------------------------------------
# Ingestion & Metric Calculations
# -----------------------------------------------------------------------------

try:
    data = buffett.get_buffett_metrics(ticker_input)
except Exception as e:
    st.error(f"Error fetching data for ticker '{ticker_input}': {e}")
    st.stop()

rows = data["rows"]
checks = data["checks"]
company_name = data["company_name"]
cik = data["cik"]

r_first = rows[0]
r_last = rows[-1]

# -----------------------------------------------------------------------------
# Executive Metrics Ribbon
# -----------------------------------------------------------------------------

st.subheader(f"📊 10-K Fundamental Health: {company_name} ({ticker_input})")

m1, m2, m3, m4 = st.columns(4)

# 1. Revenue
if r_last["revenue"] and r_first["revenue"]:
    rev_cagr = ((r_last["revenue"] / r_first["revenue"]) ** (1 / 4) - 1) * 100.0
    m1.metric("FY Revenue ($M)", f"${r_last['revenue']:,.0f}", f"{rev_cagr:+.1f}% 4-Yr CAGR")
else:
    m1.metric("FY Revenue ($M)", "not found")

# 2. Net Income
if r_last["net_income"] and r_first["net_income"]:
    ni_cagr = ((r_last["net_income"] / r_first["net_income"]) ** (1 / 4) - 1) * 100.0
    m2.metric("Net Income ($M)", f"${r_last['net_income']:,.0f}", f"{ni_cagr:+.1f}% 4-Yr CAGR")
else:
    m2.metric("Net Income ($M)", "not found")

# 3. 5-Yr Average ROE
valid_roes = [r["roe"] for r in rows if isinstance(r["roe"], (int, float))]
if valid_roes:
    avg_roe = sum(valid_roes) / len(valid_roes)
    m3.metric("5-Yr Avg ROE", f"{avg_roe:.1f}%", f"{valid_roes[-1] - valid_roes[0]:+.1f}% diff")
else:
    m3.metric("5-Yr Avg ROE", "not known", "Negative/Missing Equity")

# 4. Owner Earnings
if r_last["owner_earnings"] and r_first["owner_earnings"]:
    oe_cagr = ((r_last["owner_earnings"] / r_first["owner_earnings"]) ** (1 / 4) - 1) * 100.0
    m4.metric("Owner Earnings ($M)", f"${r_last['owner_earnings']:,.0f}", f"{oe_cagr:+.1f}% 4-Yr CAGR")
else:
    m4.metric("Owner Earnings ($M)", "not found", "Non-Industrial Tag")

st.write("")

# -----------------------------------------------------------------------------
# Visual Charts Hub
# -----------------------------------------------------------------------------

tab_line, tab_waterfall, tab_roe = st.tabs([
    "📈 Owner Earnings vs. Net Income",
    "💧 Cash Conversion Bridge (OCF vs. CapEx)",
    "🎯 ROE Hurdle Consistency"
])

chart_records = []
for r in rows:
    chart_records.append({
        "Fiscal Year End": r["fy_end"],
        "Revenue ($M)": r["revenue"] if r["revenue"] is not None else np.nan,
        "Net Income ($M)": r["net_income"] if r["net_income"] is not None else np.nan,
        "Operating Cash Flow ($M)": r["operating_cash_flow"] if r["operating_cash_flow"] is not None else np.nan,
        "Capital Spending ($M)": r["capital_spending"] if r["capital_spending"] is not None else np.nan,
        "Owner Earnings ($M)": r["owner_earnings"] if r["owner_earnings"] is not None else np.nan,
        "ROE (%)": r["roe"] if isinstance(r["roe"], (int, float)) else np.nan
    })
chart_df = pd.DataFrame(chart_records).set_index("Fiscal Year End")

with tab_line:
    has_valid_oe = not chart_df["Owner Earnings ($M)"].dropna().empty
    if has_valid_oe:
        st.line_chart(chart_df[["Net Income ($M)", "Owner Earnings ($M)"]])
        st.caption("Comparison of GAAP Net Income vs. Free Cash Flow to Owners (Operating Cash Flow minus Capital Expenditures).")
    else:
        st.line_chart(chart_df[["Net Income ($M)"]])
        st.warning("⚠️ Owner Earnings cannot be charted: CapEx is reported as 'not found' on Form 10-K (typical for banking institutions).")

with tab_waterfall:
    if has_valid_oe:
        st.bar_chart(chart_df[["Operating Cash Flow ($M)", "Capital Spending ($M)", "Owner Earnings ($M)"]])
        st.caption("Cash Generation vs. Reinvestment: Green owner cash flow represents what remains after funding necessary maintenance and growth CapEx.")
    else:
        st.info("Capital expenditure tags are absent on this filing.")

with tab_roe:
    if not chart_df["ROE (%)"].dropna().empty:
        roe_display_df = chart_df[["ROE (%)"]].copy()
        roe_display_df["Buffett 15% Hurdle"] = 15.0
        st.line_chart(roe_display_df)
        st.caption("Annual Return on Equity plotted against Warren Buffett's minimum 15.0% hurdle line.")
    else:
        st.warning("ROE is 'not known' because Stockholders' Equity was zero or negative (e.g., intensive share repurchase programs like Marriott).")

st.write("---")

# -----------------------------------------------------------------------------
# Audited Table & The Three Checks
# -----------------------------------------------------------------------------

st.subheader("📋 Audited Five-Year 10-K Metrics & The Three Checks")

table_data = []
for r in rows:
    table_data.append({
        "FY End": r["fy_end"],
        "Revenue ($M)": f"{r['revenue']:,.0f}" if r['revenue'] is not None else "not found",
        "Net Income ($M)": f"{r['net_income']:,.0f}" if r['net_income'] is not None else "not found",
        "Oper Cash ($M)": f"{r['operating_cash_flow']:,.0f}" if r['operating_cash_flow'] is not None else "not found",
        "CapEx ($M)": f"{r['capital_spending']:,.0f}" if r['capital_spending'] is not None else "not found",
        "Equity ($M)": f"{r['equity']:,.0f}" if r['equity'] is not None else "not found",
        "ROE %": f"{r['roe']:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe']),
        "Owner Earnings ($M)": f"{r['owner_earnings']:,.0f}" if r['owner_earnings'] is not None else "not found"
    })

disp_df = pd.DataFrame(table_data)
st.dataframe(disp_df, use_container_width=True)

# Buffett's Three Checks Badges
c1, c2, c3 = st.columns(3)

def check_badge(val: str) -> str:
    if val == "pass":
        return "🟢 PASS (Clear Moat)"
    elif val == "fail":
        return "🔴 FAIL (Did Not Clear)"
    else:
        return "🟡 NOT KNOWN (Missing 10-K Tag)"

with c1:
    st.markdown(r"**Check 1: ROE $\ge$ 15% every year**")
    st.info(check_badge(checks["roe_15_every_year"]))

with c2:
    st.markdown("**Check 2: Owner earnings positive every year**")
    st.info(check_badge(checks["oe_positive_every_year"]))

with c3:
    st.markdown("**Check 3: Owner earnings grew first to last**")
    st.info(check_badge(checks["oe_growth_first_to_last"]))

st.write("---")

# -----------------------------------------------------------------------------
# Anti-Hallucination Scanner & Memo Provenance Chamber
# -----------------------------------------------------------------------------

st.subheader("🛡️ Warren Buffett Investment Memo & Anti-Hallucination Audit")

# Load baseline memo
memo_filename = f"buffett_memo_{ticker_input}.md"
if os.path.exists(memo_filename):
    with open(memo_filename, "r", encoding="utf-8") as f:
        memo_content = f.read()
else:
    memo_content = buffett.generate_buffett_memo(data)
    with open(memo_filename, "w", encoding="utf-8") as f:
        f.write(memo_content)

# Apply Scenario Presets
if provenance_preset == "🚨 Injected Unprinted Numbers (40.0% ROE)":
    memo_content = memo_content.replace(
        "clearing our 15% hurdle every year",
        "clearing our 15% hurdle with a hand-typed peak ROE of 40.0% every year"
    )
elif provenance_preset == "💣 Wall Street Consensus Hype ($915 target, 52x P/E)":
    memo_content += (
        "\n\n### Wall Street Analyst Commentary\n"
        "Consensus price target stands at $915.50 per share with a forward P/E multiple of 52.4x "
        "and forecasted EBITDA margins expanding by 340 basis points."
    )

# Extract ground-truth numbers generated by the script
allowed_numbers = set()
for r in rows:
    for k in ["revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings"]:
        v = r.get(k)
        if v is not None:
            v_int = int(round(v))
            allowed_numbers.add(str(v_int))
            allowed_numbers.add(f"{v_int:,}")
            allowed_numbers.add(f"{v:.0f}")
            allowed_numbers.add(f"{v:.1f}")

    roe = r.get("roe")
    if isinstance(roe, (int, float)):
        allowed_numbers.add(f"{roe:.1f}")
        allowed_numbers.add(f"{roe:.1f}%")
        allowed_numbers.add(f"{int(round(roe))}")
        allowed_numbers.add(f"{int(round(roe))}%")

    fy_end = r.get("fy_end", "")
    for part in fy_end.split("-"):
        allowed_numbers.add(part)

# Permissible standard prompt structural tokens
standard_tokens = {
    "15", "15%", "5", "1", "2", "3", "10", "2020", "2021", "2022", "2023", "2024", "2025", "2026",
    "28", "29", "30", "31", "01", "02", "03", "04", "05", "08", "09", "10", "11", "12"
}
allowed_numbers.update(standard_tokens)

# Regex scan for all numeric citations in memo
number_pattern = re.compile(r'\b\d+(?:,\d+)*(?:\.\d+)?%?\b')
memo_numbers = number_pattern.findall(memo_content)

unprinted_flagged = []
for token in memo_numbers:
    clean_token = token.strip()
    norm_token = clean_token.replace(",", "")
    norm_num_only = norm_token.replace("%", "")
    
    matched = (
        clean_token in allowed_numbers or
        norm_token in allowed_numbers or
        norm_num_only in allowed_numbers
    )
    if not matched:
        unprinted_flagged.append(clean_token)

# Compute Provenance Score
total_numbers = len(memo_numbers)
flagged_count = len(unprinted_flagged)
provenance_pct = int(round(((total_numbers - flagged_count) / max(total_numbers, 1)) * 100))

# Status Display
p_col1, p_col2 = st.columns([1, 3])
with p_col1:
    if flagged_count == 0:
        st.metric("Provenance Score", "100%", "Grounded in SEC 10-K")
    else:
        st.metric("Provenance Score", f"{provenance_pct}%", f"-{flagged_count} Hallucinated", delta_color="inverse")

with p_col2:
    if unprinted_flagged:
        st.error(
            f"🚨 **Hallucination Alert:** Found **{flagged_count} unprinted number(s)** in the memo: "
            f"`{list(set(unprinted_flagged))}`. The script never output these numbers from Form 10-K!"
        )
    else:
        st.success(
            "✅ **100% Provenance Grounding:** Every single number cited below was mathematically "
            "computed by `buffett.py` from SEC EDGAR. Zero LLM hallucinations detected."
        )

# Render memo with visual red badges for unprinted numbers
annotated_memo = memo_content
for unp in set(unprinted_flagged):
    annotated_memo = re.sub(
        rf'\b{re.escape(unp)}\b',
        f'<span style="background-color: #ffcccc; color: #cc0000; padding: 2px 6px; border-radius: 4px; font-weight: bold; border: 1px solid #cc0000;">⚠️ {unp} (FLAGGED: UNPRINTED)</span>',
        annotated_memo
    )

st.markdown(annotated_memo, unsafe_allow_html=True)
