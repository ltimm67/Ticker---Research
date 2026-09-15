# Lab 07 — Comparable-Company Policy and Implied Range (Asbury Case)

**Course:** FIN 43900 — AI Finance Applications  
**Topic:** Comparable-Company Valuation (P/E Multiples & Peer Policy)  
**Target Company:** Asbury Automotive Group, Inc. (NYSE: ABG)  
**Valuation Date:** Retrospective training comparison as of December 31, 2024  
**Script:** [`comps.py`](comps.py)  

---

## 1. Define & Discover: What P/E Can and Cannot Tell You

### What is Price-to-Earnings (P/E)?
- **Price per share ($P$):** The observable equity market price required to buy one share of ownership. It reflects the market's collective present-value estimate of all future earnings, growth, and risks per share.
- **Earnings per share ($EPS$):** The net income attributable to common shareholders divided by weighted-average diluted shares over a period (e.g., FY2024 GAAP diluted EPS). It measures accounting profit generated per ownership unit.
- **P/E Multiple ($P / EPS$):** The number of dollars the market is willing to pay today for each dollar of current annual accounting earnings.

### Why Use a Multiple?
1. **Size Neutralization:** Comparing raw prices (\$169.84 vs. \$421.48) or net incomes is meaningless across companies of different scale. P/E standardizes equity value relative to current earning power, allowing comparison of differently sized competitors.
2. **Complement to DCF:** While a DCF calculates intrinsic value from fundamentals (FCFF, discount rates, explicit growth, terminal multiples), comps capture **relative market consensus**—what market participants are actively paying *today* for similar earnings streams. It acts as an external reality check on DCF assumptions.

### When Is P/E Useful vs. Misleading?
- **Useful When:** Peer companies share similar business models, operating margin structures, capital structures (leverage), reinvestment needs, accounting policies, and long-term earnings growth profiles.
- **Misleading When:**
  - **Negative Earnings ($EPS \le 0$):** Produces negative or mathematically meaningless multiples (cannot divide price by negative earnings to imply positive value).
  - **Unusual / Non-Recurring Items:** One-time asset sales, restructuring charges, or litigation spikes distort GAAP net income without changing underlying earning power.
  - **Differing Capital Structures:** Highly levered firms have depressed net income (due to high interest expense), which can distort P/E. (Note: P/E is an equity multiple and must **never** be bridged with enterprise-level debt or cash).
  - **Divergent Growth / ROIC:** A company growing earnings at 15% deserves a higher multiple than one growing at 3%.
- **Why Lower P/E \(\neq\) Better Investment:** A low P/E is often a "value trap" reflecting justified market skepticism: declining market share, high structural debt, vulnerable margins, or low returns on invested capital. Conversely, a high P/E often reflects superior returns on capital and durable growth runways.

---

## 2. Represent: Peer Policy for the Asbury Case

### Why Franchised Vehicle Retail & Parts/Service Matter More Than an Industry Label
A broad industry tag like "Automotive Retail" lumps together wildly different business models:
- Franchised new-vehicle dealerships (ABG, AN, GPI) hold manufacturer franchise rights, carry new/used inventories, arrange F&I (financing & insurance), and crucially derive **high-margin, recession-resilient gross profits from parts and warranty/customer service**.
- Used-only retailers (e.g., Carvana, CarMax) lack OEM franchise protections and high-margin parts/service absorption, facing extreme inventory depreciation risk and volatile margins.
- Thus, peer comparability demands matching revenue mix (especially parts/service gross profit absorption), not generic NAICS/SIC labels.

### Candidate Peer Evaluation

| Candidate Peer | Dec 31, 2024 Price | FY2024 GAAP Diluted EPS | Candidate P/E | Policy Decision | Business Rationale |
|---|---|---|---|---|---|
| **AutoNation (AN)** | \$169.84 | \$16.92 | **10.037825×** | **Use** | Direct franchised dealer peer. Dominant US presence, comparable revenue mix across new/used vehicle sales, parts/service, and customer financing. Similar scale and operating margin profile. |
| **Group 1 Automotive (GPI)** | \$421.48 | \$36.81 | **11.450149×** | **Qualify** | Direct franchised dealership operator, but carries significant international exposure (substantial UK dealership operations) and has pursued an aggressive international dealership acquisition strategy. Qualify because UK macroeconomic conditions, exchange rates, and acquisition integration create geographic and operating differences not present in Asbury's primarily US-focused footprint. |

