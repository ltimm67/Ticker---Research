"""Comparable-Company Valuation Model: P/E Multiple Analysis
Case: Asbury Automotive Group (NYSE: ABG)
Standard-library only.
"""

from statistics import median

# ==============================================================================
# Editable Inputs
# ==============================================================================

# Target Company (Asbury Automotive Group)
target_company = {
    "ticker": "ABG",
    "name": "Asbury Automotive Group",
    "price": 243.03,  # Closing price Dec 31, 2024
    "eps": 21.50,    # FY2024 total GAAP diluted EPS
}

# Candidate Peers
candidate_peers = [
    {
        "ticker": "AN",
        "name": "AutoNation",
        "price": 169.84,  # Closing price Dec 31, 2024
        "eps": 16.92,    # FY2024 total GAAP diluted EPS
    },
    {
        "ticker": "GPI",
        "name": "Group 1 Automotive",
        "price": 421.48,  # Closing price Dec 31, 2024
        "eps": 36.81,    # FY2024 total GAAP diluted EPS
    },
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
    """Deduplicate peers by ticker and exclude target company."""
    seen = set()
    cleaned = []
    target_clean = target_ticker.strip().upper()

    for p in peers:
        ticker = p.get("ticker", "").strip().upper()
        if not ticker or ticker == target_clean or ticker in seen:
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
    print("=" * 72)
    print(f"Comparable-Company Valuation: P/E Multiple Analysis")
    print(f"Target: {target_company['name']} ({target_company['ticker']})")
    print(f"Target Share Price: {format_price(target_company['price'])}")
    print(f"Target Diluted EPS: {format_price(target_company['eps'])}")
    print("=" * 72)

    # Validate target inputs
    target_eps = target_company.get("eps")
    target_eps_valid = target_eps is not None and target_eps > 0
    if not target_eps_valid:
        print("Notice: Target diluted EPS is missing or nonpositive; implied prices are not meaningful.\n")

    # Clean peers: deduplicate and exclude target
    valid_peers = clean_peers(target_company["ticker"], candidate_peers)

    # Compute P/E for each peer
    peer_data = []
    for p in valid_peers:
        pe = calculate_pe(p.get("price"), p.get("eps"))
        peer_data.append({
            "ticker": p["ticker"],
            "name": p["name"],
            "price": p.get("price"),
            "eps": p.get("eps"),
            "pe": pe,
        })

    # Print individual peer multiples
    print("\nCandidate Peer Multiples:")
    print(f"{'Ticker':<8} {'Name':<24} {'Price':>10} {'EPS':>10} {'P/E Multiple':>16}")
    print("-" * 72)
    for p in peer_data:
        pe_str = format_multiple(p["pe"])
        print(f"{p['ticker']:<8} {p['name']:<24} {format_price(p['price']):>10} {format_price(p['eps']):>10} {pe_str:>16}")

    # Usable peers have positive P/E
    usable_peers = [p for p in peer_data if p["pe"] is not None]
    n_usable = len(usable_peers)

    print("-" * 72)
    print(f"\nSummary Valuation Statistics ({n_usable} usable peer{'s' if n_usable != 1 else ''}):")

    if n_usable == 0:
        print("Result: No usable peers. Implied valuation cannot be calculated.")
        return

    pe_values = [p["pe"] for p in usable_peers]
    med_pe = median(pe_values)
    min_pe = min(pe_values)
    max_pe = max(pe_values)

    full_med_implied_price = med_pe * target_eps if target_eps_valid else None
    min_implied_price = min_pe * target_eps if target_eps_valid else None
    max_implied_price = max_pe * target_eps if target_eps_valid else None

    print(f"Peer median P/E:        {format_multiple(med_pe)}")

    if n_usable == 1:
        print(f"Peer P/E range:         Single peer ({format_multiple(med_pe)}) — reference estimate, no range")
        print(f"Implied share price:    {format_price(full_med_implied_price)} (reference estimate, no range)")
    else:
        print(f"Peer P/E range:         {format_multiple(min_pe)} to {format_multiple(max_pe)}")
        print(f"Peer-implied range:     {format_price(min_implied_price)} - {format_price(max_implied_price)}")
        print(f"At peer median:         {format_price(full_med_implied_price)}")

    # Leave-one-out sensitivity analysis
    print("\n" + "=" * 72)
    print("Leave-One-Peer-Out Sensitivity Analysis")
    print("=" * 72)

    if n_usable < 2:
        print("Sensitivity analysis requires at least 2 usable peers.")
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

