"""
mandate.py — Portfolio Mandate Rule Checker
Course: FIN 43900 — Advanced Financial Modeling / AI in Finance (Fall 2026)
Lab: Lab 13 — Portfolio Mandate Defense
Client: Meridian Foundation Reserve ($100M Reserve Mandate)
Standard library only. All values computed dynamically from inputs.
"""

import sys

# ==============================================================================
# EDITABLE INPUTS
# ==============================================================================

# Mandate parameters
RESERVE_SIZE = 100.0           # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions per quarter
QUARTERS_TO_COVER = 4          # Twelve months of payouts
LIQUIDITY_WINDOW = 5           # Business days to redeem
MIN_LIQUID_SHARE = 90.0        # Percent of portfolio redeemable within window
ISSUER_LIMIT = 8.0             # Percent limit for single company issuer
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}

# Holdings table
# (holding, issuer, business days to redeem, reserve-eligible)
HOLDINGS = [
    {"holding": "Cash",                        "issuer": "none",             "days": 0,  "reserve_eligible": True},
    {"holding": "Treasury bills",              "issuer": "U.S. Treasury",    "days": 1,  "reserve_eligible": True},
    {"holding": "Treasury 10-year note",       "issuer": "U.S. Treasury",    "days": 1,  "reserve_eligible": True},
    {"holding": "Global equity index fund",    "issuer": "diversified fund", "days": 2,  "reserve_eligible": False},
    {"holding": "Investment-grade bond fund",  "issuer": "diversified fund", "days": 3,  "reserve_eligible": False},
    {"holding": "Private real estate fund",    "issuer": "diversified fund", "days": 90, "reserve_eligible": False},
    {"holding": "Acme Corp bonds",             "issuer": "Acme Corp",        "days": 4,  "reserve_eligible": False},
    {"holding": "Acme Corp stock",             "issuer": "Acme Corp",        "days": 1,  "reserve_eligible": False},
]

