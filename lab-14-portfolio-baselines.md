# Lab 14 — Portfolio Baselines

## Question

What does each simple portfolio earn and risk, and does it meet Meridian's mandate?

## Files and commands

- `portfolio.py` — reusable standard-library portfolio risk engine.
- `mandate.py` — Lab 13 mandate checker, updated with Candidate E (Meridian's benchmark).

```powershell
python portfolio.py
python mandate.py
```

## Inputs

| Sleeve | Expected return | Volatility |
|---|---:|---:|
| Treasury bills | 3.5% | 0.5% |
| Treasury 10-year note | 4.3% | 7.0% |
| Investment-grade bond fund | 5.0% | 6.0% |
| Global equity index fund | 8.0% | 16.0% |

Objective return: 6.5% (CPI estimate of 2.5% plus 4.0%). Bills and the 10-year note are reserve-eligible.

## Results

| Portfolio | Weights: bills / 10-year / IG / equity | Return | Volatility | Reserve-eligible | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

The engine computes covariance as correlation × volatility × volatility and validates that correlations are between -1 and 1 and symmetric.

## Verification

- Changed IG bonds/equity correlation from 0.25 to 0.50 in both cells: benchmark volatility = **11.00%**.
- Invalid IG bonds/equity correlation of 1.3: the program refuses to run with a clear input error.
- Added Candidate E to `mandate.py`: 40% investment-grade bond fund and 60% global equity index fund.
- Candidate E reserve-eligible weight = **0.0%**, so it fails Meridian's 3.0% reserve requirement.

## Diversification

Diversification is combining assets whose returns do not move perfectly together. When correlation is below +1, the assets' changes partly offset each other, reducing portfolio volatility relative to a perfectly correlated combination.

Benchmark volatility by hand:

```text
variance = (0.40² × 0.06²) + (0.60² × 0.16²)
           + (2 × 0.40 × 0.60 × 0.25 × 0.06 × 0.16)
         = 0.010944

volatility = √0.010944 = 0.1046 = 10.46%
```

## Reflection

Inverse volatility puts most of its weight in bills because its weight is proportional to 1 ÷ volatility; bills have the lowest volatility at 0.5%.

I would show the CIO the benchmark first. It is the only baseline that reaches the 6.5% objective, but it has no reserve-eligible allocation and therefore conflicts with the mandate. That trade-off should be explicit before choosing a portfolio.

## Streamlit setup

Streamlit 1.66.0 is installed in `.venv`.

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit hello
```

## Before Thursday

Choose the personal Project 2 funds (three to six) before downloading five years of monthly Yahoo Finance Adj Close data into `prices.csv`. Record each chosen ticker, fund name, role, source, and download date here.
