# Project 1 — Master Submission Manifest

**Course:** FIN 43900 — Advanced Financial Modeling / AI in Finance (Fall 2026)  
**Student / Analyst:** Lucas Timm  
**Partner / Reviewer:** Miles Nine (Tesla, Inc. — TSLA)  
**Target Company:** Marriott International, Inc. (NASDAQ: MAR)  
**Submission Date:** October 2026  
**Final Committee Stance:** **WATCH / DEFER at \$335.50** (Target Entry Zone: Below \$210.00–\$230.00)  
**Deliverable File:** [`project-1-manifest.md`](file:///c:/tmp/ai-finance-work/project-1-manifest.md)  

---

## 1. Primary Deliverables Manifest

| Deliverable | File Path | Status | Description |
|---|---|:---:|---|
| **Edition A Checkpoint** | [`project-1-edition-a.md`](file:///c:/tmp/ai-finance-work/project-1-edition-a.md) | **Complete** | Supervised Week 2 baseline checkpoint with audited 2025 Form 10-K facts, accession number, synthetic training bridge output ($27.50/share), initial thesis, and partner falsification question from Miles Nine. |
| **Master Committee Memo (Edition B)** | [`project-1-memo.md`](file:///c:/tmp/ai-finance-work/project-1-memo.md) | **Complete** | Full 7-section buy-side investment committee memo synthesizing the business architecture, contamination catalog, linked 3-statement pro-forma, valuation spectrum, sensitivity/downside case, assumption challenges, and mandatory AI disclosure log. |
| **Master Code Runner** | [`run_all.py`](file:///c:/tmp/ai-finance-work/run_all.py) | **Complete** | Automated orchestration script executing `dcf.py --training`, `dcf.py`, `comps.py`, `proforma_mar.py`, and `proforma_mar.py --break` in 0.39s. |
| **Cold Run Audit Receipt** | [`cold_run_log.txt`](file:///c:/tmp/ai-finance-work/cold_run_log.txt) | **Complete** | Execution log verifying 12/12 training tests passed, 0.0000 balance sheet articulation gaps, and verified loud break assertions. |
| **Master Roadmap & Guide** | [`PROJECT-1-ROADMAP.md`](file:///c:/tmp/ai-finance-work/PROJECT-1-ROADMAP.md) | **Complete** | Step-by-step execution roadmap, "No AI" boundary map, and grading criteria alignment. |

---

## 2. Quantitative Modeling Stack (Standard-Library Python)

All modeling scripts execute locally without third-party package dependencies:

```bash
# Execute the entire suite end-to-end
python run_all.py

# Individual model components
python dcf.py --training       # 1. Class synthetic training baseline (checks 12 outputs down to $27.50)
python dcf.py                  # 2. Enterprise FCFF DCF & Reverse DCF ($145.41 anchor)
python comps.py                # 3. Pure-play franchisor comps triangulation ($265–$335 band)
python proforma_mar.py         # 4. Five-year linked 3-statement pro-forma ($174.87 FCFE floor)
python proforma_mar.py --break # 5. Diagnostic balance sheet articulation break test (fails loudly)
```

---

## 3. Valuation Football Field & Evidence Summary

```text
=======================================================================================================
Valuation Methodology               Base Value    Valuation Range / Band      Analytical Role
-------------------------------------------------------------------------------------------------------
1. Unlinked FCFF DCF (Lab 06)       $145.41       $126.85 – $169.57           Static Operating Anchor
2. Linked Pro-Forma FCFE (Lab 10)   $174.87       $151.32 – $197.01           Fundamental Cash Flow Floor
3. Adjusted Institutional Fair Value$255.00       $250.00 – $265.00           Buyback Adjusted Fair Value
4. Peer Comps Triangulation (Lab 08)$300.00       $265.00 – $335.00           Peer Royalty Multiple
5. Observed Market Price            $335.50       Observed Sept 10, 2026      Priced for Perfection
=======================================================================================================
FINAL COMMITTEE RECOMMENDATION:     WATCH / DEFER (OVERVALUED AT $335.50)
TARGET ACCUMULATION BUY ZONE:       BELOW $210.00 – $230.00 (Where Margin of Safety Emerges)
```

---

## 4. Video Submissions & Transcripts

The three required student-recorded presentations and corrected transcripts:

### Video 1: Research Evolution & Business Model
- **Duration:** ~3–4 Minutes
- **Video Link:** [Watch Video 1 (Microsoft Stream / Purdue)](https://purdue0-my.sharepoint.com/:v:/g/personal/ltimm_purdue_edu/IQC2QsYIT37qSrRGiTPdHX3OAZESRD_q8VqRELuIDo92Exo?e=3lXnu8&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)
- **Corrected Transcript File:** [`video-1-transcript.md`](file:///c:/tmp/ai-finance-work/video-1-transcript.md)
<details>
<summary>Click to view full corrected transcript</summary>

> "All right, hello, hello. My name is Lucas and this is my Video 1 for Project 1. I did my research and evaluation on Marriott, the hotel company with the ticker MAR. And my initial stance was WATCH / DEFER. We will get into that more later, but I want to start off by saying I chose this company thinking it's one of the biggest real estate companies in the world. 
> 
> But it turns out that Marriott is not actually a real estate company. They are more of an intellectual property licensor and a software network. Marriott actually owns less than 1% of the hotel rooms. Third-party owners build the hotels and deal with the real estate risk that comes along with it, while Marriott brings in franchise royalties and management fees as their source of revenue. I thought that was very interesting and definitely something that not everyone knows about them.
> 
> So getting into why I chose WATCH / DEFER at the market price of $335.50 that it was at the time: We looked into the 10-K, as everyone had to, but the main things that pointed out were the 273.6 million diluted shares, cash at $385 million, and debt of $16.2 billion, with $14.6 billion of that being in senior notes and other long-term debt.
> 
> Those were big standout numbers for me when I was looking at it originally. And the biggest thing that caught my eye was what they called the 'contamination catalog'. This net operating fee revenue of $5.6 billion is the biggest driver that I was able to identify. They report $26.18 billion in total revenue, but about $19.1 billion of that—the difference between these two numbers—is actually just reimbursed expenses that Marriott is paying to basically run the hotel. They don't build it, but they still have expenses to pay the workers, loyalty marketing, stuff like that, which owners reimburse. So this $5.6 billion remaining with the 21.4% fee margin is the real top-line driver and what we need to look at more when evaluating it.
> 
> So my initial stance was WATCH / DEFER at the market price of $335.50. And that was challenged when we did Lab 12. My partner Miles Nine said basically: 'There's negative book equity and aggressive share buybacks while carrying all of that debt. What happens to free cash flow and credit ratings if a recession hits and RevPAR contracts?' Very valid question. 
> 
> This transitioned into: okay, we can't just have a static DCF, we need to dig a little deeper, compare it against peers like Hilton, and ultimately create a three-statement pro-forma. And that's what we did next.
> 
> After creating that, we learned what we could do if this recession happened. To protect the cash floor—a minimum of $300 million in cash—and credit ratings without taking on new debt, since they already have so much debt, I think the best thing in this situation is that management would implement sort of a throttle on the buybacks, cutting them to a certain level to prevent any more debt being taken on.
> 
> This establishes the fundamental floor of $174.87 and ultimately confirms my stance of WATCH / DEFER, because fair value is around $250 to $265 compared with peers. But ultimately, at $335.50, the market is basically putting Marriott at near perfection. The models that I ran and created are saying that is the top, and barring any crazy outcomes it won't get much better than that, which is why I stick with WATCH / DEFER here. Thank you."

</details>
- **Key Files Shown:** [`project-1-edition-a.md`](file:///c:/tmp/ai-finance-work/project-1-edition-a.md), Marriott FY2025 Form 10-K, [`lab-12-marriott-present.md`](file:///c:/tmp/ai-finance-work/lab-12-marriott-present.md).
- **Core Topics Covered:** Transition from naive hotel real estate assumption to asset-light IP brand licensor; \$19.1B reimbursed cost contamination catalog; negative book equity (-\$3.8B) from share repurchases; partner challenge from Miles Nine.

### Video 2: Code Execution & Validation Suite
- **Duration:** ~3–4 Minutes
- **Video Link:** [Watch Video 2 (Microsoft Stream / Purdue)](https://purdue0-my.sharepoint.com/:v:/g/personal/ltimm_purdue_edu/IQCkd-Xhg78CTpLoR9mkkMxjAUPlOY9u72YHTDZPjq0qTJg?e=JAfcd3&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)
- **Corrected Transcript File:** [`video-2-transcript.md`](file:///c:/tmp/ai-finance-work/video-2-transcript.md)
<details>
<summary>Click to view full corrected transcript</summary>

> "All right, hello, hello. I'll share my screen real quick. 
> 
> And here we go. This is Video 2, Lucas here back on my evaluation for Marriott. We're going to show the running of the code, walk through validation checks to make sure everything's operating cleanly, and break the code to make sure it will identify accounting gaps and preserve model integrity. 
> 
> This demonstrates the execution and stress validation suite. All of these scripts—the `.py` files that run the pro-forma, comps, DCF, and the master runner `run_all.py`—are written in clean standard-library Python without any third-party dependencies, running locally on this machine right here in front of me.
> 
> Let's run the first one to show (`python run_all.py`). Right away, you can see we get the immediate execution steps:
> 
> Starting from the top, going down:
> - **Step 1** is the synthetic baseline test (`dcf.py --training`). All 12 training outputs match the course benchmark down to the exact cent at $27.50 per share, which is confirmed.
> - **Steps 2 and 3** run our unlinked DCF and comps models cleanly.
> - **Step 4** is a big one: the linked three-statement pro-forma and sensitivity analysis. We are confirming here that the dynamic balance checks passed with a 0.0 gap across all five forecast years, which is huge. When we break it, we'll see this will not be the case.
> - **Step 5** confirms that any intentional balance error will be caught loudly and flagged in red.
> 
> Moving down, this rolls up into the master valuation football field summary table. We will get into this in more depth in the next video, but I wanted to point out this fee margin range difference is around $45 per share. It proves that the driver we initially identified—Net Operating Fee Margin—is our biggest value driver, which is great to see. You can also see our overall stance: WATCH / DEFER at $335.50, and our target accumulation buy zone between $210 and $230.
> 
> Now, an essential modeling requirement is that articulation checks must fail loudly. To maintain accounting integrity, if it's being violated, the model must break the system and do so loudly. 
> 
> So when I run this next diagnostic command (`python proforma_mar.py --break`), it intentionally introduces a $50 million imbalance into Year 1. It should immediately catch it if it's doing its job.
> 
> And as you can see on screen, it immediately halts: it finds the balance gap, throws an `AssertionError`, and fails loudly, exiting with error code 1. That is one of the biggest requirements here.
> 
> Last thing being said—we will discuss this more in Video 3—our sensitivity analysis proved that Net Operating Fee Margin was the single biggest value driver compared to revenue growth: a $45.69 per share value span versus $36.30 per share for revenue growth.
> 
> Thank you very much."

</details>
- **Key Files Shown:** Terminal running `python run_all.py` and `python proforma_mar.py --break`.
- **Core Topics Covered:** Clean execution in <0.5s; 12/12 training tests matching \$27.50; 0.0000 balance sheet gaps across all 5 forecast years; verified loud assertion failure under `--break`; sensitivity proof of why fee margin is the #1 value driver over revenue growth.

### Video 3: Investment Committee Defense & Final Recommendation
- **Duration:** ~4–5 Minutes
- **Video Link:** [Watch Video 3 (Microsoft Stream / Purdue)](https://purdue0-my.sharepoint.com/:v:/g/personal/ltimm_purdue_edu/IQCj7QYpEmwDT7MvltsGGU9dAdXxy61TpGlGHqpHNxTJBK0?e=ry9UDH&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)
- **Corrected Transcript File:** [`video-3-transcript.md`](file:///c:/tmp/ai-finance-work/video-3-transcript.md)
<details>
<summary>Click to view full corrected transcript</summary>

> "All right, welcome to my investment committee memo on Marriott. I am Lucas Timm, an analyst here on the buy-side equity investment team. Welcome to the committee, and today I'm going to give you my briefing on Marriott and our recommended position.
> 
> To start off, our firm recommendation is **WATCH / DEFER at $335.50**. We should not initiate a position at today's market price of $335.50. 
> 
> While Marriott is a high-quality company—a premier global lodging network—we think right now that this price is priced for perfection. There is zero margin of safety here, so we do not think that it is prudent to initiate. Our target entry buy zone is between **$210.00 and $230.00**, and right now we're trading at $335.50. 
> 
> While we like that it's an asset-light franchisor, it's just not attractive right now at **~35x GAAP P/E** and a **92% premium** over its pro-forma cash flow floor. Once again, there's just zero margin of safety here, and this price currently demands sustained >11% revenue expansion or aggressive discount rates, which we do not see happening.
> 
> Going into our biggest operating driver: that was the Net Operating Fee Margin. As you can see here in the memo's sensitivity grid, Net Operating Fee Margin swings value by **$45.69 per share**, compared to **$36.30 per share** for organic revenue growth. 
> 
> The economic reason for this is that fee margin expansion gives shareholders **zero working capital cash drag**. 100% of those margin dollars flow directly into our free cash flow to equity, as opposed to revenue growth which gets caught up in working capital investment (accounts receivable and accrued fees). So having 100% of incremental margin convert straight into free cash flow makes fee margin the single biggest value driver, which confirmed our thesis.
> 
> Turning to the downside case and my partner review: my partner Miles Nine posed the challenge: *'With negative book equity from aggressive share buybacks while carrying all of this $16.2 billion debt, what happens to free cash flow and credit ratings if a lodging recession hits?'*
> 
> In our model, we implemented an explicit **liquidity throttle on share buybacks** in the downside scenario. In any year where operating cash flow declines by greater than 15%, this throttle automatically scales buybacks down from $2.5 billion to $1.0 billion. This ensures that the cash floor is safely preserved above our **$300 million minimum floor** and Net Debt / EBITDA stays below 3.5x. So in the event of a lodging recession, management curtails buybacks to maintain solvency and credit ratings, establishing a safe downside floor of **$138.50**.
> 
> Finally, scrolling up to our actionable conditions and reversal triggers:
> - **Where we would INITIATE (Buy):** If the price drops below **$210.00 to $230.00**, where fundamental cash flow supports a genuine margin of safety. This could be triggered by macro lodging cycle fears, or audited disclosures proving that co-branded credit card royalties have expanded fee margins sustainably higher.
> - **Where we would REMOVE from our watchlist / REJECT:** If net room growth decelerates below 3.0% combined with a credit rating downgrade warning on its senior debt, or if Marriott begins moving away from its asset-light model by reinvesting capital into owned hotel real estate.
> 
> So we are not rejecting the company; we are recommending **WATCH / DEFER**, waiting for a margin of safety to emerge before allocating capital.
> 
> Thank you, and I look forward to your questions."

</details>
- **Key Files Shown:** [`project-1-memo.md`](file:///c:/tmp/ai-finance-work/project-1-memo.md).
- **Core Topics Covered:** Committee recommendation (Watch/Defer at \$335.50); valuation spectrum; explanation of method disagreement; downside lodging recession stress test with buyback liquidity throttle; reversal buy/reject triggers.

---

## 5. Submission Integrity Checklist

- [x] All code executes with standard-library Python 3.13 (`python run_all.py` passes).
- [x] Balance sheet articulation is dynamic and verified (0.0000 gap).
- [x] Break assertions fail loudly on deliberate imbalance.
- [x] All market facts carry source dates and accession numbers.
- [x] Pass-through reimbursed costs normalized in the Contamination Catalog.
- [x] Partner challenge from Miles Nine formally credited and resolved.
- [x] Mandatory AI disclosure log included in memo with accepted, corrected, and qualified outputs.
- [x] Supervised Edition A Checkpoint recorded in `project-1-edition-a.md`.
- [x] Three student videos recorded, transcripts checked, and URLs pasted above.
