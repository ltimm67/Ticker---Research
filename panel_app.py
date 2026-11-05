"""
panel_app.py — Interactive Legend Investor Panel Streamlit Application
FIN 43900: Advanced Financial Modeling / AI in Finance (Lab 19)

Displays:
- Panel table: Investor x Check (pass, fail, not known)
- 3 Investor verdicts: Buffett, Graham, Burry
- 5-Year Net Income, Owner Earnings, and OCF trends
- 3 Legend Memos displayed side-by-side
- Universal unprinted-number hallucination scanner
- Graham threshold design choice probe (2.0 vs 1.0)
"""

import streamlit as st
import pandas as pd
import re
from panel import (
    get_company_data,
    evaluate_buffett_checks,
    evaluate_graham_checks,
    evaluate_burry_checks,
    compute_panel_verdicts,
    generate_buffett_memo,
    generate_graham_memo,
    generate_burry_memo,
    extract_printed_numbers,
    find_unprinted_numbers,
)

# -----------------------------------------------------------------------------
# Streamlit App Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Legend Investor Panel (Lab 19)",
    page_icon="🏛️",
    layout="wide",
)

st.markdown("""
<style>
    .stApp { background: #f7f8fc; }
    .hero { padding: 1.5rem 1.8rem; border-radius: 18px; color: #ffffff;
            background: linear-gradient(120deg, #0b1f3a 0%, #153d6f 54%, #1f6f8b 100%); }
    .hero h1 { margin: 0; font-size: 2.25rem; }
    .hero p { margin: .45rem 0 0; opacity: .88; font-size: 1rem; }
    .section-kicker { color: #1f6f8b; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: .75rem; }
    div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e3e8f0; border-radius: 14px;
                                  padding: .85rem; box-shadow: 0 3px 12px rgba(20, 42, 80, .06); }
    .decision-card { background: #fff8e6; border-left: 5px solid #e09f3e; border-radius: 8px; padding: 1rem 1.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>Legend Investor Panel</h1>
  <p>One company. Three investing lenses. Every conclusion traceable to 10-K facts.</p>
</div>
""", unsafe_allow_html=True)
st.caption("SEC EDGAR data • educational demonstration • not investment advice")

# -----------------------------------------------------------------------------
# Sidebar Controls
# -----------------------------------------------------------------------------

st.sidebar.header("Panel Parameters")
ticker = st.sidebar.text_input("Ticker Symbol", value="COST").upper().strip()

st.sidebar.markdown("---")
st.sidebar.subheader("Graham Threshold Probe")
cr_threshold = st.sidebar.radio(
    "Graham Current Ratio Threshold:",
    options=[2.0, 1.0],
    index=0,
    help="Design Choice Probe: Standard Graham rule requires Current Ratio >= 2.0. Lowering to 1.0 accommodates negative working-capital retail models.",
)

st.sidebar.info(
    f"Current Graham Threshold: **{cr_threshold:.1f}**\n\n"
    "• At **2.0**: Costco fails (1.06 < 2.0)\n"
    "• At **1.0**: Costco passes (1.06 >= 1.0)"
)
st.sidebar.markdown("---")
st.sidebar.caption("Tip: use the table filter and CSV download to prepare your checkout evidence.")

# -----------------------------------------------------------------------------
# Data Loading & Engine Computation
# -----------------------------------------------------------------------------

try:
    with st.spinner(f"Extracting 10-K facts for {ticker} from SEC EDGAR..."):
        data = get_company_data(ticker)
except Exception as e:
    st.error(f"Error extracting data for '{ticker}': {e}")
    st.stop()

company_name = data["company_name"]
cik = data["cik"]
rows = data["rows"]

# Run Checks
b_checks = evaluate_buffett_checks(rows)
g_checks = evaluate_graham_checks(rows, cr_threshold=cr_threshold)
m_checks = evaluate_burry_checks(rows)
all_checks = b_checks + g_checks + m_checks
verdicts = compute_panel_verdicts(b_checks, g_checks, m_checks)