---

## 3. Implement & Validate: Code Output & Checks

### Exact Run Command
```bash
python comps.py
```

### Complete Terminal Output
```text
========================================================================
Comparable-Company Valuation: P/E Multiple Analysis
Target: Asbury Automotive Group (ABG)
Target Share Price: $243.03
Target Diluted EPS: $21.50
========================================================================

Candidate Peer Multiples:
Ticker   Name                          Price        EPS     P/E Multiple
------------------------------------------------------------------------
AN       AutoNation                  $169.84     $16.92       10.037825x
GPI      Group 1 Automotive          $421.48     $36.81       11.450149x
------------------------------------------------------------------------

Summary Valuation Statistics (2 usable peers):
Peer median P/E:        10.743987x
Peer P/E range:         10.037825x to 11.450149x
Peer-implied range:     $215.81 - $246.18
At peer median:         $231.00

========================================================================
Leave-One-Peer-Out Sensitivity Analysis
========================================================================
Remove AN   (AutoNation):
  Remaining peer(s):          GPI
  Remaining median P/E:       11.450149x
  Remaining implied price:    $246.18
  Dollar change from median:  +$15.18

Remove GPI  (Group 1 Automotive):
  Remaining peer(s):          AN
  Remaining median P/E:       10.037825x
  Remaining implied price:    $215.81
  Dollar change from median:  -$15.18
```

### Validation Matrix (Six Required Checks)

| Check | Case Benchmark | [`comps.py`](comps.py) Result | Status |
|---|---|---|---|
| **AutoNation P/E** | 10.037825× | **10.037825×** | Matched |
| **Group 1 P/E** | 11.450149× | **11.450149×** | Matched |
| **Peer Median P/E** | 10.743987× | **10.743987×** | Matched |
| **Asbury Peer-Implied Range** | \$215.81–\$246.18 | **\$215.81–\$246.18** | Matched |
| **Asbury at Peer Median** | \$231.00 | **\$231.00** | Matched |
| **Remove GPI: Remaining AN Estimate** | \$215.81 | **\$215.81** | Matched |
| **Remove GPI: Change from Median** | −\$15.18 | **−\$15.18** | Matched |

---

## 4. Evolve: Changing the Peer Set & Sensitivity Interpretation

### Prediction and Result of Removing Group 1 (GPI)
- **Prior Prediction:** Because Group 1 trades at the higher multiple (11.450149×) compared to AutoNation (10.037825×), removing GPI will pull the median down to AutoNation's standalone multiple. Asbury's implied price will fall by exactly half the spread between the two peers.
- **Observed Result:**
  - Remaining median P/E drops from **10.743987×** to **10.037825×**.
  - Implied share price drops from **\$231.00** to **\$215.81** (\(-\$15.18\)).
  - **Loss of Range:** With only one peer remaining, the model produces a **single-peer reference estimate**, not a range. A range mathematically requires at least two distinct bounding points (min and max). A single peer provides an anchor for discussion, but cannot indicate dispersion or market consensus breadth.
- **Peer Set Decision Retention:**
  - We retain Group 1 as a **qualified peer** rather than excluding it entirely. While its UK exposure justifies noting caution, both companies operate franchised vehicle retail and parts/service networks. Dropping GPI entirely leaves the valuation hostage to a single firm's idiosyncratic pricing (AutoNation), whereas qualifying GPI acknowledges both US-centric and multinational franchised dealership multiples.

---

## 5. Reflect: What the Comparison Means for Asbury

1. **Where Asbury's Market Price Sits:**
   - Asbury's actual closing price on December 31, 2024 was **\$243.03** (P/E of \(243.03 / 21.50 = 11.303721\times\)).
   - This sits **within the two-peer implied range of \$215.81–\$246.18**, above the peer median (\$231.00) and closer to Group 1's multiple (\$246.18 implied).
2. **Why Comps Do Not Prove Asbury is Fairly Valued:**
   - Market multiples reflect *pricing*, not intrinsic *value*. If the entire dealership sector was systematically mispriced by the market at year-end 2024 (e.g., due to post-pandemic vehicle margin normalization fears), relative pricing to peers merely confirms that Asbury is priced consistently with competitors, not that the absolute price is fundamentally sound.
   - P/E does not account for differences in balance sheet leverage, inventory aging, customer loan portfolio recourse, or long-term capital allocation (share buybacks vs. dealership M&A).

