# Lab 09 — Pro-Forma Build: The Engine and the Known Answer (Asbury Case)

**Course:** FIN 43900 — AI Finance Applications  
**Company:** Asbury Automotive Group, Inc. (NYSE: ABG)  
**Valuation Date:** Base year FY2025; Five-Year Explicit Forecast FY2026E–FY2030E  
**Engine Script:** [`proforma.py`](proforma.py)  

---

## 1. D: The Central Question & Foundation

> **Central Question:**  
> *"What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?"*

### The Three Judgments That Carry the ABG Valuation
1. **Organic Revenue Growth (1.8% annually):**
   - Anchors top-line expansion across vehicle sales, parts/service, and F&I. Because automotive retail is mature and cyclical, 1.8% represents modest, defensible long-run GDP-like unit growth, expanding revenue from \$17,999.0M to \$19,678.3M by 2030.
2. **Gross Margin (17.05%):**
   - High-volume dealership vehicle retail operates on thin vehicle margins, stabilized by high-margin parts and warranty/customer service absorption. A 50 bps shift in gross margin swings annual gross profit by ~\$90M–\$100M, directly impacting operating profit and cash flow.
3. **SG&A ÷ Gross Profit Operating Leverage (66.5% \(\rightarrow\) 64.5%):**
   - Asbury's efficiency trajectory assumes operating leverage post-acquisition, improving from 66.5% in 2026 to 64.5% by 2028–2030. This expands operating income from \$844.2M to \$971.4M, driving the expansion of FCFE.

### Why Cash Is the Last Line the Model Computes
Cash is the ultimate residual buffer (the balance sheet "plug") of the business. Every operational decision (revenue, cost of goods, SG&A), capital investment (capex, inventory build), and financing decision (debt repayment, floor plan changes, interest, share buybacks) either produces or drains liquidity. 

Cash cannot be independently estimated; it must equal:
$$\text{Ending Cash} = \text{Opening Cash} + \text{FCFE} - \text{Share Buybacks} \pm \text{Revolver Activity}$$
Computing cash last guarantees that the balance sheet balances dynamically with zero arbitrary plug.

---

## 2. R: Model Assumptions & Opening Balance Sheet

### Assumption Set

| Assumption Parameter | Value / Formula | Classification | Economic Rationale |
|---|---|---|---|
| **Organic Revenue Growth** | 1.8% a year (`0.018`) | Judgment | Mature automotive retail unit growth |
| **Gross Margin** | 17.05% (`0.1705`) | Judgment | Vehicle sales + parts/service absorption |
| **SG&A ÷ Gross Profit** | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | Judgment | Operating leverage & post-acquisition integration |
| **Depreciation ÷ Opening PP&E** | 82.4 ÷ 3,070.4 (2.6837%) | History | FY2025 depreciation ÷ year-end PP&E |
| **Impairment (Non-Cash)** | \$120.0M a year | Judgment | Ongoing franchise/goodwill amortization & non-cash write-downs |
| **Capital Expenditures (Capex)** | \$250.0M a year | Guidance | Dealership facility image upgrades & IT infrastructure |
| **Tax Rate** | 25.5% (`0.255`) | Judgment | US federal statutory (21%) + blended state taxes |
| **Inventory Days** | 2,135.8 ÷ (17,999.0 − 3,071.7) × 365 = **52.22 days** | History | FY2025 inventory ÷ cost of sales × 365 |
| **Floor Plan Loans ÷ Inventory** | 2,027.0 ÷ 2,135.8 = **94.9059%** | History | FY2025 captive manufacturer inventory financing ratio |
| **Other Working Capital** | 0.8% of \(\Delta \text{Revenue}\) | Judgment | Receivables/prepaids net of trade payables |
| **Minimum Cash / Limit / Rate** | \$25.0M / \$850.0M / 6.0% | History / Judgment | Operating liquidity buffer and revolving credit facility |
| **Debt Repayment / Share Buybacks** | \$150.0M / \$150.0M a year | Judgment | Balanced capital return: de-leveraging + share cannibalization |
| **Interest Rates: Floor Plan / Debt** | 4.67% / 5.44% | History | FY2025 weighted average effective borrowing rates |
| **Cost of Equity / Terminal Growth** | 10.0% / 2.5% | Judgment | Discount rate and long-run sustainable GDP growth rate |
| **Diluted Shares Outstanding** | 17.951349M | Fact | SEC Form 10-Q as of June 30, 2026 |

