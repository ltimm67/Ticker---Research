---
name: michael-burry
description: >-
  Evaluate a public company using Michael Burry's forensic cash-flow quality and balance-sheet leverage criteria.
  Use this skill when auditing earnings quality against operating cash flow, testing debt solvency via total liabilities to equity,
  and detecting accounting manipulation or excessive leverage strictly from SEC EDGAR facts.
---

# Michael Burry Forensic Cash Flow & Leverage Skill

This skill enforces strict quantitative discipline based on Michael Burry's Scion Capital forensic investing framework.
**The fundamental rule:** Code computes every single number directly from audited SEC EDGAR 10-K filings; the AI model only exercises qualitative business judgment on those computed outputs.

## Procedure & Rules

1. **Ingest Audited 10-K Facts via SEC EDGAR:**
   Execute the bundled python script [`panel.py`](../../panel.py) for the target ticker:
   ```bash
   python panel.py <TICKER>
   ```
   - Connects keylessly to SEC EDGAR using `User-Agent: Lucas Timm ltimm@purdue.edu`.
   - Strictly requires Form `10-K` filings and 1-year flow periods.
   - For duplicate periods across multiple filings, the latest filing date wins.

2. **Metric Definitions & Tag Hierarchy:**
   - **Operating Cash Flow:** `NetCashProvidedByUsedInOperatingActivities`
   - **Net Income:** `NetIncomeLoss`
   - **Total Liabilities:** `Liabilities`
   - **Stockholders' Equity:** `StockholdersEquity`
   - **Liabilities Ã· Equity:** $\text{Liabilities} \div \text{StockholdersEquity}$

3. **Handling Missing / Non-Industrial Data:**
   - If a tag is absent on the filing, mark as `"not found"`. Never invent or estimate an absent line item.
   - If `StockholdersEquity` $\le 0$, $\text{Liabilities} \div \text{Equity}$ is designated as `"not known"`.
   - If `Liabilities` is missing from the 10-K XBRL tags, $\text{Liabilities} \div \text{Equity}$ is `"not known"` and the leverage check outputs `"not known"`.
   - If any required input to a check is missing, the check outcome is `"not known"`.

4. **Burry's Two Quantitative Checks (Computed in Code):**
   - **Check 1: Forensic Cash Flow Quality:**
     Operating Cash Flow $\ge$ Net Income ($\text{OCF} \ge \text{NI}$) for every single one of the 5 consecutive fiscal years.
     *Rationale:* Accrual accounting can be manipulated to inflate net income; true economic solvency requires real operational cash generation to equal or exceed reported earnings.
   - **Check 2: Solvency & Balance Sheet Leverage:**
     $\text{Liabilities} \div \text{Equity} \le 2.0$ in the most recent fiscal year.
     *Rationale:* Excessive corporate indebtedness creates existential distress during macro liquidity crunches.

5. **Generate the Michael Burry Memo:**
   - The AI writes a formal memo as Michael Burry adopting one of three stances:
     - **BULLISH / OWN:** Passes both tests; cash flow quality is pristine ($OCF \ge NI$ across all 5 years) and liabilities are well below twice equity.
     - **WATCH / HEDGE:** Passes cash flow quality but leverage is elevated, or debt metrics are unmeasurable / missing.
     - **BEARISH / PASS / SHORT CANDIDATE:** OCF consistently lags net income (aggressive accruals/working capital burn) or balance sheet liabilities exceed twice equity.
   - **Anti-Hallucination Mandate:** The memo may **ONLY** cite numbers that were explicitly output by the script. Never cite unprinted share prices, valuations, or external estimates.
