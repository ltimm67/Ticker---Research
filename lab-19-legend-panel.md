# Lab 19 — Legend Panel

## Known answer: COST

`python panel.py COST` reproduced the required results:

| Investor | Result |
|---|---|
| Buffett | 3 of 3 — OWN THE BUSINESS |
| Graham | 2 of 3 — WATCH; current ratio fails at 1.06 |
| Burry | 2 of 2 — BULLISH / OWN; liabilities/equity passes at 1.49 |

The Streamlit panel runs at `http://localhost:8501`. It displays the investor-by-check table, three verdicts, three side-by-side memos, and the all-memo unprinted-number audit. The audit returned zero unprinted numbers.

## Graham threshold probe

At the standard current-ratio threshold of 2.0, Graham fails COST at 1.06. At 1.0, Graham passes COST at 1.06. I keep **2.0** because it is the intended conservative Graham screen; 1.0 is useful only as a documented business-model probe for a rapid-turnover retailer.

## Project 2 company: AMZN

I used Amazon (AMZN), the largest holding in RXI. The panel preserves the missing `Liabilities` tag as `not known` rather than estimating it.

| Investor | Result |
|---|---|
| Buffett | 1 of 3 — PASS |
| Graham | 1 of 3 — PASS |
| Burry | 1 of 2 — WATCH / HEDGE; leverage check not known |

### Bull case

Amazon's operating cash flow met or exceeded net income in every year tested, including $139,514.0M of operating cash flow versus $77,670.0M of net income in 2025. Net income also grew from $33,364.0M in 2021 to $77,670.0M in 2025.

### Bear case

The panel records a 2022 net loss of $2,722.0M and negative owner earnings of $16,893.0M, so both Buffett's consistency tests and Graham's earnings-record test fail. Graham's latest current ratio is only 1.05 versus 2.0, and Burry's leverage conclusion is not known because the `Liabilities` tag was not found.

### Decision

**Only with a condition:** use the panel as a first-pass screen for AMZN only after manually resolving Burry's missing liabilities input and reviewing whether Graham's liquidity threshold fits Amazon's business model.

## Code explanation: `evaluate_graham_checks`

1. It reads the most recent row's `current_ratio` and builds the check label from the chosen threshold.
2. If that ratio is missing, `not found`, or `not known`, it returns `not known`; otherwise it compares the numeric value with the threshold and returns pass or fail.
3. It collects net income for every year. If any value is missing, it returns `not known`; otherwise any value at or below zero makes the earnings-record check fail.
4. It compares the first and final net-income values. Missing endpoints produce `not known`; a higher final value passes and every other numeric result fails.
