"""Comparable-Company Valuation Model: P/E Multiple Analysis
Target: Marriott International, Inc. (NASDAQ: MAR)
Candidate Peers: Hilton Worldwide Holdings (HLT), Hyatt Hotels (H), Wyndham Hotels & Resorts (WH)
Standard-library only.
"""

import sys
from statistics import median

# ==============================================================================
# Editable Inputs (Marriott International & Candidate Peers)
# Valuation Date: September 10, 2026
# ==============================================================================

# Target Company
target_company = {
    "ticker": "MAR",
    "name": "Marriott International, Inc.",
    "price": 335.50,  # Closing price Sept 10, 2026 (Nasdaq Real-Time)
    "eps": 9.51,     # FY2025 total GAAP diluted EPS (2025 Form 10-K, Item 8)
}

# Candidate Peers (Valuation Date: Sept 10, 2026, Public FY2025 Annual 10-K EPS)
candidate_peers = [
    {
        "ticker": "HLT",
        "name": "Hilton Worldwide Holdings Inc.",
        "price": 306.24,  # Closing price Sept 10, 2026
        "eps": 6.12,     # FY2025 GAAP diluted EPS (2025 Form 10-K filed Feb 11, 2026)
        "policy": "Use",  # Pure-play asset-light global lodging peer
    },
    {
        "ticker": "H",
        "name": "Hyatt Hotels Corporation",
        "price": 163.07,  # Closing price Sept 10, 2026
        "eps": -0.55,    # FY2025 GAAP diluted EPS (2025 Form 10-K filed Feb 13, 2026)
        "policy": "Qualify",  # Global hospitality peer; negative GAAP EPS makes P/E unusable
    },
    {
        "ticker": "WH",
        "name": "Wyndham Hotels & Resorts, Inc.",
        "price": 69.80,  # Closing price Sept 10, 2026
        "eps": 2.50,     # FY2025 GAAP diluted EPS (2025 Form 10-K filed Feb 19, 2026)
        "policy": "Qualify",  # Pure franchise model, but economy/midscale select service focus
    },
]

# Support running Asbury case validation via --asbury flag
if "--asbury" in sys.argv:
    target_company = {
        "ticker": "ABG",
        "name": "Asbury Automotive Group",
        "price": 243.03,
        "eps": 21.50,
    }
    candidate_peers = [
        {"ticker": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92, "policy": "Use"},
        {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81, "policy": "Qualify"},
    ]


# ==============================================================================
# Helper Functions & Core Logic
# ==============================================================================

def format_multiple(val: float | None) -> str:
    """Format a multiple to six decimal places or label not meaningful."""
    if val is None:
        return "not meaningful"
    return f"{val:.6f}x"


def format_price(val: float | None) -> str:
    """Format a price to cents ($0.01) or label not meaningful."""
    if val is None:
        return "not meaningful"
    return f"${val:,.2f}"


def format_change(val: float | None) -> str:
    """Format a dollar change to cents with explicit sign."""
    if val is None:
        return "not meaningful"
    sign = "+" if val > 0 else ("-" if val < 0 else " ")
    return f"{sign}${abs(val):,.2f}"


def clean_peers(target_ticker: str, peers: list[dict]) -> list[dict]:
    """Deduplicate peers by ticker, exclude target company, and retain Use/Qualify peers."""
    seen = set()
    cleaned = []
    target_clean = target_ticker.strip().upper()

    for p in peers:
        ticker = p.get("ticker", "").strip().upper()
        if not ticker or ticker == target_clean or ticker in seen:
            continue
        # Exclude peers marked 'Exclude' from calculation
        if p.get("policy", "").strip().lower() == "exclude":
            continue
        seen.add(ticker)
        cleaned.append(p)
    return cleaned


def calculate_pe(price: float | None, eps: float | None) -> float | None:
    """Compute P/E multiple = price / diluted EPS. Return None if nonpositive/missing."""
    if price is None or eps is None or price <= 0 or eps <= 0:
        return None
    return price / eps


