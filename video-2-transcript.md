# Video 2 — Code Execution & Validation Suite: Corrected Transcript

**Student:** Lucas Timm  
**Course:** FIN 43900 — Advanced Financial Modeling / AI in Finance (Fall 2026)  
**Company:** Marriott International, Inc. (NASDAQ: MAR)  
**Deliverable Document:** [`video-2-transcript.md`](file:///c:/tmp/ai-finance-work/video-2-transcript.md)  
**Video Recording Link:** `[Paste Video 2 Link Here — e.g. Microsoft Stream / Teams / YouTube]`  

---

### Corrected Spoken Transcript

> "All right, hello, hello. I'll share my screen real quick. 
> 
> And here we go. This is Video 2, Lucas here back on my evaluation for Marriott. We're going to show the running of the code, walk through validation checks to make sure everything's operating cleanly, and break the code to make sure it will identify accounting gaps and preserve model integrity. 
> 
> This demonstrates the execution and stress validation suite. All of these scripts—the `.py` files that run the pro-forma, comps, DCF, and the master runner `run_all.py`—are written in clean standard-library Python without any third-party dependencies, running locally on this machine right here in front of me.
> 
> Let's run the first one to show (`python run_all.py`). Right away, you can see we get the immediate execution steps:
> 
> Starting from the top, going down:
> - **Step 1** is the synthetic baseline test (`dcf.py --training`). All 12 training outputs match the course benchmark down to the exact cent at \$27.50 per share, which is confirmed.
> - **Steps 2 and 3** run our unlinked DCF and comps models cleanly.
> - **Step 4** is a big one: the linked three-statement pro-forma and sensitivity analysis. We are confirming here that the dynamic balance checks passed with a 0.0 gap across all five forecast years, which is huge. When we break it, we'll see this will not be the case.
> - **Step 5** confirms that any intentional balance error will be caught loudly and flagged in red.
> 
> Moving down, this rolls up into the master valuation football field summary table. We will get into this in more depth in the next video, but I wanted to point out this fee margin range difference is around \$45 per share. It proves that the driver we initially identified—Net Operating Fee Margin—is our biggest value driver, which is great to see. You can also see our overall stance: WATCH / DEFER at \$335.50, and our target accumulation buy zone between \$210 and \$230.
> 
> Now, an essential modeling requirement is that articulation checks must fail loudly. To maintain accounting integrity, if it's being violated, the model must break the system and do so loudly. 
> 
> So when I run this next diagnostic command (`python proforma_mar.py --break`), it intentionally introduces a \$50 million imbalance into Year 1. It should immediately catch it if it's doing its job.
> 
> And as you can see on screen, it immediately halts: it finds the balance gap, throws an `AssertionError`, and fails loudly, exiting with error code 1. That is one of the biggest requirements here.
> 
> Last thing being said—we will discuss this more in Video 3—our sensitivity analysis proved that Net Operating Fee Margin was the single biggest value driver compared to revenue growth: a \$45.69 per share value span versus \$36.30 per share for revenue growth.
> 
> Thank you very much."

---

### Manual Transcription Correction Log
In compliance with the "AI Closed / Human Correction" rule, the raw speech-to-text transcript was reviewed and corrected:
- Corrected auto-transcription *"dot UIs"* to **`.py` scripts** (`run_all.py`, `proforma_mar.py`, `comps.py`, `dcf.py`).
- Corrected *"down to percent on that 2750"* to **down to the cent on that \$27.50**.
- Corrected *"time dynamic balance checks"* to **dynamic balance checks (0.0 gap across all 5 years)**.
- Corrected speech-to-text stutter on the break test output to properly record the intentional **\$50M imbalance and `AssertionError` exit code 1**.
- Sourced and formatted the final sensitivity comparison: **\$45.69/share (fee margin) vs. \$36.30/share (revenue growth)**.
