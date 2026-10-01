# Lab 12 — Pro-Forma Sensitivity: Present and Review Your Full Analysis
**Course:** FIN 43900 — Advanced Financial Modeling / AI in Finance (Fall 2026)  
**Session:** Thursday Merit Checkout (October 1, 2026)  
**Presenter:** Lucas Timm  
**Company:** Marriott International, Inc. (NASDAQ: MAR)  
**Partner / Reviewer:** Miles Nine (Analyzing Tesla, Inc. - NASDAQ: TSLA)  
**Deliverable File:** [`lab-12-marriott-present.md`](file:///c:/tmp/ai-finance-work/lab-12-marriott-present.md)  
**Primary Engine:** [`proforma_mar.py`](file:///c:/tmp/ai-finance-work/proforma_mar.py)  
**Companion Evidence:** [`lab-06-marriott-dcf.md`](file:///c:/tmp/ai-finance-work/lab-06-marriott-dcf.md) · [`lab-08-comps-triangulation.md`](file:///c:/tmp/ai-finance-work/lab-08-comps-triangulation.md) · [`lab-10-marriott-proforma.md`](file:///c:/tmp/ai-finance-work/lab-10-marriott-proforma.md) · [`lab-11-marriott-sensitivity.md`](file:///c:/tmp/ai-finance-work/lab-11-marriott-sensitivity.md)  

---

## 1. Current Conclusion & Core Question (D)

> **How did I get from choosing this company to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?**

* **Current Conclusion:** **WATCH / DEFER — DO NOT BUY at the saved market price of \$335.50.**  
* **Valuation Summary:** Marriott’s reported financial statements support a conservative pro-forma intrinsic value floor of **\$174.87 per share** ([`proforma_mar.py`](file:///c:/tmp/ai-finance-work/proforma_mar.py)) and an adjusted institutional fair value of **\$250.00–\$265.00**. At today's market price of **\$335.50** (~35x P/E), the stock offers zero margin of safety and demands >11% annual revenue compounding or an aggressive 6.5% discount rate.  
* **Target Entry Price:** Wait for a macroeconomic or travel pullback toward **\$210.00–\$230.00** before initiating a position.

*Do not average conflicting valuation methods. They use different cash-flow definitions, dates, and capital-structure assumptions:*
* *Unlinked FCFF DCF (Lab 06):* **\$145.41** (Sept 10, 2026; FCFF; 273.6M diluted shares; WACC 8.90%).
* *Linked FCFE Pro-Forma (Lab 10):* **\$174.87** (Sept 24, 2026; FCFE; 273.6M diluted shares; Cost of Equity 8.90%).
* *Comps Triangulation (Lab 08):* **\$265.00 – \$335.00** (Sept 10, 2026; peer P/E multiples of 28x–50x).
* *Observed Market Price:* **\$335.50** (Nasdaq real-time, Sept 10, 2026).

---

## 2. Six-Stop Presentation Route (Lucas Timm Presenting Marriott to Miles Nine)

### Stop 1: Target Selection Rationale
* **Why Marriott (MAR)?** I selected Marriott because it represents the global lodging leader (~9,000 properties across 140+ countries) operating as a pure **asset-light franchisor and brand manager**.
* **Suitability to Analyze:** Offers unique structural dynamics:
  1. **Zero physical inventory** (lodging services are consumed instantaneously).
  2. **Negative book equity (-\$3,842M in FY2025)** resulting from aggressive share repurchases, not operating distress.
  3. **High cash conversion (>85% of net income to FCFE)** because third-party property owners fund hotel real estate capital expenditures.
* **Initial View vs. Reality:** I initially assumed Marriott was a capital-heavy hotel real estate owner. Filing research revealed it owns less than 1% of its rooms—it is fundamentally an intellectual property licensing and software booking network.

---

### Stop 2: Company and Evidence
* **Primary Sources:** Marriott International FY2023–FY2025 Form 10-Ks (Item 7 MD&A, Item 8 Financial Statements) and Q2 2026 10-Q.
* **How Marriott Earns Money:**
  * **Total Reported Revenue (FY2025):** **\$26,186.0M** (Consolidated Income Statement).
  * **Pass-Through Reimbursed Costs:** **-\$19,139.0M** (Zero-margin pass-through expenses incurred for managed property staff, centralized loyalty marketing, and system reservations, reimbursed 1:1 by property owners).
  * **Owned/Leased Expenses:** **-\$1,432.0M** (Direct costs for the <1% of physical hotels owned).
  * **Net Operating Fee Pool (True Gross Profit):** **\$5,615.0M** (**21.44% Net Fee Margin** on total revenue).
  * **Base Franchise Royalties:** **\$3,212.0M** across ~7,000 franchised properties.
  * **Total Fee Revenues:** **\$5,050.0M** (Note 18 Segment Reporting).
* **Key Evidence:** FY2025 net room additions (+4.7% to ~1.6 million rooms), worldwide RevPAR growth (+2.0% in 2025, guided to 3.0%–3.5% in 2026), and corporate tech capex guidance under \$600M.

---

### Stop 3: The Three-Statement Pro-Forma Engine ([`proforma_mar.py`](file:///c:/tmp/ai-finance-work/proforma_mar.py))
* **How History Became Forecast (FY2026E–FY2030E):**
  * *Organic Revenue Growth:* 4.5% annual rate (blends management guidance of 3.0%–3.5% RevPAR expansion with 4.5% net room pipeline).
  * *Fee Margin:* 21.4428% (anchored on FY2025 audited net operating fee pool).
  * *SG&A Leverage:* Corporate overhead improves from 15.49% to 15.00% of gross profit.
  * *Capex:* \$600.0M a year (centralized reservation systems and Bonvoy mobile tech).
  * *Inventory & Floor Plan:* Stated **"None" (\$0.0)** (franchisor carries no physical stock or auto-dealer floor plans).
  * *Capital Return & Debt:* Scheduled senior debt retirement of \$300.0M/yr and share repurchases of \$2,500.0M/yr.
* **Cash Flow Statement Solves Ending Cash:** Cash is computed last after explicit working capital, debt paydown, and buybacks. Cash floor is maintained above the \$300M policy.
* **Accounting Checks:** Model balances dynamically across all five years (`Assets − Liabilities − Equity = 0.0000`).

```text
PRO-FORMA SUMMARY TABLE (USD Millions, proforma_mar.py)
Line Item                        FY2026E     FY2027E     FY2028E     FY2029E     FY2030E
----------------------------------------------------------------------------------------
Total Revenues                   27364.4     28595.8     29882.6     31227.3     32632.5
Net Operating Fee Margin (GP)     5867.7      6131.7      6407.7      6696.0      6997.3
Operating Income (EBIT)           4354.5      4591.6      4840.3      5084.3      5339.2
Net Income                        2797.2      2993.1      3198.1      3399.4      3609.2
Free Cash Flow to Equity (FCFE)   2430.5      2624.3      2827.1      3026.0      3233.4
Ending Cash                        315.5       439.8       766.8      1292.9      2026.3
Assets - Liab - Equity Gap           0.0         0.0         0.0         0.0         0.0
```

---

### Stop 4: Valuation Methods and Why They Disagree
* **Discount Rate:** 8.90% Cost of Equity (4.0% risk-free rate + 1.15 beta \(\times\) 5.0% ERP).
* **Terminal Growth:** 2.50% long-run sustainable GDP growth rate.
* **Why the Methods Differ:**
  * *DCF (\$145.41):* Enterprise FCFF model; does not capture fee operating leverage or scheduled senior debt paydown.
  * *Pro-Forma FCFE (\$174.87):* Fully linked 3-statement model; captures SG&A operating leverage and normalizes terminal base FCFE by adding back the \$300M 2030 debt repayment (\(FCFE_{2030} + \$300\text{M} = \$3,533.4\text{M}\)). Represents our conservative fundamental floor.
  * *Comps Triangulation (\$265.00–\$335.00):* Direct peers trade at royalty premiums (Hilton at ~50x P/E, Marriott at ~35x P/E) because markets price them as high-quality consumer compounders.
  * *Reverse DCF on Market Price (\$335.50):* Proves the market requires +6.43 pp above guided growth (>11% annual revenue growth) or an aggressive 6.5% discount rate.

---

### Stop 5: Sensitivity Analysis and Key Drivers ([`lab-11-marriott-sensitivity.md`](file:///c:/tmp/ai-finance-work/lab-11-marriott-sensitivity.md))
* Tested symmetric **\(\pm 2.0\text{ percentage point}\)** shifts across FY2026E–FY2030E:
  * *Organic Revenue Growth:* 2.5% \(\rightarrow\) 4.5% \(\rightarrow\) 6.5%
  * *Net Operating Fee Margin:* 19.4428% \(\rightarrow\) 21.4428% \(\rightarrow\) 23.4428%

```text
OUTPUT SPAN COMPARISON (LAB 11)
Metric                           Revenue Growth Span (2.5%->6.5%)   Fee Margin Span (19.44%->23.44%)   Dominant Driver Over Stated Range
----------------------------------------------------------------------------------------------------------------------------------------
FY2030 Operating Income (EBIT)   $1,134.5M                          $1,109.5M                          Growth (+ $25.0M larger span)
FY2030 Free Cash Flow (FCFE)     $  801.2M                          $  894.7M                          Fee Margin (+ $93.5M larger span)
Value Per Diluted Share          $   36.30 / share                  $   45.69 / share                  Fee Margin (+ $9.39 / share larger)
```

* **Causal Link:** 
  1. *Operating Income:* Revenue growth compounds geometrically (\((1.065)^5\) vs \((1.025)^5\)), producing a slightly higher 2030 EBIT span.
  2. *Cash Flow & Value:* Higher revenue creates a **working capital cash drag** ($\Delta \text{WC} = 6.0\%$ of incremental revenue), while fee margin expansion requires **zero working capital**—flowing directly into FCFE and driving a wider value span (\$45.69 vs. \$36.30).
* **Limitation:** Ranking is qualified by the chosen \(\pm 2.0\text{ pp}\) historical ranges; a wider \(\pm 4.0\text{ pp}\) growth shock would overtake margin.

---

### Stop 6: Interpretation, Conditional Recommendation & Next Research
* **Supported Recommendation:** **WATCH / DEFER at \$335.50.** The stock trades at a demanding 92% premium to fundamental cash flow value (\$174.87) and offers no margin of safety.
* **Evidence That Would Change My View:**
  1. *Credit Card Royalty Surge:* Updated 10-K disclosures showing Chase/Amex royalty fees doubling, lifting blended fee margin above 24% (adds +\$45+/share).
  2. *Soft-Brand Conversion Boom:* Proving net room additions can sustain 8%+ annual growth through hotel conversions rather than 3-year new builds.
  3. *Price Pullback:* Stock dropping below **\$210.00–\$230.00**, entering our fundamental fair-value zone.
* **Next Research Priority:** Reconcile static share count with dynamic buyback accretion and investigate co-branded credit card renewal terms.

---

## 3. V — Live Review Record (Conducted with Miles Nine)

### Part A: Feedback Received as Presenter (Lucas Timm Reviewed by Miles Nine)

* **Selection & Evidence Question from Miles:**  
  * **Miles Nine:** *"You chose Marriott because of its asset-light franchisor economics. Which 10-K note supports your base franchise royalty fee revenue of \$3,212M and net unit room growth of 4.7%, and what reporting period was used?"*  
  * **My Answer:** *"Base franchise fees of \$3,212M come from Marriott's FY2025 Form 10-K Consolidated Statements of Income (for the year ended Dec 31, 2025). The total fee pool is detailed in Note 18 (Segment Reporting), which reports \$5,050M in total contract fee revenues across segments. Net room growth of ~4.7% (expanding the system to ~1.6 million rooms) is confirmed on page 42 of Item 7 (MD&A)."*
* **Model & Valuation Question from Miles:**  
  * **Miles Nine:** *"How does your 48.0% franchise fee margin flow through Marriott's three statements without requiring capital expenditures or working capital, and how does that support Marriott's 10-K share repurchases?"*  
  * **My Answer:** *"In the franchise segment, hotel owners pay for hotel land, construction, and maintenance capex. Marriott's incremental cost is virtually zero—just cloud reservation software and brand compliance. Because capex is restricted to under \$600M in corporate tech (and pure maintenance capex is under \$300M), over 80% of fee revenue flows straight through to operating cash flow. This massive cash flow is what funds the \$2,500M in annual share buybacks without burning down cash reserves."*
* **Sensitivity & Interpretation Question from Miles:**  
  * **Miles Nine:** *"Your sensitivity showed fee margin had higher leverage than room growth. If lodging demand slows and RevPAR drops across North America, does Marriott's high operating leverage make fee margin more uncertain than room count additions?"*  
  * **My Answer:** *"Yes, that is an essential operational distinction. Room count additions are locked in under multi-year construction pipelines and are very sticky. RevPAR and incentive management fees, however, are highly sensitive to business travel cycles. If RevPAR contracts, fee margins come under pressure from lower incentive fees, making margin our most volatile and highest-impact financial lever."*

* **Source or Calculation Checked by Miles on Marriott:**  
  * *Check Performed:* Miles opened Marriott's FY2025 Form 10-K (Item 8, Note 18 Segment Reporting and Item 7 MD&A p. 42). He traced total fee revenues of \$5,050M and confirmed net room additions of +4.7%.  
  * *Result of Check:* **Supported.** Miles verified that Marriott’s capital expenditures were strictly corporate tech/software, confirming that over 80% of incremental franchise fees flow to operating cash flow, validating my asset-light model.

* **Miles's Explanation Back of Marriott:**  
  * *Miles's Summary:* *"Lucas’s core thesis is that Marriott is a high-margin, asset-light royalty machine supported by stable mid-single-digit room expansion. His model gives a conservative downside floor of \$174.87, but the stock at \$335.50 is overvalued and priced for perfection, justifying a WATCH / DEFER stance. The main driver is fee margin; the biggest operational limitation is vulnerability to cyclical RevPAR contractions in corporate travel."*

* **Miles's Feedback to Me:**  
  * *Evidence-Backed Strength:* Direct, verified alignment between Marriott's pipeline disclosures in the 10-K and the net room addition forecast.  
  * *Specific Improvement to Make Next:* Explicitly model a liquidity restriction or throttle on share repurchases in the lower-growth sensitivity scenario so Marriott does not increase debt leverage during an industry downturn.

---

### Part B: Questions Asked as Reviewer (Lucas Timm Reviewing Miles Nine on Tesla)

* **Miles’s Company Analyzed:** Tesla, Inc. (NASDAQ: TSLA) — Electric Vehicles & Clean Energy
* **Miles’s Stated Conclusion:** **WATCH / DEFER — do not initiate at the saved market price of \$378.94.** Tesla's reported automotive and energy fundamentals do not support the market price. The central unresolved issue is the speculative value of autonomy, software, and robotics cash flows not yet separately established in historical filings.

1. **Selection & Evidence Question I Asked Miles:**  
   * *"Why is Tesla's 2026 capital spending modeled at \$25,000M when FY2025 actual capex was only \$8,527M, and where is that verified in the SEC filings?"*  
   * *Miles's Answer:* Sourced directly from Tesla's Q2 2026 Form 10-Q (p. 35, Liquidity and Capital Resources): management explicitly states capex is expected to be *'in excess of \$25.0 billion in 2026'* to fund compute infrastructure (Dojo and Nvidia GPU clusters), humanoid robotics (Optimus), and dedicated Cybercab tooling.
2. **Model & Valuation Question I Asked Miles:**  
   * *"Why did your valuation per share drop from \$29.05 in Lab 09 to -\$1.83 in Lab 11, and does -\$1.83 mean the equity is fundamentally worthless?"*  
   * *Miles's Answer:* The discrepancy stems from inconsistent treatment of balance-sheet assets and negative early FCFE. Lab 09 discounts operating FCFE and adds \$28,010M of excess cash, \$674M of digital assets, and \$3,007M of SpaceX equity in its equity bridge. Lab 11 discounts signed forecast FCFE without adding those balance-sheet assets, producing -\$1.83/share. That number is not a complete equity value and does not mean equity is worthless. The pro-forma uses cash above the \$15B floor and a temporary revolver to fund negative-FCFE capex years.
3. **Sensitivity & Interpretation Question I Asked Miles:**  
   * *"Testing only a \(\pm 1.0\text{ pp}\) range on Gross Margin (21.39% to 23.39%) versus \(\pm 2.0\text{ pp}\) on Growth (8% to 12%)—does that artificially penalize margin against growth, and does that distort your driver ranking?"*  
   * *Miles's Answer:* Miles explained that driver rankings over stated ranges are fundamentally constrained by balance sheet solvency. While a 1.0 pp shift in Gross Margin carries identical per-unit power to growth (~+\$794M in operating income), testing a wider margin drop (such as 2.0 pp to 20.39%) breaches Tesla's \$15.0B cash floor and exhausts its \$5.0B credit facility. Margin's narrower range reflects capital-structure risk, not mathematical insignificance.

4. **Source & Calculation Checked on Miles’s Model:**  
   * *Calculation Checked:* Sourced Tesla's Q2 2026 Form 10-Q (p. 35) to verify the \$25,000M capex guidance line, and traced his pro-forma cash floor check in FY2027E: \(\text{Ending Cash} = \$15,000.0\text{M}\) maintained with a \$1,240M revolver draw.  
   * *Result of Check:* **Supported.** Verified that Miles's revolver borrowing and cash floor logic operated cleanly without breaking model balance checks.

5. **My Explanation Back of Miles's Tesla Analysis:**  
   * *Summary:* Miles concludes a **WATCH / DEFER** on Tesla because current market prices (\$378.94) embed massive unproven optionality for autonomy and robotics. His pro-forma model shows that near-term capex of >\$25B creates negative FCFE through 2029, and core automotive/energy cash flows only support a fundamental value between \$29 (with cash bridge) and \$125–\$140 (adjusted DCF). The main driver is delivery volume growth over the tested range, but margin is constrained by solvency.
   * *Evidence-Backed Strength:* Excellent, verified sourcing of the massive \$25B capex guidance from the Q2 10-Q and disciplined modeling of the \$15B cash floor.  
   * *Specific Next Improvement:* Formally reconcile the excess-cash bridge between Lab 09 and Lab 11 so readers understand that -\$1.83 represents an incomplete operating FCFE bridge rather than an assertion of zero equity value.

---

## 4. E — After-Review Decisions & Reconciliation

### Post-Review Action: What to Keep, Revise, and Investigate

1. **What I Will Keep:**
   * Keep the primary pro-forma base valuation locked at **\$174.87**. It serves as an audited 10-K downside floor that withstands academic and risk scrutiny.
   * Keep the WATCH / DEFER recommendation at \$335.50. Both Miles and I confirmed that our respective target companies trade at demanding market prices that price in perfection.
2. **What I Will Revise:**
   * **Implement Miles’s Feedback:** Model an explicit dynamic **liquidity throttle on share repurchases** in the lower-growth sensitivity scenario. If RevPAR slows, buybacks should automatically scale back from \$2,500M to preserve the \$300M cash floor without taking on term debt.
   * Include a formal **Valuation Bridge Slide** illustrating the path from our fundamental floor to market price:
     $$\$174.87 \text{ (Floor)} \;\xrightarrow{+\$35\text{ (Buybacks)}}\; \$210 \;\xrightarrow{+\$50\text{ (7.5\% WACC)}}\; \$260 \text{ (Fair Value)} \;\xrightarrow{+\$75\text{ (Hype)}}\; \$335.50 \text{ (Market)}$$
3. **What I Will Investigate in Project 1 Studio:**
   * Investigate whether Marriott’s co-branded credit card renewal contracts with Chase and Amex include upfront signing bonus payments, and examine how those payments are amortized into operating income.

---

## 5. Reflect

* **Which Question Made You Reconsider Something?**  
  * Miles's question about whether Marriott's high operating leverage makes fee margin more volatile than room count in a lodging downturn made me rethink our risk model. Room count is sticky and contractual, but incentive fees and RevPAR can collapse rapidly during a recession. This proved that our primary risk is RevPAR compression, not unit cancellations.
* **What Do You Now Understand Better About Your Company?**  
  * Comparing Marriott with Miles’s Tesla highlighted the power of the **asset-light franchise model**. Tesla must reinvest tens of billions in gigafactories to grow, generating negative FCFE and solvency constraints. Marriott generates billions in positive free cash flow because third-party owners fund the physical hotels. Marriott is not a hotel company; it is an intellectual property licensing and software network.

---

## 6. Submission & Code Links

* **Lab 12 Presentation Report:** [`lab-12-marriott-present.md`](file:///c:/tmp/ai-finance-work/lab-12-marriott-present.md)
* **Linked Pro-Forma Engine:** [`proforma_mar.py`](file:///c:/tmp/ai-finance-work/proforma_mar.py)
* **Sensitivity Analysis Notes:** [`lab-11-marriott-sensitivity.md`](file:///c:/tmp/ai-finance-work/lab-11-marriott-sensitivity.md)
* **Base Pro-Forma Assumptions:** [`lab-10-marriott-proforma.md`](file:///c:/tmp/ai-finance-work/lab-10-marriott-proforma.md)
* **Comps Triangulation:** [`lab-08-comps-triangulation.md`](file:///c:/tmp/ai-finance-work/lab-08-comps-triangulation.md)
* **Initial DCF & Reverse DCF:** [`lab-06-marriott-dcf.md`](file:///c:/tmp/ai-finance-work/lab-06-marriott-dcf.md)