def run_comparable_analysis() -> None:
    print("=" * 76)
    print("Comparable-Company Valuation: P/E Multiple Analysis")
    print(f"Target: {target_company['name']} ({target_company['ticker']})")
    print(f"Valuation Date: September 10, 2026")
    print(f"Target Share Price: {format_price(target_company['price'])}")
    print(f"Target Diluted EPS: {format_price(target_company['eps'])}")
    print("=" * 76)

    target_eps = target_company.get("eps")
    target_eps_valid = target_eps is not None and target_eps > 0
    if not target_eps_valid:
        print("Notice: Target diluted EPS is missing or nonpositive; implied prices are not meaningful.\n")

    valid_peers = clean_peers(target_company["ticker"], candidate_peers)

    peer_data = []
    for p in valid_peers:
        pe = calculate_pe(p.get("price"), p.get("eps"))
        peer_data.append({
            "ticker": p["ticker"],
            "name": p["name"],
            "price": p.get("price"),
            "eps": p.get("eps"),
            "policy": p.get("policy", "Use"),
            "pe": pe,
        })

    print("\nCandidate Peer Multiples:")
    print(f"{'Ticker':<8} {'Name':<32} {'Policy':<10} {'Price':>10} {'EPS':>10} {'P/E Multiple':>16}")
    print("-" * 92)
    for p in peer_data:
        pe_str = format_multiple(p["pe"])
        eps_str = format_price(p["eps"]) if (p["eps"] is not None and p["eps"] >= 0) else (f"-${abs(p['eps']):.2f}" if p["eps"] is not None else "missing")
        print(f"{p['ticker']:<8} {p['name']:<32} {p['policy']:<10} {format_price(p['price']):>10} {eps_str:>10} {pe_str:>16}")

    usable_peers = [p for p in peer_data if p["pe"] is not None]
    n_usable = len(usable_peers)

    print("-" * 92)
    print(f"\nSummary Valuation Statistics ({n_usable} usable peer{'s' if n_usable != 1 else ''}):")

    if n_usable == 0:
        print("Result: No usable peers (candidate earnings are nonpositive or missing). Implied valuation cannot be calculated.")
        return

    pe_values = [p["pe"] for p in usable_peers]
    med_pe = median(pe_values)
    min_pe = min(pe_values)
    max_pe = max(pe_values)

    full_med_implied_price = med_pe * target_eps if target_eps_valid else None
    min_implied_price = min_pe * target_eps if target_eps_valid else None
    max_implied_price = max_pe * target_eps if target_eps_valid else None

    print(f"Target Diluted EPS:     {format_price(target_eps)}")
    print(f"Peer Median P/E:        {format_multiple(med_pe)}")

    if n_usable == 1:
        print(f"Peer P/E Range:         Single usable peer ({usable_peers[0]['ticker']} at {format_multiple(med_pe)}) — reference estimate, no range")
        print(f"Implied Share Price:    {format_price(full_med_implied_price)} (single-peer reference estimate)")
    else:
        print(f"Peer P/E Range:         {format_multiple(min_pe)} to {format_multiple(max_pe)}")
        print(f"Peer-Implied Range:     {format_price(min_implied_price)} - {format_price(max_implied_price)}")
        print(f"At Peer Median:         {format_price(full_med_implied_price)}")

    # Leave-one-out sensitivity analysis
    print("\n" + "=" * 76)
    print("Leave-One-Peer-Out Sensitivity Analysis")
    print("=" * 76)

    if n_usable < 2:
        print(f"Sensitivity analysis: Only 1 usable peer ({usable_peers[0]['ticker']}). Removing it leaves no usable peers — no estimate.")
        return

    for removed in usable_peers:
        remaining = [p for p in usable_peers if p["ticker"] != removed["ticker"]]
        if not remaining:
            print(f"Remove {removed['ticker']}: No remaining peers — no estimate.")
            continue

        rem_pes = [p["pe"] for p in remaining]
        rem_med_pe = median(rem_pes)
        rem_price = rem_med_pe * target_eps if target_eps_valid else None

        if full_med_implied_price is not None and rem_price is not None:
            diff = rem_price - full_med_implied_price
            diff_str = format_change(diff)
        else:
            diff_str = "not meaningful"

        rem_names = ", ".join(p["ticker"] for p in remaining)
        print(f"Remove {removed['ticker']:<4} ({removed['name']}):")
        print(f"  Remaining peer(s):          {rem_names}")
        print(f"  Remaining median P/E:       {format_multiple(rem_med_pe)}")
        print(f"  Remaining implied price:    {format_price(rem_price)}")
        print(f"  Dollar change from median:  {diff_str}")
        print()


def main() -> None:
    run_comparable_analysis()


if __name__ == "__main__":
    main()
