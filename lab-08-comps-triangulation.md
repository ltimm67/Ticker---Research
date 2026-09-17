# Lab 08 — Deal Evidence and Valuation Triangulation: Marriott International (NASDAQ: MAR)

**Company:** Marriott International, Inc. (NASDAQ: MAR)  
**Valuation Date:** September 10, 2026 (matching Week 3 DCF date)  
**Today's Market Price:** \$335.50 (observed Nasdaq Real-Time, Sept 10, 2026, 1:45 PM EDT)  
**Target Diluted EPS:** \$9.51 (FY2025 Form 10-K, Item 8, filed Feb 10, 2026)  
**Calculator Script:** [`comps.py`](comps.py)  

---

## 1. Define & Discover: Understanding Marriott's Economics

### How Marriott Earns Money
Marriott is a worldwide lodging franchisor, operator, and licensor. Its business model is fundamentally **asset-light**:
- **Franchise Fees:** Royalties charged as a percentage of gross room revenues (typically 4%–6%) across >9,800 properties.
- **Management Fees:** Base management fees (percentage of revenue) and incentive management fees (percentage of hotel operating profits).
- **Brand Licensing & Co-Branded Credit Cards:** Substantial, high-margin licensing fees from partners such as JPMorgan Chase and American Express.
- **Owned/Leased Real Estate:** Represents <1% of its system rooms. Marriott does not rely on real estate appreciation or rental income; its economics are driven by fee volume, global brand power, RevPAR, and room count expansion.

### Reported Earnings Profile
Marriott reported positive GAAP diluted EPS of **\$9.51** for FY2025 (Net Income of \$2,662M across 273.6M diluted shares), confirming that a P/E multiple calculation is mathematically and economically viable for the target company.

### Focused Research Question
> *"What premium or discount does the market apply to Marriott's asset-light fee stream relative to direct lodging peers (Hilton, Hyatt, Wyndham), and can a peer P/E multiple justify the large gap between today's market price (\$335.50) and the 5-year FCFF DCF intrinsic value (\$145.41)?"*

---

## 2. Represent: Peer Policy & Candidate Decisions

### Peer Selection Policy (Established Before Gathering Multiples)
1. **Business Economics That Must Match:**
   - Asset-light, fee-driven lodging franchisor or manager.
   - Revenue predominantly composed of franchise royalties and management fees.
   - Global or national brand scale with loyalty program network effects.
   - Low ongoing capital expenditure requirements relative to operating cash flow.
2. **Differences to Qualify:**
   - Companies undergoing transition to asset-light (e.g., significant disposition accounting or lingering owned assets).
   - Franchise-only operators that lack luxury/lifestyle and large-scale managed-hotel breadth (e.g., economy/midscale concentration).
3. **Differences to Exclude:**
   - **Hotel Real Estate Investment Trusts (REITs)** (e.g., Host Hotels [HST], Park Hotels [PK]): Excluded because they are capital-intensive asset owners with heavy property-level debt, depreciation, and real estate risks.
   - **Online Travel Agencies (OTAs)** (e.g., Booking Holdings [BKNG], Expedia [EXPE]): Excluded because they are digital distribution channels and travel agencies without lodging brand ownership, franchise compliance, or hotel operations.

### Candidate Evaluation & Sourced Evidence Table

| Candidate Company | Trading Price (Sept 10, 2026) | FY2025 Reported Diluted EPS | Fiscal Period & 10-K Date | Policy Decision | Business Comparison & Section Locator | Primary SEC Source |
|---|---|---|---|---|---|---|
| **Hilton Worldwide Holdings Inc. (NYSE: HLT)** | \$306.24 | \$6.12 | FY ended Dec 31, 2025 (Filed Feb 11, 2026) | **Use** | **Closest Peer:** Pure-play asset-light lodging operator. Over 90% of revenue is fee-based franchise royalties and management fees. Similar global multi-brand portfolio and customer loyalty platform. Sourced from 2025 Form 10-K, Item 1 ("Business") and Item 8 Consolidated Statements of Operations. | [HLT 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1564590/000156459026003214/hlt-20251231.htm) |
| **Hyatt Hotels Corporation (NYSE: H)** | \$163.07 | \$(0.55) | FY ended Dec 31, 2025 (Filed Feb 13, 2026) | **Qualify (Unusable for P/E)** | **Diagnostic Limitation:** Direct global hospitality peer, but underwent significant real estate asset sales and disposition accounting charges, producing negative FY2025 GAAP diluted EPS of \$(0.55). Because EPS is negative, P/E is **not meaningful** and cannot mathematically support valuation. Sourced from 2025 Form 10-K, Item 8 Consolidated Statements of Income. | [H 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1468174/000146817426000018/h-20251231.htm) |
| **Wyndham Hotels & Resorts, Inc. (NYSE: WH)** | \$69.80 | \$2.50 | FY ended Dec 31, 2025 (Filed Feb 19, 2026) | **Qualify** | **Segment Mismatch:** Operates a pure-play franchise model (~9,000 hotels), but portfolio is concentrated in economy and midscale select-service properties (Super 8, Days Inn, Ramada). Lacks Marriott's high-margin luxury/full-service brands (Ritz-Carlton, St. Regis, Marriott) and managed-contract revenue. Sourced from 2025 Form 10-K, Item 1 and Item 8 Statements of Income. | [WH 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1726165/000172616526000009/wh-20251231.htm) |

