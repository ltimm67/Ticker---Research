---
name: ben-graham
description: >-
  Evaluate a public company using Benjamin Graham's conservative balance-sheet and margin-of-safety criteria.
  Use this skill when assessing working-capital adequacy via the current ratio, multi-year net income stability,
  and determining whether a business passes Graham's defensive investor rules strictly from SEC EDGAR facts.
---

# Benjamin Graham Defensive Value Investing Skill

This skill enforces strict quantitative discipline based on Benjamin Graham's margin-of-safety and balance-sheet solvency principles from *The Intelligent Investor* and *Security Analysis*.
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
   - **Current Assets:** `AssetsCurrent`
   - **Current Liabilities:** `LiabilitiesCurrent`
   - **Current Ratio:** $\text{AssetsCurrent} \div \text{LiabilitiesCurrent}$
   - **Net Income:** `NetIncomeLoss`
   - **Revenue:** `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues`
   - **Stockholders' Equity:** `StockholdersEquity`

3. **Handling Missing / Non-Industrial Data:**
   - If a tag is absent on the filing, mark as `"not found"`. Never invent or estimate an absent line item.
   - If `AssetsCurrent` or `LiabilitiesCurrent` is missing, Current Ratio is `"not found"` and the current-ratio check outputs `"not known"`.
   - If any required input to a check is missing, the check outcome is `"not known"`.

4. **Graham's Three Quantitative Checks (Computed in Code):**
   - **Check 1: Working Capital Buffer (Current Ratio):**
     $\text{Current Ratio} \ge 2.0$ in the most recent fiscal year.
     *Probe Note:* A threshold of 2.0 reflects Graham's industrial-era margin of safety. If probed at 1.0 (for negative-working-capital retail models), record the chosen threshold and rationale.
   - **Check 2: Positive Earnings Record:**
     Net income $> 0$ in each of the last 5 consecutive fiscal years (no deficit years).
   - **Check 3: Earnings Growth:**
     Net income in the latest fiscal year $>$ Net income in the first fiscal year ($NI_{\text{latest}} > NI_{\text{first}}$).

5. **Generate the Benjamin Graham Memo:**
   - The AI writes a formal memo as Benjamin Graham adopting one of three stances:
     - **DEFENSIVE BUY / SATISFACTORY:** Passes all three quantitative tests with adequate working-capital cushion.
     - **WATCH:** Strong earnings record and growth, but fails working-capital threshold (e.g. current ratio between 1.0 and 2.0).
     - **PASS / UNSATISFACTORY:** Structural deficit year (negative net income) or deteriorating multi-year profitability.
   - **Anti-Hallucination Mandate:** The memo may **ONLY** cite numbers that were explicitly output by the script. Never cite unprinted share prices, valuations, or external estimates.
