"""
Lab 16 — Provenance Gate
Point-in-time filter and signal engine.
Standard library only.
"""

from datetime import datetime

# ---------------------------------------------------------
# Editable inputs
# ---------------------------------------------------------

DECISION_DATE = "2026-03-31"

RAW_DATA = [
    {"row": 1,  "ticker": "AAA", "month": "2026-01", "published_on": "2026-02-10", "index": 101.0},
    {"row": 2,  "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-10", "index": 104.0},
    {"row": 3,  "ticker": "AAA", "month": "2026-03", "published_on": "2026-04-10", "index": 109.0},
    {"row": 4,  "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-25", "index": 103.0},
    {"row": 5,  "ticker": "BBB", "month": "2026-01", "published_on": "2026-02-10", "index": 98.0},
    {"row": 6,  "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 7,  "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 8,  "ticker": "BBB", "month": "2026-03", "published_on": "2026-04-10", "index": 92.0},
    {"row": 9,  "ticker": "CCC", "month": "2026-01", "published_on": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published_on": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "",    "month": "2026-02", "published_on": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published_on": "2026-03-10", "index": 111.0},
]


# ---------------------------------------------------------
# Reusable Rule Functions
# ---------------------------------------------------------

def rule_1_quarantine_no_ticker(rows):
    """
    Rule 1: Quarantine a row with no ticker.
    Returns: (kept_rows, removed_rows)
    """
    kept = []
    removed = []
    for r in rows:
        ticker = (r.get("ticker") or "").strip()
        if not ticker:
            removed.append(r)
        else:
            kept.append(r)
    return kept, removed


def rule_2_remove_duplicates(rows):
    """
    Rule 2: Remove an exact duplicate across (ticker, month, published_on, index).
    Returns: (kept_rows, removed_rows)
    """
    kept = []
    removed = []
    seen = set()
    for r in rows:
        key = (r["ticker"], r["month"], r["published_on"], r["index"])
        if key in seen:
            removed.append(r)
        else:
            seen.add(key)
            kept.append(r)
    return kept, removed


def rule_3_filter_by_decision_date(rows, decision_date):
    """
    Rule 3: Remove a row published after the decision date.
    Returns: (kept_rows, removed_rows)
    """
    kept = []
    removed = []
    for r in rows:
        if r["published_on"] > decision_date:
            removed.append(r)
        else:
            kept.append(r)
    return kept, removed