# Candidates (percent of the portfolio)
CANDIDATES = {
    "A": {
        "Cash": 2.0,
        "Treasury bills": 2.0,
        "Treasury 10-year note": 10.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 26.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    "B": {
        "Cash": 1.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 55.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 15.0,
        "Acme Corp bonds": 5.0,
        "Acme Corp stock": 4.0,
    },
    "C": {
        "Cash": 1.0,
        "Treasury bills": 1.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 70.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 8.0,
    },
    "D": {
        # Candidate D: Propose one portfolio that passes every checkable rule
        # but that the Meridian CIO could reasonably reject (offends S4 benchmark and exposes S9 loss)
        "Cash": 3.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 97.0,
        "Investment-grade bond fund": 0.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    "E": {
        # Meridian's benchmark: 40% investment-grade bonds / 60% global equity.
        "Cash": 0.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 40.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
}

# ==============================================================================
# MANDATE CHECK ENGINE
# ==============================================================================

def compute_reserve_minimum():
    """quarters x distribution / reserve size, as a percent."""
    return (QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION) / RESERVE_SIZE * 100.0


def evaluate_candidate(cand_weights, reserve_min):
    """Evaluate one candidate portfolio against all mandate rules."""
    holdings_dict = {h["holding"]: h for h in HOLDINGS}
    
    # 1. Weights sum to 100
    total_weight = sum(cand_weights.values())
    sum_pass = abs(total_weight - 100.0) < 1e-4
    
    # 2. Long-only (lowest weight not negative)
    lowest_weight = min(cand_weights.values())
    long_pass = lowest_weight >= -1e-6
    
    # 3. Reserve-eligible weight at least reserve minimum
    reserve_weight = sum(
        weight for name, weight in cand_weights.items()
        if holdings_dict[name]["reserve_eligible"]
    )
    reserve_pass = reserve_weight >= (reserve_min - 1e-6)
    
    # 4. Weight redeemable within liquidity window (days <= LIQUIDITY_WINDOW)
    liquid_weight = sum(
        weight for name, weight in cand_weights.items()
        if holdings_dict[name]["days"] <= LIQUIDITY_WINDOW
    )
    liquid_pass = liquid_weight >= (MIN_LIQUID_SHARE - 1e-6)
    
    # 5. Largest single company at most issuer limit (non-exempt issuers)
    # Cash, Treasury, and diversified funds exempt; one company's securities count together
    company_totals = {}
    for name, weight in cand_weights.items():
        issuer = holdings_dict[name]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_totals[issuer] = company_totals.get(issuer, 0.0) + weight
            
    largest_company = max(company_totals.values()) if company_totals else 0.0
    issuer_pass = largest_company <= (ISSUER_LIMIT + 1e-6)
    
    # Count failed rules
    failed_count = sum([
        not sum_pass,
        not long_pass,
        not reserve_pass,
        not liquid_pass,
        not issuer_pass
    ])
    
    if failed_count == 0:
        verdict = "passes every checkable rule"
    else:
        verdict = f"fails {failed_count} rule(s)"
        
    return {
        "total_weight": total_weight,
        "sum_pass": sum_pass,
        "lowest_weight": lowest_weight,
        "long_pass": long_pass,
        "reserve_weight": reserve_weight,
        "reserve_pass": reserve_pass,
        "liquid_weight": liquid_weight,
        "liquid_pass": liquid_pass,
        "largest_company": largest_company,
        "issuer_pass": issuer_pass,
        "failed_count": failed_count,
        "verdict": verdict,
    }


def main():
    reserve_min = compute_reserve_minimum()
    candidate_names = list(CANDIDATES)
    print(f"Reserve minimum: {reserve_min:.1f}% of the portfolio.\n")
    
    # Detailed output candidate by candidate
    for cand_name in candidate_names:
        cand_weights = CANDIDATES[cand_name]
        res = evaluate_candidate(cand_weights, reserve_min)
        
        print(f"Candidate {cand_name}:")
        print(f"  Weights sum to 100:            {res['total_weight']:.1f} {'pass' if res['sum_pass'] else 'FAIL'}")
        print(f"  Long-only (lowest weight):     {res['lowest_weight']:.1f} {'pass' if res['long_pass'] else 'FAIL'}")
        print(f"  Reserve >= {reserve_min:.1f}%:                {res['reserve_weight']:.1f} {'pass' if res['reserve_pass'] else 'FAIL'}")
        print(f"  Redeemable in {LIQUIDITY_WINDOW} days >= {MIN_LIQUID_SHARE:.0f}%: {res['liquid_weight']:.1f} {'pass' if res['liquid_pass'] else 'FAIL'}")
        print(f"  Largest single company <= {ISSUER_LIMIT:.0f}%:   {res['largest_company']:.1f} {'pass' if res['issuer_pass'] else 'FAIL'}")
        print(f"  Calendar-year loss:            requires CIO clarification")
        print(f"  Verdict:                       {res['verdict']}\n")
        
    # Summary comparison table matching Lab 13 V format
    print("=" * 96)
    print("SUMMARY VERIFICATION TABLE (Lab 13 — V & E)")
    print("=" * 96)
    hdr = " | ".join([f"{'Rule':<30}"] + [f"{name:<18}" for name in candidate_names])
    print(hdr)
    print("-" * 96)
    
    evals = {name: evaluate_candidate(CANDIDATES[name], reserve_min) for name in candidate_names}
    
    def fmt_cell(val, status):
        return f"{val:.1f} {'pass' if status else 'FAIL'}"
        
    checks = [
        ("Weights sum to 100", "total_weight", "sum_pass"),
        ("Long-only (lowest weight)", "lowest_weight", "long_pass"),
        (f"Reserve >= {reserve_min:.1f}%", "reserve_weight", "reserve_pass"),
        ("Redeemable in 5 days >= 90%", "liquid_weight", "liquid_pass"),
        ("Largest single company <= 8%", "largest_company", "issuer_pass"),
    ]
    for label, value_key, pass_key in checks:
        cells = [f"{label:<30}"] + [f"{fmt_cell(evals[name][value_key], evals[name][pass_key]):<18}" for name in candidate_names]
        print(" | ".join(cells))
    print(" | ".join([f"{'Calendar-year loss':<30}"] + [f"{'requires CIO clarification' if name == 'A' else 'same':<18}" for name in candidate_names]))
    print("-" * 96)
    print(" | ".join([f"{'Verdict':<30}"] + [f"{evals[name]['verdict']:<18}" for name in candidate_names]))
    print("=" * 96)

if __name__ == "__main__":
    main()