### Opening Balance Sheet (FY2025, USD Millions)
- **Assets:** Cash \$40.4M + Inventory \$2,135.8M + PP&E \$3,070.4M + Other Assets \$6,371.6M = **Total Assets \$11,618.2M**
- **Liabilities & Equity:** Floor Plan \$2,027.0M + Term Debt \$3,572.0M + Other Liabilities \$2,127.5M + Equity \$3,891.7M = **Total Liabilities & Equity \$11,618.2M**
- **Balance Check:** \(\text{Assets} - \text{Liabilities} - \text{Equity} = \mathbf{0.0M}\)

---

## 3. I & V: Engine Output & Benchmark Validation

Run command:
```bash
python proforma.py
```

### Complete Pro-Forma Output

```text
================================================================================================
1. PRO-FORMA INCOME STATEMENT
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Revenue                                  18323.0     18652.8     18988.5     19330.3     19678.3
Gross profit                              3124.1      3180.3      3237.5      3295.8      3355.1
SG&A expense                              2077.5      2083.1      2088.2      2125.8      2164.1
Depreciation                                82.4        86.9        91.3        95.5        99.7
Impairment (non-cash)                      120.0       120.0       120.0       120.0       120.0
Operating income                           844.2       890.3       938.1       954.5       971.4
Interest expense                           289.0       282.5       276.1       269.7       263.4
Pretax income                              555.2       607.8       661.9       684.8       708.0
Income tax expense                         141.6       155.0       168.8       174.6       180.5
Net income                                 413.6       452.8       493.1       510.1       527.5

================================================================================================
2. PRO-FORMA BALANCE SHEET
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Cash and equivalents                       101.8       206.9       356.6       527.5       719.8
Inventory                                 2174.7      2213.8      2253.7      2294.2      2335.5
Property, plant & equipment               3238.0      3401.1      3559.8      3714.3      3864.6
Other assets                              6254.2      6136.8      6019.5      5902.3      5785.0
Total Assets                             11768.7     11958.6     12189.6     12438.2     12704.9
Floor plan notes payable                  2063.9      2101.0      2138.9      2177.4      2216.5
Term debt                                 3422.0      3272.0      3122.0      2972.0      2822.0
Revolving credit facility                    0.0         0.0         0.0         0.0         0.0
Other liabilities                         2127.5      2127.5      2127.5      2127.5      2127.5
Total Liabilities                         7613.4      7500.5      7388.4      7276.9      7166.0
Common Equity                             4155.3      4458.1      4801.2      5161.4      5538.9
Total Liabilities & Equity               11768.7     11958.6     12189.6     12438.2     12704.9

================================================================================================
3. PRO-FORMA CASH FLOW & FREE CASH FLOW TO EQUITY (FCFE)
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Net income                                 413.6       452.8       493.1       510.1       527.5
Depreciation                                82.4        86.9        91.3        95.5        99.7
Impairment (non-cash)                      120.0       120.0       120.0       120.0       120.0
Capital expenditures (Capex)               250.0       250.0       250.0       250.0       250.0
Change in inventory                         38.9        39.1        39.8        40.6        41.3
Change in other working capital              2.6         2.6         2.7         2.7         2.8
Change in floor plan notes                  36.9        37.1        37.8        38.5        39.2
Term debt repayment                        150.0       150.0       150.0       150.0       150.0
Free cash flow to equity (FCFE)            211.4       255.1       299.7       320.9       342.3
Share buybacks                             150.0       150.0       150.0       150.0       150.0
Revolver draw / (repayment)                  0.0         0.0         0.0         0.0         0.0
Cash, year end                             101.8       206.9       356.6       527.5       719.8

================================================================================================
4. BALANCE SHEET INTEGRITY & CASH CHECKS
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Assets - liabilities - equity                0.0         0.0         0.0         0.0         0.0
Cash at or above minimum ($25M)               OK          OK          OK          OK          OK

================================================================================================
5. FCFE VALUATION SUMMARY
================================================================================================
PV of explicit FCFE (2026-2030):   $   1059.87M
Normalized terminal base FCFE:      $    492.28M  (2030 FCFE + 2030 repayment)
Terminal value at Year 5 (2030):    $   6727.85M
PV of terminal value:               $   4177.46M
Equity value:                       $   5237.34M
Diluted shares outstanding:           17.951349M
Value per share:                    $    291.75
Share of value after 2030:               79.76%
```