---

## 3. Implement: Calculator Execution (`comps.py`)

Run the calculator with standard library Python:
```bash
python comps.py
```

### Complete Terminal Output
```text
============================================================================
Comparable-Company Valuation: P/E Multiple Analysis
Target: Marriott International, Inc. (MAR)
Valuation Date: September 10, 2026
Target Share Price: $335.50
Target Diluted EPS: $9.51
============================================================================

Candidate Peer Multiples:
Ticker   Name                             Policy          Price        EPS     P/E Multiple
--------------------------------------------------------------------------------------------
HLT      Hilton Worldwide Holdings Inc.   Use           $306.24      $6.12       50.039216x
H        Hyatt Hotels Corporation         Qualify       $163.07     -$0.55   not meaningful
WH       Wyndham Hotels & Resorts, Inc.   Qualify        $69.80      $2.50       27.920000x
--------------------------------------------------------------------------------------------

Summary Valuation Statistics (2 usable peers):
Target Diluted EPS:     $9.51
Peer Median P/E:        38.979608x
Peer P/E Range:         27.920000x to 50.039216x
Peer-Implied Range:     $265.52 - $475.87
At Peer Median:         $370.70

============================================================================
Leave-One-Peer-Out Sensitivity Analysis
============================================================================
Remove HLT  (Hilton Worldwide Holdings Inc.):
  Remaining peer(s):          WH
  Remaining median P/E:       27.920000x
  Remaining implied price:    $265.52
  Dollar change from median:  -$105.18

Remove WH   (Wyndham Hotels & Resorts, Inc.):
  Remaining peer(s):          HLT
  Remaining median P/E:       50.039216x
  Remaining implied price:    $475.87
  Dollar change from median:  +$105.18
```

---

## 4. Validate: Calculations & Peer Decisions

### Hand-Checked Arithmetic
1. **Hilton P/E:** \(\$306.24 / \$6.12 = \mathbf{50.039216\times}\)
   - Implied Marriott Price at Hilton multiple: \(50.039216 \times \$9.51 = \mathbf{\$475.87}\)
2. **Wyndham P/E:** \(\$69.80 / \$2.50 = \mathbf{27.920000\times}\)
   - Implied Marriott Price at Wyndham multiple: \(27.920000 \times \$9.51 = \mathbf{\$265.52}\)
3. **Peer Median P/E:** \((50.039216 + 27.920000) / 2 = \mathbf{38.979608\times}\)
   - Implied Marriott Price at Peer Median: \(38.979608 \times \$9.51 = \mathbf{\$370.70}\)

### Leave-One-Out Sensitivity Analysis
- **Removing Hilton (HLT):** Removes the premium-multiple peer (50.04×). The median collapses to Wyndham's multiple (27.92×), causing the implied share price to drop by **−\$105.18** to **\$265.52**.
- **Removing Wyndham (WH):** Removes the discount economy peer (27.92×). The median rises to Hilton's multiple (50.04×), increasing the implied price by **+\$105.18** to **\$475.87**.
- **Single-Peer Reference Note:** If Wyndham is excluded due to brand-tier mismatch, Hilton remains the sole usable peer, producing a single-peer reference estimate of **\$475.87** with **no range**.
- **Hyatt Negative Earnings Diagnostic:** Hyatt's FY2025 EPS of \$(0.55) properly triggered the calculator's `not meaningful` flag. We do not substitute non-GAAP adjusted earnings or force an artificial positive number; Hyatt serves as an empirical demonstration that GAAP accounting noise can temporarily disable P/E comparability.

---