# Generate Memos
b_memo = generate_buffett_memo(ticker, data, b_checks)
g_memo = generate_graham_memo(ticker, data, g_checks, cr_threshold=cr_threshold)
m_memo = generate_burry_memo(ticker, data, m_checks)

# Whitelist & Scanner
whitelist = extract_printed_numbers(data, all_checks)

# -----------------------------------------------------------------------------
# Top Overview Cards
# -----------------------------------------------------------------------------

pass_count = sum(c["status"].startswith("pass") for c in all_checks)
fail_count = sum(c["status"].startswith("fail") for c in all_checks)
unknown_count = len(all_checks) - pass_count - fail_count

st.markdown("<div class='section-kicker'>Company under review</div>", unsafe_allow_html=True)
st.markdown(f"### {company_name} &nbsp; `#{ticker}`")
st.caption(f"CIK {cik} • Five fiscal years ending {rows[0]['fy_end']} to {rows[-1]['fy_end']}")

if fail_count == 0 and unknown_count == 0:
    consensus = "UNANIMOUSLY POSITIVE"
    consensus_detail = "Every quantitative check passed."
elif unknown_count:
    consensus = "REQUIRES REVIEW"
    consensus_detail = f"{unknown_count} check(s) remain not known; do not replace gaps with estimates."
else:
    consensus = "SPLIT PANEL"
    consensus_detail = f"{fail_count} check(s) failed across the three lenses."

st.info(f"**Panel signal: {consensus}** — {consensus_detail}")

c1, c2, c3, c4 = st.columns(4)

def verdict_color(v):
    if "OWN" in v or "BUY" in v:
        return "green"
    elif "WATCH" in v or "HEDGE" in v:
        return "orange"
    else:
        return "red"

with c1:
    b_v = verdicts["Buffett"]["verdict"]
    st.metric("Warren Buffett", b_v, f"{verdicts['Buffett']['score']} Checks Passed")

with c2:
    g_v = verdicts["Graham"]["verdict"]
    st.metric("Benjamin Graham", g_v, f"{verdicts['Graham']['score']} Checks Passed (CR >= {cr_threshold:.1f})")

with c3:
    m_v = verdicts["Burry"]["verdict"]
    st.metric("Michael Burry", m_v, f"{verdicts['Burry']['score']} Checks Passed")

with c4:
    st.metric("Panel Checks", f"{pass_count}/{len(all_checks)} pass", f"{fail_count} fail • {unknown_count} unknown")

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 1: The Panel Table (Investor x Check)
# -----------------------------------------------------------------------------

st.markdown("<div class='section-kicker'>The scorecard</div>", unsafe_allow_html=True)
st.subheader("📋 The Legend Panel Table")
st.markdown("Code-computed evaluation across all three investor rules. Filter for only the points that need discussion.")

panel_data = []
for c in all_checks:
    status_str = c["status"]
    if status_str.startswith("pass"):
        badge = "✅ PASS"
    elif status_str.startswith("fail"):
        badge = "❌ FAIL"
    else:
        badge = "⚠️ NOT KNOWN"
    
    panel_data.append({
        "Investor": c["investor"],
        "Check Description": c["check"],
        "Result": badge,
        "Detail / Value": status_str,
    })

panel_df = pd.DataFrame(panel_data)
table_filter = st.radio("Show", ["All checks", "Fails and unknowns only"], horizontal=True)
visible_panel_df = panel_df if table_filter == "All checks" else panel_df[~panel_df["Result"].str.contains("PASS")]
st.dataframe(visible_panel_df, width="stretch", hide_index=True)
st.download_button(
    "Download panel results (CSV)",
    panel_df.to_csv(index=False).encode("utf-8"),
    file_name=f"{ticker}_legend_panel.csv",
    mime="text/csv",
)

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 2: 5-Year Financial Trend Chart & Tables
# -----------------------------------------------------------------------------

