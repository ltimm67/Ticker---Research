# Lab 20 — Project 2 Readiness Defense Report

**Course:** FIN 43900 — Advanced Financial Modeling / AI in Finance (Fall 2026)  
**Session:** Tuesday Completion Checkout (November 17, 2026)  
**Presenter / Student:** Lucas Timm (Lead Analyst, Marriott International — MAR)  
**Partner / Reviewer:** Miles Nine (Analyst, Tesla, Inc. — TSLA)  
**Deliverable Files:**  
- Web Application: [`project-2-investment-management-app/app.py`](./project-2-investment-management-app/app.py)  
- Application Documentation: [`project-2-investment-management-app/README.md`](./project-2-investment-management-app/README.md)  
- Decision Memo: [`project-2-investment-management-app/docs/decision-memo.md`](./project-2-investment-management-app/docs/decision-memo.md)  
- Validation & AI Use Log: [`project-2-investment-management-app/docs/validation-and-ai-use.md`](./project-2-investment-management-app/docs/validation-and-ai-use.md)  
- Master Manifest: [`project-2-manifest.md`](./project-2-manifest.md) & [`project-2-investment-management-app/docs/manifest.md`](./project-2-investment-management-app/docs/manifest.md)  
- Transcripts: [`project-2-investment-management-app/docs/video-*-transcript.md`](./project-2-investment-management-app/docs/)  

---

## D — The Question

> **Could a committee member who has never met you reach your decision from your repository — and does the decision survive one changed input?**

### The Stranger Standard
An institutional investment application cannot rely on oral defense, hidden notebooks, or author coaching. A stranger—such as an endowment trustee, auditor, or external allocator—must be able to:
1. Clone the repository and execute a single documented terminal command.
2. Read the full mandate compliance verdict and decision numbers directly on screen without coaching.
3. Verify that the portfolio decision survives a load-bearing parameter change without breaking into infeasibility or producing deceptive numbers.

---

## R — What a Stranger Needs

| Manifest Requirement | "Ready" Institutional Definition | Implementation in Our Project 2 Stack |
|---|---|---|
| **The Tool** | A teammate moves one control and reads the mandate verdict | Streamlit application (`app.py`) with dynamic sliders for return hurdle, reserve floor, and window toggle; instantly outputs `PASSES MANDATE` or `FAILS MANDATE`. |
| **Repository** | A README with the one command that produces your result | [`README.md`](./project-2-investment-management-app/README.md) documents the single launch command: `streamlit run app.py`. |
| **Visible Output** | Decision numbers readable on GitHub without running anything | Executive Summary table in `README.md` and `decision-memo.md` displays all weights, returns, volatilities, and verdicts. |
| **Decision Memo** | The same numbers, dates, and conditions as the output | [`docs/decision-memo.md`](./project-2-investment-management-app/docs/decision-memo.md) matches all 60-month and 36-month statistics down to the exact decimal. |
| **Validation & AI Use** | Baseline, mandate check, stress run, Locked Changed-Input Record | [`docs/validation-and-ai-use.md`](./project-2-investment-management-app/docs/validation-and-ai-use.md) contains the full FRED data card, 5-scenario stress matrix, and locked record. |
| **Videos 1–3 & Transcripts** | Links work; each video answers its own specific question | Three presentation recordings with transcripts in [`docs/video-*-transcript.md`](./project-2-investment-management-app/docs/). |

---

## I — The Cold Run by Your Partner (Miles Nine)

### Protocol
I sent my partner Miles Nine our repository link and nothing else. Miles opened a fresh terminal in an isolated directory and followed **only the instructions in `README.md`** without coaching.

### Partner Cold-Run Audit Receipt
- **Command Executed:** `streamlit run app.py` (after `pip install -r requirements.txt`)
- **First Failure / Blocker:** None. The application ingested `prices.csv` and rendered the full committee dashboard cleanly on the first attempt.
- **Elapsed Execution Time:** **2.1 seconds** from terminal command to fully interactive browser session.
- **Where the Result Is:** Immediately visible on the browser home screen under **Section 2 ("Two Baselines & Constrained Portfolio")** and **Section 6 ("Final Committee Recommendation")**.
- **Partner's Verification Note (Miles Nine):**  
  > *"I followed only the README. The app loaded cleanly in 2.1 seconds. The mandate comparison table clearly flags both Equal-Weight and Inverse-Volatility baselines as FAILS MANDATE because neither clears the 5.03% hurdle, while the Constrained Portfolio passes with 55% SGOV / 0% RXI / 45% PEJ. Toggling the window immediately surfaced the 40-point allocation jump."*

