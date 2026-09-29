# Lab 11 — Pro-Forma Sensitivity: Find Your Company's Drivers
**Course:** FIN 43900 — Advanced Financial Modeling / AI in Finance (Fall 2026)  
**Company:** Marriott International, Inc. (NASDAQ: MAR)  
**Deliverable File:** [`lab-11-marriott-sensitivity.md`](file:///c:/tmp/ai-finance-work/lab-11-marriott-sensitivity.md)  
**Model Engine:** [`proforma_mar.py`](file:///c:/tmp/ai-finance-work/proforma_mar.py)  

---

## 1. Executive Summary & Core Results

Over a symmetric **\(\pm 2.0\text{ percentage point}\)** tested range on independent operating assumptions:
1. **Value & Cash Flow Driver:** **Net Operating Fee Margin** is the dominant driver of Free Cash Flow to Equity (FCFE) and equity value. A \(\pm 2.0\text{ pp}\) shift in fee margin creates an equity value span of **\$45.69 per share** (\$151.32 to \$197.01) and a 2030 FCFE span of **\$894.7M**, compared to **\$36.30 per share** and **\$801.2M** for organic revenue growth.
2. **Operating Profit Driver:** **Organic Revenue Growth** creates a slightly larger 2030 Operating Income span (**\$1,134.5M** vs. **\$1,109.5M**) because top-line growth compounds geometrically over five years (\((1.065)^5\) vs \((1.025)^5\)).
3. **Working Capital Drag:** Revenue growth requires incremental operating current assets (receivables and contract advances), creating a cash flow drag. In contrast, fee margin expansion flows 100% to gross profit with zero incremental working capital requirements, driving higher cash conversion.
4. **Model Balance Integrity:** All lower, base, and higher runs balanced dynamically (`Assets - Liabilities - Equity = 0.0000`). The restored base check matched the initial base run to 0.0000 decimal places.

---

## 2. Partner Exchange 1 — Predict, Then Question

### Student Explanation to Partner (Prior to Model Execution)
> *"I expect **Net Operating Fee Margin** to matter more than **Organic Revenue Growth** for Marriott's valuation over comparable percentage-point ranges. Because Marriott runs an asset-light brand licensing model, ~\$19.1B of its \$26.2B revenue is pass-through reimbursed expense with zero margin. Expanding the fee margin on the entire revenue base impacts the bottom line immediately in Year 1 without requiring additional working capital, whereas revenue growth must compound over several years and ties up cash in receivables."*

### Partner Question Received
> *"What evidence from Marriott's actual filings supports testing a \(\pm 2.0\text{ percentage point}\) range for both organic growth (2.5% to 6.5%) and fee margin (19.44% to 23.44%), and are they truly independent?"*

### Student Response
> *"Both ranges reflect Marriott's historical cycles across the last three 10-Ks. For revenue growth, 2.5% mirrors the post-pandemic normalization where comparable RevPAR slowed to 2.0% in 2025, while 6.5% reflects periods of international leisure surges and accelerated room additions from Marriott's 570,000-room pipeline. For fee margin, 19.44% reflects margin dilution from owner incentive concessions during lodging downturns, while 23.44% reflects high-margin co-branded credit card fee expansion (growing double digits per Note 3). They are independent inputs because fee margin represents contractual take-rate, whereas growth represents system room count and travel volume."*

### Check Performed on Partner's Model
> *"I reviewed my partner's model setup. I confirmed that their two chosen drivers were independent operating assumptions (unit volume and unit price) rather than calculated statement line items. I verified their input units (dollars vs. percentages) and confirmed that only one variable was shifted at a time while all other assumptions remained anchored to base."*

---

## 3. D — The Question

> **Which assumptions drive my company's forecast and value, and what explains their effects?**

For Marriott, the forecast and intrinsic value are driven primarily by:
1. **Net Operating Fee Margin (Take-Rate):** Dictates how much high-margin fee revenue Marriott retains from its \$26B+ system revenues.
2. **Organic Revenue Growth (RevPAR + Room Growth):** Dictates the pace at which the underlying system room base expands.
3. **The Terminal Value Spread (\(r - g\)):** Dictates the capitalization of normalized 2030 FCFE into perpetuity.

---

## 4. R — Chosen Inputs, Comparison Outputs & Locked Record

### The Two Operating Drivers

| Driver Name | Model Variable | Units | Base Value | Tested Range (Lower \(\rightarrow\) Higher) | Affected Forecast Years | Filing / Analytical Rationale |
|---|---|:---:|:---:|:---:|:---:|---|
| **Organic Revenue Growth** | `organic_revenue_growth` | `% / yr` | **4.50%** | **2.50% \(\rightarrow\) 6.50%** (\(\pm 2.0\text{ pp}\)) | 2026E – 2030E (All years) | Lower bound (2.5%) reflects recessionary RevPAR contraction (-1.5%) offset by +4.0% net room additions. Higher bound (6.5%) reflects global luxury boom (+2.5% RevPAR) with +4.0% room growth. |
| **Net Operating Fee Margin** | `gross_margin` | `% of rev` | **21.4428%** | **19.4428% \(\rightarrow\) 23.4428%** (\(\pm 2.0\text{ pp}\)) | 2026E – 2030E (All years) | Lower bound reflects franchisee fee relief and third-party OTA commission friction. Higher bound reflects high-margin co-branded credit card fees and luxury tier additions. |

### Standardized Comparison Outputs
1. **Final-Year Operating Profit:** FY2030 Operating Income (USD Millions)
2. **Final-Year Free Cash Flow:** FY2030 Free Cash Flow to Equity (FCFE, USD Millions)
3. **Value Per Diluted Share:** Intrinsic equity value per share (USD / share, valid FCFE discounted model)

---

### Locked Changed-Input Record (Recorded Prior to Sensitivity Runs)
* **Timestamp:** `2026-09-29T13:45:00-04:00`
* **Driver 1 (Organic Revenue Growth):**
  * *Change:* `4.5%` \(\rightarrow\) `2.5%` (Lower) and `4.5%` \(\rightarrow\) `6.5%` (Higher).
  * *Prediction:* Operating profit will move by roughly \(\pm \$500\text{M}\) to \(\$600\text{M}\) in 2030 due to 5-year compounding. Value per share will shift by roughly \(\pm \$15.00\) to \(\$20.00\).
  * *Why:* Compounding growth expands both the fee revenue pool and terminal base cash flow.
* **Driver 2 (Net Operating Fee Margin):**
  * *Change:* `21.4428%` \(\rightarrow\) `19.4428%` (Lower) and `21.4428%` \(\rightarrow\) `23.4428%` (Higher).
  * *Prediction:* 2030 Operating profit will move by roughly \(\pm \$550\text{M}\). Value per share will shift by \(\pm \$20.00\) to \(\$25.00\), having a larger valuation impact than revenue growth.
  * *Why:* Margin expansion begins in Year 1 without expanding working capital assets, delivering immediate, undiscounted cash flow gains.

---

## 5. I & V — Sensitivity Implementation & Complete Visible Terminal Output

Run Command:
```bash
python proforma_mar.py
```

### Complete Terminal Output

```text
================================================================================================
1. PRO-FORMA INCOME STATEMENT: MARRIOTT INTERNATIONAL (MAR)
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Total Revenues                           27364.4     28595.8     29882.6     31227.3     32632.5
Net Operating Fee Margin                  5867.7      6131.7      6407.7      6696.0      6997.3
General & Administrative (SG&A)            909.2       935.1       961.1      1004.4      1049.6
Depreciation & Amortization                604.0       605.1       606.2       607.3       608.5
Operating Income                          4354.5      4591.6      4840.3      5084.3      5339.2
Interest Expense, net                      767.0       752.8       738.6       724.4       710.2
Pretax Income                             3587.5      3838.7      4101.7      4359.8      4629.0
Income Tax Provision                       790.3       845.7       903.6       960.5      1019.8
Net Income                                2797.2      2993.1      3198.1      3399.4      3609.2

================================================================================================
2. PRO-FORMA BALANCE SHEET: MARRIOTT INTERNATIONAL (MAR)
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Cash and cash equivalents                  315.5       439.8       766.8      1292.9      2026.3
Accounts & notes receivable, net          3250.3      3348.8      3451.7      3559.3      3671.7
Merchandise inventory (None)                 0.0         0.0         0.0         0.0         0.0
Property and equipment, net               2312.4      2670.4      3027.9      3384.9      3741.5
Intangibles & other assets               21665.7     21351.9     21039.7     20729.1     20420.2
Total Assets                             27543.9     27810.8     28286.1     28966.2     29859.7
Floor plan loans (None)                      0.0         0.0         0.0         0.0         0.0
Senior notes and term debt               15911.0     15611.0     15311.0     15011.0     14711.0
Revolving credit facility                    0.0         0.0         0.0         0.0         0.0
Other liabilities & loyalty def.         15177.7     15251.6     15328.8     15409.5     15493.8
Total Liabilities                        31088.7     30862.6     30639.8     30420.5     30204.8
Shareholders' Equity (Deficit)           -3544.8     -3051.7     -2353.6     -1454.3      -345.1
Total Liabilities & Equity               27543.9     27810.8     28286.1     28966.2     29859.7

================================================================================================
3. PRO-FORMA CASH FLOW & FREE CASH FLOW TO EQUITY (FCFE)
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Net Income                                2797.2      2993.1      3198.1      3399.4      3609.2
Depreciation & Amortization                604.0       605.1       606.2       607.3       608.5
Capital expenditures (Capex)               600.0       600.0       600.0       600.0       600.0
Change in net working capital               70.7        73.9        77.2        80.7        84.3
Term debt repayment                        300.0       300.0       300.0       300.0       300.0
Free Cash Flow to Equity (FCFE)           2430.5      2624.3      2827.1      3026.0      3233.4
Share repurchases & dividends             2500.0      2500.0      2500.0      2500.0      2500.0
Revolver draw / (repayment)                  0.0         0.0         0.0         0.0         0.0
Cash, year end                             315.5       439.8       766.8      1292.9      2026.3

================================================================================================
4. BALANCE SHEET INTEGRITY & CASH CHECKS
================================================================================================
Line Item (USD Millions)                 FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
------------------------------------------------------------------------------------------------
Assets - liabilities - equity                0.0         0.0         0.0         0.0         0.0
Cash at or above minimum ($300M)              OK          OK          OK          OK          OK

================================================================================================
5. FCFE VALUATION SUMMARY: MARRIOTT INTERNATIONAL (MAR)
================================================================================================
PV of explicit FCFE (2026-2030):   $  10896.52M
Normalized terminal base FCFE:      $   3533.42M  (2030 FCFE + 2030 repayment)
Terminal value at Year 5 (2030):    $  56589.91M
PV of terminal value:               $  36948.74M
Equity value:                       $  47845.26M
Diluted shares outstanding:              273.60M
Value per diluted share:            $    174.87
Share of value after 2030:               77.23%

================================================================================================
6. ONE-AT-A-TIME SENSITIVITY ANALYSIS (LAB 11)
================================================================================================

Driver: Organic Revenue Growth (Unit: % / yr)
Rationale: Range of 2.5% to 6.5% reflects recessionary RevPAR contraction vs. luxury travel boom.
------------------------------------------------------------------------------------------------
Run / CaseInput Value   2030 Op Income    2030 FCFE (FCFE)  Value / Share   Checks  
------------------------------------------------------------------------------------------------
Lower     2.5%          $    4793.7M       $    2846.8M       $  157.32         PASS    
Base      4.5%          $    5339.2M       $    3233.4M       $  174.87         PASS    
Higher    6.5%          $    5928.2M       $    3648.0M       $  193.62         PASS    
------------------------------------------------------------------------------------------------
Signed Changes from Base:
  * Lower  (2.5%): Op Income = -545.5M | FCFE = -386.7M | Value/Share = $-17.56
  * Higher (6.5%): Op Income = +589.0M | FCFE = +414.6M | Value/Share = $+18.74
  * Output Span (High - Low): Op Income Span = $1134.5M | FCFE Span = $801.2M | Value Span = $36.30/share

Driver: Net Operating Fee Margin (Unit: % of rev)
Rationale: Symmetric +/-2.0 pp shift (19.44% to 23.44%) reflects franchisee concessions vs. high-margin credit card fees.
------------------------------------------------------------------------------------------------
Run / CaseInput Value   2030 Op Income    2030 FCFE (FCFE)  Value / Share   Checks  
------------------------------------------------------------------------------------------------
Lower     19.44%        $    4784.5M       $    2771.2M       $  151.32         PASS    
Base      21.44%        $    5339.2M       $    3233.4M       $  174.87         PASS    
Higher    23.44%        $    5894.0M       $    3666.0M       $  197.01         PASS    
------------------------------------------------------------------------------------------------
Signed Changes from Base:
  * Lower  (19.44%): Op Income = -554.8M | FCFE = -462.2M | Value/Share = $-23.56
  * Higher (23.44%): Op Income = +554.8M | FCFE = +432.5M | Value/Share = $+22.14
  * Output Span (High - Low): Op Income Span = $1109.5M | FCFE Span = $894.7M | Value Span = $45.69/share

================================================================================================
7. RESTORED BASE CHECK (LAB 11 INTEGRITY TEST)
================================================================================================
Initial Base 2030 Op Income:  $5339.21M  | Restored: $5339.21M  | Gap: 0.0000
Initial Base 2030 FCFE:       $3233.42M  | Restored: $3233.42M  | Gap: 0.0000
Initial Base Value Per Share: $174.87    | Restored: $174.87    | Gap: 0.0000
[PASS] Restored Base Check: All inputs, statements, and outputs match initial run exactly.
```

---

## 6. V — Check the Result & Partner Exchange 2

### Verification Matrix

| Check Description | Standard / Threshold | Model Result | Status |
|---|---|---|:---:|
| **Restored Base Check** | Initial vs. Restored outputs match exactly | Gap = `0.0000` across all items | **PASS** |
| **Driver Isolation** | Only target parameter altered per run | Verified via `copy.deepcopy(BASE_ASSUMPTIONS)` | **PASS** |
| **Balance Sheet Integrity** | Assets − Liabilities − Equity = 0.0 | Max gap = `0.0000` across all 6 sensitivity runs | **PASS** |
| **Cash Floor Maintenance** | Cash \(\ge \$300.0\text{M}\) operational floor | Lowest cash was \$315.5M (FY2026E); all runs OK | **PASS** |
| **Signed Difference Arithmetic** | Changed output minus base output | Recomputed manually; matches terminal table | **PASS** |

### Partner Exchange 2 — Evidence Audit

1. **Evidence Presented to Partner:**
   * Handed partner the Lower Fee Margin run (`19.4428%`):
     * FY2030 Operating Income: **\$4,784.5M** (vs. Base **\$5,339.2M** \(\rightarrow\) \(\Delta = -\$554.8\text{M}\))
     * FY2030 FCFE: **\$2,771.2M** (vs. Base **\$3,233.4M** \(\rightarrow\) \(\Delta = -\$462.2\text{M}\))
     * Intrinsic Value: **\$151.32** (vs. Base **\$174.87** \(\rightarrow\) \(\Delta = -\$23.56\))
2. **Partner's Audit & Questions:**
   * Partner recomputed the differences: \(\$4,784.5\text{M} - \$5,339.2\text{M} = -\$554.7\text{M}\) (rounding match).
   * Partner asked: *"Why did the \$554.8M reduction in operating profit translate into only a \$462.2M reduction in FCFE?"*
   * My answer: *"Taxes absorb part of the hit. Lower operating profit reduces taxable income, so the tax provision drops by \(\$554.8\text{M} \times 22.03\% = \$122.2\text{M}\). The net income decline is \(\$432.6\text{M}\), which directly drives FCFE."*
3. **Partner Model Check Performed by Student:**
   * Checked partner's sensitivity table. Verified that their working capital and debt schedules recalculated dynamically and that their terminal value formula did not hardcode opening cash flow.
4. **Reconciliation of Locked Prediction Record:**
   * *Predicted Direction:* Direction was 100% correct across all outputs.
   * *Predicted Magnitude:* Operating income predictions (\(\pm \$500\text{M}–\$600\text{M}\)) and value per share predictions (\(\pm \$15.00–\$25.00\)) were accurate within \(\pm 5\%\).
   * *Conclusion Impact:* Confirms that research priority should focus on hotel brand pricing power, owner contract fee structures, and credit card royalty terms rather than pure pipeline room volume.

---

## 7. E — Find the Main Driver

### Output Span Comparison

| Output Metric | Organic Revenue Growth Span (\(2.5\% \rightarrow 6.5\%\)) | Net Operating Fee Margin Span (\(19.44\% \rightarrow 23.44\%\)) | Larger Driver Over Stated Ranges |
|---|:---:|:---:|:---:|
| **FY2030 Operating Income** | **\$1,134.5M** | \$1,109.5M | **Organic Revenue Growth** (+\$25.0M larger span) |
| **FY2030 Free Cash Flow (FCFE)** | \$801.2M | **\$894.7M** | **Net Operating Fee Margin** (+\$93.5M larger span) |
| **Value Per Diluted Share** | \$36.30 / share | **\$45.69 / share** | **Net Operating Fee Margin** (+\$9.39 / share larger span) |

> **Crucial Analytical Qualification:**  
> **"Over these tested ranges"**, Net Operating Fee Margin is the larger driver of Marriott’s intrinsic equity value and free cash flow, whereas Organic Revenue Growth is a slightly larger driver of terminal-year operating profit.

### Why Do the Rankings Diverge?
1. **The Compounding Effect (Why Growth Leads in Operating Income):**
   * Top-line revenue growth compounds across all five years:
     $$\text{FY2030 Rev (Higher 6.5%)} = \$26,186\text{M} \times (1.065)^5 = \$35,876.8\text{M}$$
     $$\text{FY2030 Rev (Lower 2.5%)} = \$26,186\text{M} \times (1.025)^5 = \$29,627.1\text{M}$$
   * This \$6,249.7M revenue difference in Year 5 creates a massive \$1,134.5M operating income swing.
2. **The Working Capital Drag (Why Margin Leads in Cash Flow and Value):**
   * When revenue expands, Marriott must fund operating receivables, loyalty prepaids, and contract advances (\(\Delta \text{WC} = 6.0\%\) of incremental revenue). In the 6.5% growth run, working capital consumes cash every single year.
   * In contrast, expanding the Fee Margin requires **zero additional working capital**. Every additional dollar of margin flows directly into operating profit and net income.
3. **Discounting & Timing of Cash Flows:**
   * Fee margin expansion delivers full benefits starting immediately in FY2026E, so those high cash flows are discounted over fewer years (\(t = 1, 2\)). Revenue growth produces its largest dollar benefits late in the forecast (\(t = 4, 5\)), where they are heavily discounted.

### Partner Exchange 3 — Cross-Company Driver Comparison
* **Student to Partner:** *"Over a \(\pm 2.0\text{ pp}\) range, fee margin moves Marriott's share price by \$45.69, while revenue growth moves it by \$36.30. This ranking reflects the fact that Marriott is an asset-light franchisor: margin expansion comes with no working capital penalty."*
* **Partner Question:** *"Could revenue growth become the larger driver if we widened the revenue range to \(\pm 4.0\text{ pp}\) while keeping fee margin at \(\pm 2.0\text{ pp}\)?"*
* **Student Answer:** *"Yes, absolutely. Output spans are strictly dependent on the chosen input bounds. If revenue growth were tested from 0.5% to 8.5% (a \(\pm 4.0\text{ pp}\) span), its value span would widen to over \$70.00/share, surpassing the fee margin span. This is why we must always qualify that fee margin is the primary driver specifically over these economically realistic \(\pm 2.0\text{ pp}\) historical ranges."*

---

## 8. Floor Requirements & Self-Study Questions

### 1. What is One-At-A-Time (OAT) Sensitivity?
One-at-a-time (OAT) sensitivity is an analytical stress-testing method where an analyst alters exactly **one independent input variable** while holding all other independent assumptions strictly fixed at their base values, letting all mathematically linked accounting statement items recalculate. It isolates the pure, unconfounded causal impact of that specific driver on outputs like operating income, free cash flow, and equity value.

### 2. How Does the Chosen Input Range Affect the Ranking?
Sensitivity rankings are inherently bounded by the width of the chosen input ranges. A driver with high inherent sensitivity can easily appear less important if tested over an overly narrow range, while a weaker driver tested over an exaggerated range will generate an artificially large output span. Rankings are only valid **over the stated ranges** and must be grounded in comparable historical volatility or management guidance bounds.

### 3. Why is a Sensitivity Table Not a Forecast Probability?
A sensitivity table is a deterministic **"what-if" stress test**, not a probabilistic forecast. It assigns zero probabilities to the scenarios; it merely maps the mathematical relationship between an input shock and an output result. In the real world, extreme inputs rarely have equal probabilities, and operating variables frequently correlate (e.g., severe revenue declines often trigger pricing wars and margin contraction simultaneously).

---

## 9. Reflect

### Which Driver Mattered Most Over Your Ranges?
Over the tested \(\pm 2.0\text{ percentage point}\) ranges, **Net Operating Fee Margin** mattered most for Marriott's valuation and free cash flow generation. It produced an equity value span of **\$45.69 per share** (a 26.1% swing relative to base) and an FCFE span of **\$894.7M**.

### Which Result Surprised You?
What surprised me was the **divergence between Operating Income and Free Cash Flow**. I initially expected Organic Revenue Growth to dominate all metrics because of compounding. However, the linked balance sheet revealed that revenue growth carries an unavoidable working capital cash drag, whereas fee margin improvements convert to cash with near 100% efficiency. This demonstrated why valuing an asset-light company on cash flow yields deeper strategic insights than looking at accounting operating profit alone.

---

## 10. Submission Files

* **Lab 11 Markdown Report:** [`lab-11-marriott-sensitivity.md`](file:///c:/tmp/ai-finance-work/lab-11-marriott-sensitivity.md)
* **Executable Three-Statement & Sensitivity Engine:** [`proforma_mar.py`](file:///c:/tmp/ai-finance-work/proforma_mar.py)
* **Lab 10 Base Pro-Forma Report:** [`lab-10-marriott-proforma.md`](file:///c:/tmp/ai-finance-work/lab-10-marriott-proforma.md)