st.markdown("<div class='section-kicker'>The evidence</div>", unsafe_allow_html=True)
st.subheader("📊 5-Year 10-K Fundamentals & Ratios")

# Chart Data
chart_data = []
for r in rows:
    chart_data.append({
        "Fiscal Year End": r["fy_end"],
        "Net Income ($M)": r["net_income"] if isinstance(r["net_income"], (int, float)) else None,
        "Operating Cash Flow ($M)": r["operating_cash_flow"] if isinstance(r["operating_cash_flow"], (int, float)) else None,
        "Owner Earnings ($M)": r["owner_earnings"] if isinstance(r["owner_earnings"], (int, float)) else None,
    })
chart_df = pd.DataFrame(chart_data).set_index("Fiscal Year End")

tab1, tab2, tab3 = st.tabs(["📈 Cash Flow & Earnings Chart", "📑 Core 10-K Facts Table", "⚖️ Working Capital & Solvency Table"])

with tab1:
    st.line_chart(chart_df, height=350)
    st.caption("Comparison of Net Income, Operating Cash Flow, and Owner Earnings (OCF - CapEx).")

with tab2:
    fact_rows = []
    for r in rows:
        fact_rows.append({
            "FY End Date": r["fy_end"],
            "Revenue ($M)": f"${r['revenue']:,.1f}" if isinstance(r["revenue"], (int, float)) else str(r["revenue"]),
            "Net Income ($M)": f"${r['net_income']:,.1f}" if isinstance(r["net_income"], (int, float)) else str(r["net_income"]),
            "Operating Cash ($M)": f"${r['operating_cash_flow']:,.1f}" if isinstance(r["operating_cash_flow"], (int, float)) else str(r["operating_cash_flow"]),
            "CapEx ($M)": f"${r['capital_spending']:,.1f}" if isinstance(r["capital_spending"], (int, float)) else str(r["capital_spending"]),
            "Equity ($M)": f"${r['equity']:,.1f}" if isinstance(r["equity"], (int, float)) else str(r["equity"]),
            "ROE %": f"{r['roe']:.1f}%" if isinstance(r["roe"], (int, float)) else str(r["roe"]),
            "Owner Earnings ($M)": f"${r['owner_earnings']:,.1f}" if isinstance(r["owner_earnings"], (int, float)) else str(r["owner_earnings"]),
        })
    st.table(pd.DataFrame(fact_rows))

with tab3:
    solv_rows = []
    for r in rows:
        solv_rows.append({
            "FY End Date": r["fy_end"],
            "Current Assets ($M)": f"${r['assets_current']:,.1f}" if isinstance(r["assets_current"], (int, float)) else str(r["assets_current"]),
            "Current Liabilities ($M)": f"${r['liabilities_current']:,.1f}" if isinstance(r["liabilities_current"], (int, float)) else str(r["liabilities_current"]),
            "Current Ratio": f"{r['current_ratio']:.2f}" if isinstance(r["current_ratio"], (int, float)) else str(r["current_ratio"]),
            "Total Liabilities ($M)": f"${r['liabilities']:,.1f}" if isinstance(r["liabilities"], (int, float)) else str(r["liabilities"]),
            "Liabilities / Equity": f"{r['liabilities_equity']:.2f}" if isinstance(r["liabilities_equity"], (int, float)) else str(r["liabilities_equity"]),
        })
    st.table(pd.DataFrame(solv_rows))

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 3: Universal Unprinted-Number Flag Across All Memos
# -----------------------------------------------------------------------------

st.markdown("<div class='section-kicker'>Trust check</div>", unsafe_allow_html=True)
st.subheader("🛡️ Provenance & Anti-Hallucination Audit")

