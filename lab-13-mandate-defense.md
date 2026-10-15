# Lab 13 — Portfolio Mandate Defense

**Course:** FIN 43900 — Advanced Financial Modeling / AI in Finance (Fall 2026)  
**Session:** Thursday Merit Checkout (October 15, 2026)  
**Presenter / Student:** Lucas Timm (Lead Analyst, Marriott International — MAR)  
**Partner / Reviewer:** Miles Nine (Analyst, Tesla, Inc. — TSLA)  
**Deliverable Files:** [`mandate.py`](file:///c:/tmp/ai-finance-work/mandate.py) · [`lab-13-mandate-defense.md`](file:///c:/tmp/ai-finance-work/lab-13-mandate-defense.md)  
**Client Mandate Case:** Meridian Foundation Reserve ($100 Million Reserve Mandate)  

---

## 1. Sort Before You Build (No AI): S1–S10 Classification

Before writing a single line of Python, each statement from the Meridian Foundation CIO is sorted into its formal institutional Investment Policy Statement (IPS) category with an operational justification:

| # | What the CIO Said | Classification | Operational Reason |
|---|---|---|---|
| **S1** | Horizon seven years; annual rebalancing. | **Hard constraint** | Imposes an immovable seven-year terminal liquidity boundary and an enforceable annual trading cadence that legally bounds re-allocation. |
| **S2** | Objective: CPI + 4% a year, net of costs, over rolling five-year periods. | **Objective** | Defines the foundation's primary economic hurdle: preserving real purchasing power while funding perpetual intergenerational grants. |
| **S3** | Pays out \$0.75M every quarter; 12 months of payouts held in cash or daily-liquid government securities. | **Hard constraint** | Non-negotiable liquidity requirement: requires $4 \times \$0.75\text{M} = \$3.0\text{M}$ (3.0% of \$100M reserve) held in cash or 1-day liquid Treasuries to guarantee contractual payouts. |
| **S4** | Benchmark: 60% global equities, 40% U.S. investment-grade bonds. | **Preference** | Serves as the strategic asset allocation reference portfolio for measuring relative risk and returns, not a rigid constraint fixing portfolio weights. |
| **S5** | Long-only: no borrowing, short sales or derivatives. | **Hard constraint** | Strict legal prohibition: negative weights ($w_i < 0$), margin leverage, short positions, and synthetic derivative contracts are banned. |
| **S6** | No single issuer above 8%. | **Hard constraint** | Enforceable concentration limit: caps exposure to any single corporate credit or equity issuer at 8.0%, aggregating across all security classes. |
| **S7** | Annual turnover at most 25% without committee approval. | **Hard constraint** | Hard trading boundary: annual two-way portfolio rebalancing transactions cannot exceed \$25M without formal investment committee sign-off. |
| **S8** | At least 90% redeemable within five business days. | **Hard constraint** | Structural liquidity constraint: at least 90% of assets must be convertible to cash within one business week. |
| **S9** | "The reserve cannot have a calendar-year loss greater than 10%." No measure, no breach rule. | **Unverifiable promise** | Expresses an aspirational downside hope without a statistical confidence level (e.g., 95% 1-yr VaR), historical window, or algorithmic action protocol upon breach. Cannot be checked on static weights. |
| **S10** | No sector, ESG, tax or home-bias preference; nobody has said what the pilot should optimize. | **Missing** | The mandate lacks an explicit mathematical objective function for portfolio optimization (e.g., max Sharpe ratio vs. min tracking error vs. min variance), while explicitly confirming zero non-financial constraints. |

---

## 2. The Mandate Checker Engine (`mandate.py`)

The mandate verification engine was implemented in [`mandate.py`](file:///c:/tmp/ai-finance-work/mandate.py) using standard-library Python only. All outputs are computed dynamically from inputs.

### Core Architecture & Exemption Rules
- **Reserve Minimum Formula:**
  $$\text{Reserve Minimum} = \frac{\text{Quarters to Cover} \times \text{Quarterly Distribution}}{\text{Reserve Size}} \times 100 = \frac{4 \times \$0.75\text{M}}{\$100.0\text{M}} \times 100 = 3.0\%$$
- **Issuer Exemption Policy:** Cash, U.S. Treasury, and diversified funds are exempt from the 8.0% single-issuer limit. All securities of a single non-exempt corporation (e.g., Acme Corp bonds + Acme Corp stock) are aggregated together.

### Verification Run & Output Table (V)
Command to run:
```bash
python mandate.py
```

```text
Reserve minimum: 3.0% of the portfolio.

Candidate A:
  Weights sum to 100:            100.0 pass
  Long-only (lowest weight):     0.0 pass
  Reserve >= 3.0%:               14.0 pass
  Redeemable in 5 days >= 90%:   100.0 pass
  Largest single company <= 8%:  0.0 pass
  Calendar-year loss:            requires CIO clarification
  Verdict:                       passes every checkable rule

Candidate B:
  Weights sum to 100:            100.0 pass
  Long-only (lowest weight):     0.0 pass
  Reserve >= 3.0%:               1.0 FAIL
  Redeemable in 5 days >= 90%:   85.0 FAIL
  Largest single company <= 8%:  9.0 FAIL
  Calendar-year loss:            requires CIO clarification
  Verdict:                       fails 3 rule(s)

Candidate C:
  Weights sum to 100:            100.0 pass
  Long-only (lowest weight):     0.0 pass
  Reserve >= 3.0%:               2.0 FAIL
  Redeemable in 5 days >= 90%:   100.0 pass
  Largest single company <= 8%:  8.0 pass
  Calendar-year loss:            requires CIO clarification
  Verdict:                       fails 1 rule(s)

Candidate D:
  Weights sum to 100:            100.0 pass
  Long-only (lowest weight):     0.0 pass
  Reserve >= 3.0%:               3.0 pass
  Redeemable in 5 days >= 90%:   100.0 pass
  Largest single company <= 8%:  0.0 pass
  Calendar-year loss:            requires CIO clarification
  Verdict:                       passes every checkable rule
```

### Complete Verification Summary Grid
```text
================================================================================================
SUMMARY VERIFICATION TABLE (Lab 13 — V & E)
================================================================================================
Rule                           | A                  | B                  | C                  | D                 
------------------------------------------------------------------------------------------------
Weights sum to 100             | 100.0 pass         | 100.0 pass         | 100.0 pass         | 100.0 pass        
Long-only (lowest weight)      | 0.0 pass           | 0.0 pass           | 0.0 pass           | 0.0 pass          
Reserve >= 3.0%                | 14.0 pass          | 1.0 FAIL           | 2.0 FAIL           | 3.0 pass          
Redeemable in 5 days >= 90%    | 100.0 pass         | 85.0 FAIL          | 100.0 pass         | 100.0 pass        
Largest single company <= 8%   | 0.0 pass           | 9.0 FAIL           | 8.0 pass           | 0.0 pass          
Calendar-year loss             | requires CIO clarification | same       | same               | same              
------------------------------------------------------------------------------------------------
Verdict                        | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) | passes every checkable rule
================================================================================================
```

### Probe Test: Proving the Checker Catches Violations
To prove the checker dynamically evaluates constraints rather than hard-coding answers, we conducted the mandated probe test:
- **Probe Inputs in Candidate A:** Set `Cash = -2.0%` and `Global equity index fund = 64.0%`.
- **Rerun Result:**
  - `Long-only (lowest weight)`: Reads `-2.0 FAIL`.
  - `Reserve >= 3.0%`: Reads `10.0 pass` ($-2.0\% + 2.0\% + 10.0\% = 10.0\% \ge 3.0\%$).
  - `Weights sum to 100`: Reads `100.0 pass`.
  - `Redeemable in 5 days`: Reads `100.0 pass`.
  - `Largest company`: Reads `0.0 pass`.
  - `Verdict`: Accurately shifts to `fails 1 rule(s)`.
- Candidate A was subsequently restored to original inputs.

---

## 3. Quizzing the Engine

**Target Line Under Review:**
```python
company_totals[issuer] = company_totals.get(issuer, 0.0) + weight
```
- **Self-Quiz Question:** *Why must `issuer` be checked against `EXEMPT_ISSUERS` and aggregated across all security types rather than checking individual holding lines?*
- **My Answer:** *Because a corporation can issue multiple classes of securities (e.g., Acme Corp issued both bonds and stock in Candidate B). If we checked each line independently, Acme bonds (5.0%) and Acme stock (4.0%) would each falsely pass the 8.0% limit. Grouping by corporate issuer reveals the combined 9.0% concentration, correctly catching the mandate violation.*

---

## 4. E — Attack Your Own Checker (Candidate D)

### Candidate D Allocation (Lucas Timm):
- **Cash:** 3.0%
- **Global equity index fund:** 97.0%
- **All other assets:** 0.0%

### Mandate Check Status
- Weights sum: 100.0% (Pass)
- Long-only: 0.0% min (Pass)
- Reserve-eligible: 3.0% (Pass: meets exact \$3M cash floor)
- 5-Day Liquidity: 100.0% (Pass: Cash 0 days, Global equity 2 days)
- Single Company: 0.0% (Pass: no non-exempt corporate issuers)
- **Verdict:** `passes every checkable rule`.

### AI Closed Human Judgment: Does the Objection Hold?
> Yes, the objection holds because allocating 97% of the reserve to equities completely distorts the foundation's risk profile and creates an unacceptable drawdown exposure. **Statement S4** (the 60/40 equity/bond strategic policy benchmark) and the downside intent of **Statement S9** decide it, as a 97% equity fund will inevitably experience calendar-year drawdowns between -20% and -35% during severe market contractions (such as 2008 and 2022).

### Partner Swap Review (Miles Nine on Tesla / Reserve Allocation)
- **Miles Nine's Candidate D:**
  - **Allocation:** Cash 3.0%, U.S. Treasury bills 97.0%, all others 0.0%.
  - **Checker Verdict:** Passes all checkable rules (Reserve 100%, Liquidity 100%, Company 0%, Sum 100%).
- **Statement Lucas Cites Against Miles's Portfolio:**
  > I cite **Statement S2 (Objective: CPI + 4% a year net of costs over rolling five-year periods)** against Miles's portfolio. While 100% Cash/T-bills is bulletproof on liquidity and credit risk, its long-term expected real return after inflation and costs is ~0%, mathematically guaranteeing the failure of the foundation's primary investment objective.

---

## 5. The One Question for the CIO

> **"What is the mathematical objective function for the portfolio optimizer (e.g., minimizing tracking error to the 60/40 benchmark vs. maximizing Sharpe ratio net of fees), and what specific statistical metric and breach protocol define the S9 10% calendar-year loss rule (e.g., 95% annual VaR, conditional VaR, or a hard risk budget)?"**

### The Answer That Would Change the Portfolio:
- **Scenario A (Tracking Error Minimization):** If the CIO clarifies, *"Minimize tracking error against the 60/40 policy benchmark with a maximum active risk of 2.0%,"* then the portfolio must strictly anchor to 60% global equities and 40% investment-grade bonds (similar to Portfolio A).
- **Scenario B (Downside VaR Maximization):** If the CIO clarifies, *"Maximize net return subject to a strict 99% 1-year Value-at-Risk loss limit of 10%,"* equity exposure must be dramatically cut from 60% down to **30%–35%** with a large allocation to short-term Treasuries, because a 60/40 benchmark historically suffers calendar-year losses of -15% to -25% during market crises.

---

## 6. Investment Policy Statement (IPS) — Learn on Your Own

### 1. What is an Investment Policy Statement?
An Investment Policy Statement (IPS) is the formal governing charter between an institutional asset owner (e.g., foundation, endowment, pension fund) and its portfolio managers. It establishes the rules of engagement, translating the client's qualitative mission into quantitative boundaries, strategic benchmarks, risk budgets, and accountability frameworks.

### 2. How Does It Work: Objectives and Constraints?
Institutional portfolio design operates under the classic CFA Institute asset-management framework:
- **Objectives:**
  1. *Return Requirement:* Real hurdle rate required to fulfill distributions and maintain endowment corpus.
  2. *Risk Tolerance:* The client's willingness (psychological) and ability (structural balance-sheet capacity) to withstand drawdowns.
- **Constraints (The 5 Pillars):**
  1. *Time Horizon:* Investment runway influencing asset class selection.
  2. *Liquidity Needs:* Anticipated cash outflows requiring liquid reserves.
  3. *Tax Considerations:* Tax status (e.g., non-profit tax-exempt status).
  4. *Legal and Regulatory Requirements:* Prudent Investor laws, fiduciary duties, and concentration rules.
  5. *Unique Circumstances:* Ethical restrictions, ESG mandates, or specific asset exclusions.

### 3. Mapping S1–S10 into the IPS Framework
```text
IPS Element                  CIO Statement & Mapping
-------------------------------------------------------------------------------------------------
Return Objective             S2 (CPI + 4% net of costs over rolling 5-year periods)
Risk Tolerance               S9 ("Cannot have calendar-year loss > 10%" — Unverifiable risk limit)
Time Horizon Constraint      S1 (Seven-year investment horizon)
Liquidity Constraint         S3 ($0.75M quarterly payout; 12 months in cash/daily Treasuries)
                             S8 (At least 90% redeemable within 5 business days)
Asset Allocation Policy      S4 (60% global equities / 40% U.S. investment-grade bonds benchmark)
Governance / Rebalancing     S1 (Annual rebalancing cadence)
                             S7 (Annual turnover at most 25% without committee approval)
Legal & Mandate Limits       S5 (Long-only: no borrowing, short sales, or derivatives)
Concentration Constraint     S6 (No single issuer above 8%, with cash/Treasury/fund exemptions)
Unique Circumstances         S10 (Zero ESG, tax, or sector preferences; unstated objective function)
```

---

## 7. Reflect

### 1. Why a Portfolio Can Pass Every Checkable Rule and Still Be Wrong
A software checker tests **necessary negative constraints** (e.g., weights are not negative, leverage is zero, cash meets the minimum floor). It does not evaluate **sufficiency, holistic suitability, or economic alignment**.  
Both Candidate D examples prove this disconnect:
- A 97% equity portfolio passes every checkable rule in code, but takes reckless market risk that offends the client's 60/40 benchmark (S4) and violates their downside loss expectation (S9).
- A 100% Cash/T-bill portfolio passes every checkable rule in code, but starves the client of return, guaranteeing failure of the CPI + 4% mandate (S2).  
Code enforces boundary lines; human judgment ensures mandate fidelity.

### 2. The S1–S10 Type I Was Least Sure Of
I was least sure of **Statement S4 (Benchmark: 60% global equities, 40% U.S. investment-grade bonds)**.  
Initially, one might classify a benchmark as a hard constraint requiring the portfolio to hold exactly 60% equities and 40% bonds. However, in institutional practice, a policy benchmark is a **preference / performance comparator**, not a rigid constraint. Active managers are allowed deliberate active tilts around the benchmark (e.g., Candidate B's 55% equity or Candidate C's 70% equity). It only becomes a hard constraint if the mandate specifies an explicit active tracking error limit (e.g., maximum $\pm 2.0\%$ tracking error), which the Meridian CIO failed to provide.

---

## 8. Preview: Project 2 Mandate Design (Marriott Equity Sleeve)

For Project 2, I formulate the client mandate for an institutional lodging and consumer discretionary equity sleeve:

- **Target / Client:** University Endowment Long-Only Equity Reserve (Hospitality & Brand Infrastructure Sleeve).
- **Return Objective:** Outperform the MSCI World Consumer Discretionary Index by +150 bps net of fees over rolling 3-year periods.
- **Hard Constraints:**
  - Long-only: 0% leverage, no short positions, no derivatives.
  - Single-Issuer Limit: Maximum 10.0% in any single corporate issuer (permitting high-conviction core positions in top franchisors like Marriott International — MAR).
  - Liquidity: 95% of the portfolio redeemable in $\le 3$ business days.
  - Cash Floor: Minimum 2.0% cash reserve for routine redemptions.
- **The One Question for the Client:**
  > *"Does your endowment committee enforce an exclusion policy against gaming and casino hotel properties (which affects Marriott's casino-resort partnerships), and what is the allowable active share and tracking error budget against the benchmark?"*

---

## 9. Submission & Evidence Links

- **Python Rule Checker:** [`mandate.py`](file:///c:/tmp/ai-finance-work/mandate.py)
- **Mandate Defense Deliverable:** [`lab-13-mandate-defense.md`](file:///c:/tmp/ai-finance-work/lab-13-mandate-defense.md)
- **Prior Lab Foundations:** [`lab-12-marriott-present.md`](file:///c:/tmp/ai-finance-work/lab-12-marriott-present.md) · [`run_all.py`](file:///c:/tmp/ai-finance-work/run_all.py)
