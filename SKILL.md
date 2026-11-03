---
name: warren-buffett
description: >-
  Evaluate a public company using Warren Buffett's quantitative 10-K value investing criteria.
  Use this skill whenever evaluating whether a company is a high-quality franchise to own,
  when running a 10-K fundamental screen for Return on Equity (ROE) and Owner Earnings,
  or when generating a Warren Buffett investment committee memo strictly from SEC EDGAR facts.
---

# Warren Buffett Value Investing Skill

This skill enforces strict quantitative discipline based on Warren Buffett's owner-earnings philosophy.
**The fundamental rule:** Code computes every single number directly from audited SEC EDGAR 10-K filings; the AI model only exercises qualitative business judgment on those computed outputs.

## Procedure & Rules

1. **Ingest Audited 10-K Facts via SEC EDGAR:**
   Execute the bundled python script [`buffett.py`](./buffett.py) for the target ticker:
   ```bash
   python buffett.py <TICKER>
   ```
   - Connects keylessly to SEC EDGAR using `User-Agent: Lucas Timm ltimm@purdue.edu`.
   - Strictly requires `10-K` filings and 1-year flow periods.
   - For duplicate periods across multiple filings, the latest filing date wins.

2. **Metric Definitions & Tag Hierarchy:**
   - **Revenue:** `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues`
   - **Net Income:** `NetIncomeLoss`
   - **Operating Cash Flow:** `NetCashProvidedByUsedInOperatingActivities`
   - **Capital Spending (CapEx):** `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets`
   - **Stockholders' Equity:** `StockholdersEquity`
   - **Return on Equity (ROE):** $\frac{\text{Net Income}}{\text{Year-End Equity}} \times 100\%$
   - **Owner Earnings:** $\text{Operating Cash Flow} - \text{Capital Expenditures}$

3. **Handling Missing / Non-Industrial Data:**
   - If a tag is absent on the filing, mark as `"not found"`. Never invent or estimate an absent line item.
   - If Equity $\le 0$, ROE is designated as `"not known"`.
   - If any required input to a check is missing, the check outcome is `"not known"`.

4. **Buffett's Three Quantitative Checks (Computed in Code):**
   - **Check 1:** ROE $\ge 15.0\%$ every year for 5 consecutive fiscal years.
   - **Check 2:** Owner Earnings positive every year for 5 consecutive fiscal years.
   - **Check 3:** Owner Earnings grew from the first fiscal year to the last fiscal year.

5. **Generate the Warren Buffett Memo:**
   - The AI writes a formal memo as Warren Buffett adopting one of three stances:
     - **OWN THE BUSINESS:** Clears all three checks with proven economic moat.
     - **WATCH IT:** High ROE franchise but owner earnings are unmeasurable (e.g. banks) or cyclical.
     - **PASS:** Structural failure of ROE or owner earnings checks.
   - **Anti-Hallucination Mandate:** The memo may **ONLY** cite numbers that were explicitly output by the script. Never cite unprinted share prices, valuations, or external estimates.