memos_dict = {
    "Warren Buffett": b_memo,
    "Benjamin Graham": g_memo,
    "Michael Burry": m_memo,
}

total_unprinted = 0
unprinted_by_memo = {}

for name, m_text in memos_dict.items():
    unprinted = find_unprinted_numbers(m_text, whitelist)
    unprinted_by_memo[name] = unprinted
    total_unprinted += len(unprinted)

if total_unprinted == 0:
    st.success(
        "✅ **Universal Anti-Hallucination Audit Passed:** All three legend memos cite strictly verified numbers "
        "computed by code from SEC EDGAR Form 10-K filings. Exactly 0 unprinted numbers detected across the entire panel."
    )
else:
    st.error(
        f"🚨 **Hallucination Alert:** {total_unprinted} unprinted number(s) detected across legend memos!"
    )
    for name, unprinted in unprinted_by_memo.items():
        if unprinted:
            st.warning(f"• **{name} Memo:** Unprinted numbers flagged: `{', '.join(unprinted)}`")

# Interactive Live Provenance Probe
with st.expander("🧪 Test Live Provenance Flagger with Custom Text"):
    sample_probe = st.text_area(
        "Paste text to test against the 10-K printed number whitelist:",
        value=f"Costco's membership renewal rate is 90.5% and shares trade at $925.",
        height=80,
    )
    if sample_probe:
        probe_flags = find_unprinted_numbers(sample_probe, whitelist)
        if probe_flags:
            st.markdown(
                f"<span style='color:red; font-weight:bold;'>⚠️ FLAGGED UNPRINTED NUMBERS:</span> "
                + " ".join([f"<mark style='background-color: #ffcccc;'>{f}</mark>" for f in probe_flags]),
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<span style='color:green;'>✅ All numbers in test text match printed 10-K data.</span>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 4: Three Memos Side by Side
# -----------------------------------------------------------------------------

st.markdown("<div class='section-kicker'>The investment committee</div>", unsafe_allow_html=True)
st.subheader("📝 Legend Investment Committee Memos (Side by Side)")

col_b, col_g, col_m = st.columns(3)

def highlight_memo(text, unprinted_list):
    """Highlight unprinted numbers in red if any exist."""
    res = text
    for num in unprinted_list:
        res = re.sub(rf"\b({re.escape(num)})\b", r" :red[**⚠️ \1 (FLAGGED: UNPRINTED)**] ", res)
    return res

with col_b:
    st.markdown("### 🎩 Warren Buffett")
    st.markdown(highlight_memo(b_memo, unprinted_by_memo["Warren Buffett"]))

with col_g:
    st.markdown("### 👓 Benjamin Graham")
    st.markdown(highlight_memo(g_memo, unprinted_by_memo["Benjamin Graham"]))

with col_m:
    st.markdown("### 🩺 Michael Burry")
    st.markdown(highlight_memo(m_memo, unprinted_by_memo["Michael Burry"]))

st.markdown("---")

# -----------------------------------------------------------------------------
# Section 5: Decision & Partner Debate
# -----------------------------------------------------------------------------

st.markdown("<div class='section-kicker'>Decision discipline</div>", unsafe_allow_html=True)
st.subheader("⚖️ Panel Decision & Defense")
st.markdown("""
<div class="decision-card">
<strong>Only with a condition.</strong> Use the panel as a first quantitative screen only when business-model-specific thresholds are documented and missing balance-sheet tags trigger a forensic SEC footnote cross-check—not a guess or automatic rejection.
</div>
""", unsafe_allow_html=True)

with st.expander("How to explain the split to a partner"):
    st.markdown(
        f"**Agreement:** {pass_count} of {len(all_checks)} checks passed.  \\n+**Disagreement / gaps:** {fail_count} failed and {unknown_count} are not known.  \\n+**Threshold lesson:** changing Graham's current-ratio cutoff from 2.0 to 1.0 can change a verdict without changing a single 10-K fact."
    )