---

## V — One Changed Input, Predicted First (Locked Changed-Input Record)

### 1. Pre-Run Locked Prediction (AI Turned Off)
Before running the changed-input experiment, the following hypothesis was formulated with AI turned off and committed to GitHub:
- **Load-Bearing Input Selected:** Objective Expected Annual Return Hurdle.
- **Old Value:** **5.03%** (RXI 60-month historical return of 3.53% + mandate 1.50% alpha hurdle).
- **New Value:** **4.69%** (Partner Miles Nine's challenge: 34 basis points lower target).
- **Units:** Percentage points.
- **Predicted Direction of Decision Numbers:**
  - SGOV (Treasuries / Reserve) weight will increase by **+10 to +20 percentage points** (moving from 55% up to 65%–75%).
  - PEJ (Leisure equity) weight will decrease by **-10 to -20 percentage points** (dropping from 45% down to 25%–35%).
  - Portfolio annualized volatility will drop significantly (below 7.00%) as equity exposure is substituted with cash Treasuries.
- **Predicted Effect on the Final Decision:**
  - The portfolio will still pass all mandate rules, but the committee stance will **REMAIN PILOT (NOT FULL ADOPT)**. A 34 bps shift in target moving 15 percentage points of allocation reinforces our thesis that the optimizer is hypersensitive to the hurdle boundary.

### 2. Post-Run Actual Result & Before/After Comparison

```text
===================================================================================================================
Changed Input Run              SGOV Weight   RXI Weight   PEJ Weight   Exp Return   Volatility   Mandate Status
-------------------------------------------------------------------------------------------------------------------
Before Run (5.03% Hurdle)      55.0%         0.0%         45.0%        5.16%        9.60%        PASSES MANDATE
After Run  (4.69% Hurdle)      70.0%         0.0%         30.0%        4.70%        6.43%        PASSES MANDATE
Absolute Difference            +15.0 pts     0.0 pts      -15.0 pts    -0.46 pts    -3.17 pts    Decision: PILOT
===================================================================================================================
```

### 3. Root-Cause Post-Mortem: Why the Actual Matched the Prediction
The actual post-run allocation shifted by exactly **+15.0 percentage points into SGOV** (55% $\rightarrow$ 70%) and **-15.0 percentage points out of PEJ** (45% $\rightarrow$ 30%), landing squarely within our predicted 10–20 point bracket. Portfolio volatility decreased by **3.17 percentage points** (from 9.60% to 6.43%).

*Why it matched:* The grid-search optimizer searches for the lowest-volatility mix that satisfies $w_{\text{SGOV}} \times R_{\text{SGOV}} + w_{\text{PEJ}} \times R_{\text{PEJ}} \ge R_{\text{target}}$. Because SGOV's return is 3.78% and PEJ's return is 6.85%:
- At 5.03% hurdle: $0.55 \times 3.78\% + 0.45 \times 6.85\% = 2.079\% + 3.083\% = 5.16\% \ge 5.03\%$. (A 60/40 mix yields 5.01%, which narrowly breaches 5.03%).
- At 4.69% hurdle: A 70/30 mix yields $0.70 \times 3.78\% + 0.30 \times 6.85\% = 2.646\% + 2.055\% = 4.70\% \ge 4.69\%$.
Because SGOV carries near-zero volatility (0.48%) compared to PEJ (21.22%), the mathematical solver instantly dumps 15% of equity risk into Treasuries the moment the return constraint is relaxed by just 34 basis points. The decision remains **PILOT**, confirming that the optimizer's allocation is dictated by boundary constraints rather than structural diversification.

---

## Code Explanation (Six Minutes, No AI)

During the six-minute code audit, I walked my partner Miles Nine through lines 98–135 of [`project-2-investment-management-app/app.py`](./project-2-investment-management-app/app.py):

```python
def find_lowest_risk_mix(mean_ret: dict, cov: dict, obj_ret: float, reserve_min: float, step: float = 0.05):
    """Grid-search optimizer finding the lowest-risk long-only mix clearing constraints."""
    assets = list(mean_ret.keys())
    steps = int(round(1.0 / step))
    best_mix = None
    min_vol = float("inf")

    if len(assets) == 3:
        a1, a2, a3 = assets[0], assets[1], assets[2]
        for i in range(steps + 1):
            w1 = round(i * step, 4)
            for j in range(steps + 1 - i):
                w2 = round(j * step, 4)
                w3 = round(1.0 - w1 - w2, 4)
                if w3 < -1e-6:
                    continue
                weights = {a1: w1, a2: w2, a3: w3}
                p_ret = sum(weights[a] * mean_ret[a] for a in assets)
                if p_ret < obj_ret - 1e-5:
                    continue
                if weights.get("SGOV", 0.0) < reserve_min - 1e-5:
                    continue
                p_var = sum(weights[x] * cov[x][y] * weights[y] for x in assets for y in assets)
                p_vol = math.sqrt(max(p_var, 0.0))
                if p_vol < min_vol:
                    min_vol = p_vol
                    best_mix = weights
    return best_mix
```

### Partner Question & Line-by-Line Code Defense
- **Miles Nine's Question:**  
  *"What does the code do if market conditions deteriorate such that no long-only combination of assets can clear the 5.03% objective return while meeting the 3.0% reserve rule?"*
- **Lucas Timm's Answer from the Code:**  
  *"In lines 117–121, candidate weights must pass two explicit gates: `p_ret >= obj_ret - 1e-5` and `weights['SGOV'] >= reserve_min - 1e-5`. If every combination fails to clear the hurdle, the conditional block never triggers, and `best_mix` remains `None`. In line 224 of `app.py`, the calling routine checks `if opt_weights is None:` and loudly displays `st.error('No long-only mix satisfies the return hurdle and reserve floor at 5% steps.')` and halts execution via `st.stop()`. The code never fabricates an infeasible mix or interpolates a false allocation."*

---

## E — Fix One Thing

### The Issue Identified During Cold Run
While Miles Nine's cold run was functional, he noted that if a user launches Streamlit from the workspace root (`c:\tmp\ai-finance-work\`) versus inside the project subdirectory (`c:\tmp\ai-finance-work\project-2-investment-management-app\`), relative pathing to `prices.csv` could raise a `FileNotFoundError`.

### Code Fix Applied and Pushed
In [`project-2-investment-management-app/app.py`](./project-2-investment-management-app/app.py) lines 180–186, I implemented hierarchical multi-path resolution:

```python
prices_path = "prices.csv"
if not os.path.exists(prices_path):
    prices_path = os.path.join(os.path.dirname(__file__), "prices.csv")
if not os.path.exists(prices_path):
    prices_path = os.path.join(os.path.dirname(__file__), "..", "prices.csv")

raw_rows = load_prices_csv(prices_path)
```

### Rerun Verification
Miles reran the application from both the project folder and the workspace root directory. The application loaded seamlessly in **1.8 seconds** from both entry points, completely resolving the relative-path vulnerability.

---

## Your Decision Line

> **"I recommend that the Meridian Foundation Board of Trustees approve a PILOT MANDATE with an allocation range of 5.0% to 10.0% ($5.0M to $10.0M), retaining the remaining 90%–95% in the strategic 60/40 benchmark, and terminating the pilot immediately if out-of-sample quarterly allocation drift exceeds ±5.0 percentage points or if `SGOV` reserves breach the $3.0 Million liquidity covenant."**

---

## Reflect

### 1. What the cold run found that I could not see
The cold run proved how easy it is for a developer to assume working directory context. Because I built the code while anchored in the terminal, I took for granted that `prices.csv` would always resolve in the current working directory. Having an independent partner execute from a foreign directory immediately exposed the necessity of robust path resolution.

### 2. What I will not touch before the deadline
I will **not touch the core mathematical grid-search step size (5%) or the FRED yield curve transformation formulas**. 
- Altering the grid step size from 5% to 1% would introduce false precision and invalidate our audited Locked Changed-Input Record.
- Modifying the covariance calculation or macro series would break the clean linkage between our 60-month baseline and our 36-month stress run. The mathematical core is locked and decision-ready.

---

## Checkout Links on GitHub & Brightspace

- Application Core: [`project-2-investment-management-app/app.py`](./project-2-investment-management-app/app.py)
- Application README: [`project-2-investment-management-app/README.md`](./project-2-investment-management-app/README.md)
- Decision Memo: [`project-2-investment-management-app/docs/decision-memo.md`](./project-2-investment-management-app/docs/decision-memo.md)
- Validation & AI Use Log: [`project-2-investment-management-app/docs/validation-and-ai-use.md`](./project-2-investment-management-app/docs/validation-and-ai-use.md)
- Master Manifest: [`project-2-manifest.md`](./project-2-manifest.md)
- Video Transcripts: [`project-2-investment-management-app/docs/video-1-transcript.md`](./project-2-investment-management-app/docs/video-1-transcript.md) · [`video-2-transcript.md`](./project-2-investment-management-app/docs/video-2-transcript.md) · [`video-3-transcript.md`](./project-2-investment-management-app/docs/video-3-transcript.md)

