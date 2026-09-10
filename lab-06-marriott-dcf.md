# Lab 06: Marriott International (NASDAQ: MAR) Valuation and Reverse DCF

**Company:** Marriott International, Inc. (NASDAQ: MAR)  
**Valuation date / target price quote:** September 10, 2026, 1:45 PM EDT  
**Current share price (reverse-DCF target):** $335.50  
**Primary SEC filing:** [2025 Form 10-K (SEC EDGAR, Accession No. 0001048286-26-000007)](https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm)

---

## Section R: Marriott Sourced Model Inputs

| Input parameter | Value | Unit | As-of date | Exact locator and methodology | Source type |
|---|---:|---|---|---|---|
| **Starting FCFF** | 3,111.0 | USD millions | FY ended Dec. 31, 2025 | 2025 Form 10-K, Consolidated Statements of Cash Flows. Operating cash flow ($3,212M) + after-tax interest paid (approximately $503M = $645M × 78%) - capital expenditures ($604M). Base FCF without the interest addback is $2,608M. | Sourced / calculated |
| **Growth, Years 1-5** | 6.0%, 5.5%, 5.0%, 4.5%, 4.0% | Annual growth | 2026-2030 forecast | 2025 Form 10-K, Item 7 MD&A, and Q2 2026 earnings release. Forecast is anchored to net rooms growth guidance of 4.5%-5.0%, RevPAR growth of 3.0%-3.5%, and fee operating leverage, with growth declining toward the terminal rate. | Labeled forecast |
| **WACC** | 8.9% | Annual rate | Sept. 10, 2026 | Cost of equity = 9.75% (4.0% risk-free rate + 1.15 beta × 5.0% equity risk premium). After-tax cost of debt = 4.06% (5.2% coupon × 78%). Capital structure weights: 85.0% equity ($91.8B market cap) and 15.0% debt ($16.2B). WACC = 0.85 × 9.75% + 0.15 × 4.06% = 8.90%. | Labeled estimate |
| **Terminal growth** | 2.5% | Annual rate | Perpetual | Long-run sustainable macroeconomic growth estimate, rather than a company-specific growth rate. | Labeled estimate |
| **Cash** | 385.0 | USD millions | Dec. 31, 2025 | 2025 Form 10-K, Consolidated Balance Sheets, “Cash and equivalents.” Q2 2026 cash was approximately $500M. | Sourced |
| **Debt** | 16,211.0 | USD millions | Dec. 31, 2025 | 2025 Form 10-K, Consolidated Balance Sheets: current portion of long-term debt ($1,550M) plus senior notes and other long-term debt ($14,661M). Q2 2026 debt was approximately $16,900M. | Sourced |
| **Diluted shares** | 273.6 | Millions of shares | FY ended Dec. 31, 2025 | 2025 Form 10-K, Consolidated Statements of Income and Note 3, Earnings Per Share. | Sourced |

---

## Training-Case Verification

Before using Marriott’s inputs, I verified `dcf.py` using the class training inputs.

- **Twelve known outputs:** All twelve lines matched the class answers to four decimals, including a value per diluted share of **$27.50**.
- **Sensitivity grid:** The grid matched cell-for-cell, with the base case in the center.
- **Reverse DCF practice run:** The solved shift at a $30.00 target price was **+1.78 percentage points**, exactly matching the expected class result.

---

## Section I: Marriott Through the Model

Running `python dcf.py` with Marriott’s inputs produced:

```text
FCFF Year 1: 3,297.6600
FCFF Year 2: 3,479.0313
FCFF Year 3: 3,652.9829
FCFF Year 4: 3,817.3671
FCFF Year 5: 3,970.0618
Present value of the explicit FCFF: 14,096.7190
Terminal value at Year 5: 63,583.0207
Present value of the terminal value: 41,514.6860
Enterprise value: 55,611.4050
Equity value: 39,785.4050
Value per diluted share: 145.4145
Present value of the terminal value as a share of enterprise value: 0.7465 (74.65%)
```

---

## Section V: Reasonableness Check

- **Model value per diluted share:** **$145.41**
- **Current market share price:** **$335.50**
- **Model value / market price:** **0.43x**
- **Assessment:** The model value is outside the 0.5x to 2.0x reasonableness band.
- **Action taken:** Per the assignment instructions, no inputs were adjusted simply to force the valuation into the reasonableness band.

### Input most open to question

The most questionable assumptions are the **starting FCFF and explicit growth rates**.

Marriott’s asset-light franchising and licensing model requires relatively little capital expenditure and can generate substantial cash flow. The base growth assumptions of 4%-6% reflect room expansion and RevPAR trends, but they may not fully capture potential fee-margin improvement or stronger-than-expected international growth. That said, the model holds diluted shares constant, so the potential benefit of future share repurchases is not directly reflected in this FCFF valuation.

---

## Section E: Sensitivity Grid and Reverse DCF

### Sensitivity Grid: Value per Diluted Share

```text
WACC \ Terminal Growth        2.0%      2.5%      3.0%
7.9%                         166.61    183.42    203.64
8.9%                         133.73    145.41    159.08
9.9%                         109.19    117.69    127.43
```

- **Base case:** $145.41 at an 8.9% WACC and 2.5% terminal growth rate.
- **Direction check:** Value falls as WACC rises and increases as terminal growth rises.
- **Four-corners range:** $109.19 to $203.64.

### Reverse DCF: Market Expectations

```text
Target share price: $335.50
Inputs held fixed:
  Starting FCFF: 3,111.0000 USD Millions
  Base growth rates: ['6.00%', '5.50%', '5.00%', '4.50%', '4.00%']
  WACC: 8.90%
  Terminal growth: 2.50%
  Cash: 385.0000 USD Millions
  Debt: 16,211.0000 USD Millions
  Diluted shares: 273.60 Millions

Solved uniform growth rate shift: +16.37 percentage points (+0.1637)
Implied explicit growth rates: ['22.37%', '21.87%', '21.37%', '20.87%', '20.37%']
```

**Finding:** At a share price of **$335.50**, with capital structure, WACC, terminal growth, cash, debt, and share count held constant, Marriott’s FCFF would need to grow by roughly **21%-22% annually for the next five years**. That is about **16.4 percentage points above the base forecast**.

**Interpretation:** Put simply, the current market price reflects expectations far above modest organic lodging growth. Within this model, it requires substantial and sustained growth in Marriott’s fee business, international operations, and cash-generation capacity. Because the model holds share count fixed, future buybacks are not a direct source of the implied FCFF growth.

---

## Conditional Call

**Recommendation: Watch and defer.** I would wait rather than initiate at the current price. A more attractive entry point would be a share price below approximately **$210**, where the reverse-DCF gap would move closer to the base-case forecast. Alternatively, I would reconsider if Marriott reports a verified acceleration in high-margin international royalty fees that supports FCFF growth above 15% over time.

**What to monitor:** Net additions to the rooms pipeline and net fee-revenue margin in the next quarterly earnings release.