def rule_4_resolve_revisions(rows):
    """
    Rule 4: Where one ticker and month has two publications, keep the latest
    one published by the decision date (a revision).
    Returns: (kept_rows, removed_rows)
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for r in rows:
        groups[(r["ticker"], r["month"])].append(r)

    kept = []
    removed = []
    for (ticker, month), group_rows in groups.items():
        # Sort by published_on ascending (or row if tie); latest publication is kept
        sorted_group = sorted(group_rows, key=lambda x: (x["published_on"], x["row"]))
        kept.append(sorted_group[-1])
        removed.extend(sorted_group[:-1])

    # Re-sort kept by row number to preserve original table sequence
    kept = sorted(kept, key=lambda x: x["row"])
    removed = sorted(removed, key=lambda x: x["row"])
    return kept, removed


def build_asof_panel(rows, decision_date):
    """
    Applies the four rules in strict order and returns the funnel log and final panel.
    """
    r1_kept, r1_removed = rule_1_quarantine_no_ticker(rows)
    r2_kept, r2_removed = rule_2_remove_duplicates(r1_kept)
    r3_kept, r3_removed = rule_3_filter_by_decision_date(r2_kept, decision_date)
    r4_kept, r4_removed = rule_4_resolve_revisions(r3_kept)

    funnel = [
        ("Quarantined: no ticker", [r["row"] for r in r1_removed]),
        ("Exact duplicate", [r["row"] for r in r2_removed]),
        (f"Published after {decision_date}", [r["row"] for r in r3_removed]),
        ("Older vintage replaced by a revision", [r["row"] for r in r4_removed]),
    ]
    return r4_kept, funnel


# ---------------------------------------------------------
# Signal Calculations
# ---------------------------------------------------------

def get_month_name(month_str):
    """Converts '2026-02' to 'February'."""
    dt = datetime.strptime(month_str, "%Y-%m")
    return dt.strftime("%B")


def compute_ticker_signal(panel_rows, ticker):
    """
    Computes percent change from previous month to latest knowable month for a ticker.
    Returns: (signal_pct, latest_month_str, previous_month_str)
    """
    t_rows = [r for r in panel_rows if r["ticker"] == ticker]
    if len(t_rows) < 2:
        return None
    # Sort chronologically by month measured
    t_rows_sorted = sorted(t_rows, key=lambda x: x["month"])
    prev_row = t_rows_sorted[-2]
    latest_row = t_rows_sorted[-1]
    pct_change = ((latest_row["index"] - prev_row["index"]) / prev_row["index"]) * 100.0
    return pct_change, latest_row["month"]


def compute_signals(panel_rows):
    """
    Computes signals for all tickers present in panel.
    """
    tickers = sorted(list({r["ticker"] for r in panel_rows}))
    results = {}
    for t in tickers:
        sig = compute_ticker_signal(panel_rows, t)
        if sig:
            results[t] = sig
    return results


def compute_naive_signals(raw_rows):
    """
    Naive signal: same calculation using every row's latest publication,
    ignoring publication date.
    Applies Rule 1 (no ticker) and Rule 2 (duplicates), but does NOT filter by date.
    Then resolves revisions using the absolute latest publication for each (ticker, month).
    """
    r1_kept, _ = rule_1_quarantine_no_ticker(raw_rows)
    r2_kept, _ = rule_2_remove_duplicates(r1_kept)
    r4_kept, r4_removed = rule_4_resolve_revisions(r2_kept)
    
    # Check which months were revised across all data
    revised_months = {(r["ticker"], r["month"]) for r in r4_removed}

    tickers = sorted(list({r["ticker"] for r in r4_kept}))
    results = {}
    for t in tickers:
        sig = compute_ticker_signal(r4_kept, t)
        if sig:
            pct_change, latest_month = sig
            is_revised = (t, latest_month) in revised_months
            results[t] = (pct_change, latest_month, is_revised)
    return results


# ---------------------------------------------------------
# Formatting and Output
# ---------------------------------------------------------

def print_results(panel, funnel, asof_signals, naive_signals):
    print("=" * 60)
    print("Lab 16 - Provenance Gate Engine")
    print(f"Decision date: {DECISION_DATE}")
    print("=" * 60)
    print("\nThe row funnel")
    print(f"{'Funnel step':<38} | {'Rows removed'}")
    print("-" * 55)
    for step_name, rows in funnel:
        rows_str = ", ".join(map(str, rows)) if rows else "None"
        print(f"{step_name:<38} | {rows_str}")

    asof_row_nums = [r["row"] for r in panel]
    print(f"{'As-of panel':<38} | {', '.join(map(str, asof_row_nums))}")

    print("\nAs-of panel records:")
    print(f"{'Row':<5} {'Ticker':<8} {'Month':<10} {'Published':<12} {'Index':<8}")
    print("-" * 45)
    for r in panel:
        print(f"{r['row']:<5} {r['ticker']:<8} {r['month']:<10} {r['published_on']:<12} {r['index']:<8.1f}")

    print("\nThe signals")
    print(f"{'Ticker':<8} | {'As-of signal':<22} | {'Naive signal':<28}")
    print("-" * 62)
    tickers = sorted(list(asof_signals.keys()))
    for t in tickers:
        asof_pct, asof_m = asof_signals[t]
        asof_sign = "+" if asof_pct >= 0 else ""
        asof_str = f"{asof_sign}{asof_pct:.2f}% ({get_month_name(asof_m)})"

        naive_pct, naive_m, is_rev = naive_signals[t]
        naive_sign = "+" if naive_pct >= 0 else ""
        rev_tag = ", revised" if (is_rev and naive_m == asof_m) else ""
        naive_str = f"{naive_sign}{naive_pct:.2f}% ({get_month_name(naive_m)}{rev_tag})"

        print(f"{t:<8} | {asof_str:<22} | {naive_str:<28}")
    print("=" * 60)


def main():
    panel, funnel = build_asof_panel(RAW_DATA, DECISION_DATE)
    asof_sigs = compute_signals(panel)
    naive_sigs = compute_naive_signals(RAW_DATA)
    print_results(panel, funnel, asof_sigs, naive_sigs)


if __name__ == "__main__":
    main()