### Benchmark Validation Matrix

| Line Item | Known Benchmark FY2026E | Model Result FY2026E | Known Benchmark FY2030E | Model Result FY2030E | Status |
|---|---|---|---|---|---|
| **Revenue** | 18,323.0 | **18,323.0** | 19,678.3 | **19,678.3** | **Exact match** |
| **Operating Income** | 844.2 | **844.2** | 971.4 | **971.4** | **Exact match** |
| **Net Income** | 413.6 | **413.6** | 527.5 | **527.5** | **Exact match** |
| **Free Cash Flow to Equity (FCFE)** | 211.4 | **211.4** | 342.3 | **342.3** | **Exact match** |
| **Cash, Year End** | 101.8 | **101.8** | 719.8 | **719.8** | **Exact match** |
| **Assets − Liabilities − Equity** | 0.0 | **0.0** | 0.0 | **0.0** | **Exact match** |
| **Value Per Diluted Share** | **\$291.75** | **\$291.75** | — | — | **Exact match** |
| **Terminal Value Share** | ~80% | **79.76%** | — | — | **Exact match** |

---

## 4. Swap and Break: Diagnostic Validation

### The Experiment
To confirm the integrity of `assert_balanced()`, we simulate a broken balance sheet where 2026 ending cash is artificially hardcoded to opening cash (\$40.4M) instead of the computed \$101.8M.

### Resulting Output
```text
AssertionError: Model balance check failed in FY2026E: Assets - Liabilities - Equity gap = -61.4000
```

### Interpretation
- **What the −61.4 tells you before opening a single cell:**
  In FY2026E, net cash generation was `+61.4M` (`FCFE $211.4M − Share buyback $150.0M`).
  Setting cash to \$40.4M understates total assets by exactly \$61.4M.
  The error immediately tells the analyst that balance sheet cash failed to record the net cash flow generated by the cash flow statement, pinpointing the break without needing to trace every line item.

---

## 5. Floor Plan Financing: Deep-Dive Analysis

1. **What is it?**  
   Floor plan financing consists of revolving credit lines extended by automobile manufacturers' captive finance companies (e.g., Ford Credit, Ally, GM Financial) and commercial banks specifically to purchase vehicle inventory. Dealerships pledge the vehicles as collateral.
2. **How does it work?**  
   Floor plan borrowing tracks inventory almost 1:1 (~94.9% of inventory in Asbury's model). As vehicle inventory grows by \$38.9M in 2026, floor plan borrowings automatically rise by \$36.9M. In FCFE, changes in floor plan notes are treated as **operating liabilities** because vehicle retail cannot occur without inventory financing.
3. **Why removing floor plan sends cash to about −\$1.1 billion:**  
   If floor plan financing were removed, Asbury would have to fund over \$2.1 billion of vehicle inventory using its own cash reserves and equity. Without the annual +\$37M to +\$39M floor plan financing offset and bearing the full burden of inventory cash outlays, Asbury’s cash reserves would be completely depleted, plunging cash to approximately **−\$1.1 billion** and maxing out its revolving credit facility.

---

## 6. Reflect & Peer Comparison Connection

### Why FCFE Normalization in Terminal Value Matters
In calculating terminal value:
$$\text{Normalized Base FCFE} = \text{FY2030 FCFE} (\$342.3\text{M}) + \text{FY2030 Debt Repayment} (\$150.0\text{M}) = \mathbf{\$492.3\text{M}}$$
Adding back the \$150.0M debt repayment normalizes terminal cash flow to a **steady-state debt level**. In perpetuity, a mature company maintains a constant target debt-to-capital ratio rather than perpetually paying down \$150M of principal every year until debt is negative.

### Summary
The three-statement pro-forma engine integrates the income statement, balance sheet, and cash flow into a dynamic, balanced model. It matches the known Asbury benchmarks down to the cent, catches accounting breaks dynamically, and prepares the workspace for company-specific pro-forma modeling in Lab 10.