## 5. Evolve: Valuation Triangulation & Skeptical Colleague Review

### Valuation Comparison Table

| Method | Marriott Result (Sept 10, 2026) | Primary Assumptions & Drivers | Key Limitations |
|---|---|---|---|
| **Week 3 FCFF DCF** | Base Case: **\$145.41**<br>Range: **\$109.19 – \$203.64** | Starting FCFF \$3,111M; 5-yr growth path 6.0% \(\rightarrow\) 4.0%; WACC 8.90%; Terminal Growth 2.50%; Net Debt \$15,826M; 273.6M shares. | Projects company-level FCFF at top-line RevPAR rates (3%–6%); fails to reflect the rapid compounding of cash flow *per share* generated by Marriott retiring 3%–5% of its shares annually via buybacks. |
| **Peer P/E Multiples** | Median: **\$370.70**<br>Range: **\$265.52 – \$475.87**<br>*(Single HLT ref: \$475.87)* | Multiples of 27.92× (WH) to 50.04× (HLT) applied to Marriott's FY2025 reported diluted EPS of \$9.51. | Reflects current equity market sentiment and trailing GAAP profits. Hilton's 50x multiple prices in peak cycle optimism; Hyatt was unusable; Wyndham lacks luxury scale. P/E ignores balance sheet debt differences. |
| **Market Reality** | **\$335.50** (Target Price) | Trailing P/E = **35.28×**; Reverse DCF requires **+16.37 ppt** growth shift. | Market prices Marriott between Wyndham and Hilton, baking in significant fee-margin leverage and ongoing buybacks. |

### Skeptical Colleague Review & Inquiry

> **Skeptical Critique:**  
> *"Your peer P/E valuation (\$265.52–\$475.87) is over \$100 higher than your DCF range (\$109.19–\$203.64). You are benchmarking Marriott against Hilton at 50× trailing earnings, but Hilton has lower debt-to-EBITDA and superior net room growth pipeline metrics. Furthermore, Marriott's net debt is \$16.2 billion. P/E ignores debt differences because it is an equity multiple. If lodging demand softens, high fixed interest costs will crush Marriott's net income faster than its revenue drops.  
> **One Question:** If international RevPAR turns negative and debt refinancing rates stay elevated, won't Marriott's multiple compress toward Wyndham's 28× (\$265), and isn't your DCF's \$145 value the true fundamental downside floor?"*

### Response to Skeptical Critique
- **Judgment:** **ACCEPT.**
- **Reasoning:** The critique correctly identifies the core structural vulnerability: P/E multiples evaluate equity without penalizing differences in enterprise leverage. Marriott carries \$16.2B in debt versus Hilton's ~\$11B. In Q2 2026, Marriott's international RevPAR contracted by 0.5% due to geopolitical headwinds, and interest expense rose year-over-year. If lodging demand softens, financial leverage amplifies earnings contraction, exposing investors to double downside: falling EPS and multiple compression toward Wyndham's 27.9× (\$265.52).

---

## 6. Reflect: Final Synthesis & Conditional Recommendation

### Peer Policy Defense & Triangulation Takeaways
1. **P/E Adds Market Context to DCF:** The DCF proved that Marriott cannot be justified on organic hotel room cash flows alone at an 8.9% WACC. The peer comparison explains *why* the market pays \$335.50: investors treat mega-cap lodging franchisors as capital-light royalties, awarding them premium multiples (35×–50×) comparable to consumer brand monopolies.
2. **Why We Do Not Average the Methods:** Mechanically averaging \$145.41 and \$370.70 produces a meaningless \$258 compromise. Instead, the DCF provides the **fundamental downside floor**, while the peer P/E range defines the **market pricing band**.

### Final Stance & Conditional Call
**Current Call: WATCH-DEFER.**  
At **\$335.50**, Marriott trades at 35.3× trailing earnings. This already captures the bulk of the peer re-rating (well above Wyndham's 27.9×) while sitting far above its fundamental DCF value (\$145.41).

> **Conditional Call:**  
> **Initiate if** market price pulls back below **\$265.00** (aligning with Wyndham's multiple, narrowing the reverse-DCF growth demand to a realistic +6.6 percentage points, and providing a 21% margin of safety against today's price), OR if Marriott reports two consecutive quarters of >5% international RevPAR acceleration alongside total debt reduction below \$14.0 billion.  
> **Otherwise, defer.**  
> **Item to Monitor:** Worldwide RevPAR growth and net debt/EBITDA leverage in the upcoming Q3 2026 earnings release.

