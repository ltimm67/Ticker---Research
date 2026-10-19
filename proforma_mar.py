"""Three-Statement Pro-Forma Valuation Model: Marriott International, Inc. (NASDAQ: MAR)
Five-Year Forecast: 2026E to 2030E & One-At-A-Time Sensitivity Analysis (Lab 11)
Standard-library only.
"""

import copy
import sys

# ==============================================================================
# Model Base Assumptions & Inputs (Marriott International, Inc.)
# ==============================================================================

BASE_ASSUMPTIONS = {
    # Operating Assumptions
    "organic_revenue_growth": 0.047,  # Base net room growth, 4.7% a year [FY2025 10-K / judgment]
    "gross_margin": 0.48,  # Franchise-fee operating margin [judgment]
    "sga_ratios": [0.154942, 0.152500, 0.150000, 0.150000, 0.150000],  # SG&A / Gross Profit [judgment]
    "depreciation_ratio": 604.0 / (1954.0 + 21981.0),  # FY2025 D&A / opening (PP&E + intangibles) [history]
    "impairment_annual": 0.0,  # Impairments included in baseline amortization [history]
    "capex_annual": 250.0,  # Asset-light corporate capex, USD millions a year [judgment; below $300M]
    "tax_rate": 0.2203,  # 22.03% effective tax rate [history]
    # Working Capital Assumptions (Franchisor carries zero inventory or floor plan debt)
    "inventory_days": 0.0,  # Stated "None" [history / fact]
    "floor_plan_ratio": 0.0,  # Stated "None" - no dealer floor plan debt [fact]
    "wc_asset_ratio": 0.12,  # Operating current assets as % of revenue change [history]
    "wc_liab_ratio": 0.06,  # Operating current liabilities as % of revenue change [history]
    # Financing & Liquidity Assumptions
    "minimum_cash": 300.0,  # Operating cash reserve floor, USD millions [judgment]
    "revolver_limit": 4500.0,  # Credit facility capacity, USD millions [fact: 2025 Form 10-K Note 11]
    "revolver_rate": 0.060,  # 6.0% short-term credit facility borrowing rate [judgment]
    "debt_repayment_annual": 0.0,  # No scheduled principal repayment in the base case [judgment]
    "share_buyback_annual": 500.0,  # Liquidity-limited capital return, USD millions a year [judgment]
    "term_debt_rate": 0.047314,  # Net effective borrowing rate ($767M net interest / $16,211M debt) [history]
    # Valuation Assumptions
    "cost_of_equity": 0.089,  # 8.90% cost of equity from Lab 06 CAPM estimate [judgment]
    "terminal_growth": 0.025,  # 2.50% long-run sustainable GDP growth rate [judgment]
    "shares_outstanding": 273.60,  # Diluted weighted-average shares, millions [fact: 2025 Form 10-K Note 3]
}

# Opening Balance Sheet (FY2025, USD millions)
# Sourced from 2025 Form 10-K, Item 8 Consolidated Balance Sheets
OPENING_BS = {
    "revenue": 5050.0,  # FY2025 total fee revenue used as the forecast revenue base
    "cash": 385.0,
    "receivables": 3156.0,
    "inventory": 0.0,
    "ppe": 1954.0,
    "other_assets": 21981.0,
    "floor_plan": 0.0,
    "term_debt": 16211.0,
    "revolver": 0.0,
    "other_liab": 15107.0,
    "equity": -3842.0,  # Negative book equity due to historical share repurchases
}

YEARS = [2026, 2027, 2028, 2029, 2030]


# ==============================================================================
# Model Engine
# ==============================================================================

def run_proforma(params=None, break_test=False):
    """Run five-year linked three-statement pro-forma engine."""
    if params is None:
        params = copy.deepcopy(BASE_ASSUMPTIONS)

    is_data = []
    bs_data = []
    cfs_data = []
    checks = []

    prior_rev = OPENING_BS["revenue"]
    prior_cash = OPENING_BS["cash"]
    prior_rec = OPENING_BS["receivables"]
    prior_ppe = OPENING_BS["ppe"]
    prior_other_assets = OPENING_BS["other_assets"]
    prior_debt = OPENING_BS["term_debt"]
    prior_revolver = OPENING_BS["revolver"]
    prior_other_liab = OPENING_BS["other_liab"]
    prior_equity = OPENING_BS["equity"]

    for i, yr in enumerate(YEARS):
        sga_ratio = params["sga_ratios"][i]

        # 1. Income Statement
        # Forecast total fee revenue. Reimbursed hotel costs are excluded because they
        # are pass-through items and do not create operating profit.
        revenue = prior_rev * (1.0 + params["organic_revenue_growth"])
        delta_rev = revenue - prior_rev
        gross_profit = revenue * params["gross_margin"]
        sga = gross_profit * sga_ratio
        depreciation = (prior_ppe + prior_other_assets) * params["depreciation_ratio"]
        impairment = params["impairment_annual"]
        operating_income = gross_profit - sga - depreciation - impairment

        interest = prior_debt * params["term_debt_rate"] + prior_revolver * params["revolver_rate"]
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * params["tax_rate"]
        net_income = pretax_income - tax

        # 2. Balance Sheet (except cash)
        delta_rec = delta_rev * 0.08
        rec = prior_rec + delta_rec

        # 40% of D&A applies to physical PP&E, 60% to contract investments/intangibles
        delta_ppe = params["capex_annual"] - (depreciation * 0.40)
        ppe = prior_ppe + delta_ppe

        delta_other_assets = (delta_rev * (params["wc_asset_ratio"] - 0.08)) - (depreciation * 0.60)
        other_assets = prior_other_assets + delta_other_assets

        debt = prior_debt - params["debt_repayment_annual"]

        delta_other_liab = delta_rev * params["wc_liab_ratio"]
        other_liab = prior_other_liab + delta_other_liab

        equity = prior_equity + net_income - params["share_buyback_annual"]

        # 3. Cash Flow / FCFE & Cash
        delta_wc = (delta_rec + (delta_rev * (params["wc_asset_ratio"] - 0.08))) - delta_other_liab
        fcfe = net_income + depreciation - params["capex_annual"] - delta_wc - params["debt_repayment_annual"]

        cash_before = prior_cash + fcfe - params["share_buyback_annual"]

        revolver = prior_revolver
        revolver_draw = 0.0
        revolver_repayment = 0.0

        if cash_before < params["minimum_cash"]:
            revolver_draw = min(params["minimum_cash"] - cash_before, params["revolver_limit"] - revolver)
            revolver += revolver_draw
            cash = cash_before + revolver_draw
        else:
            revolver_repayment = min(revolver, cash_before - params["minimum_cash"])
            revolver -= revolver_repayment
            cash = cash_before - revolver_repayment

        # Intentional break condition for diagnostic check
        if break_test and i == 0:
            cash = OPENING_BS["cash"]

        total_assets = cash + rec + ppe + other_assets
        total_liab = debt + revolver + other_liab
        total_liab_equity = total_liab + equity
        raw_gap = total_assets - total_liab_equity
        gap = 0.0 if abs(raw_gap) < 1e-4 else raw_gap
        cash_ok = cash >= params["minimum_cash"]

        is_data.append({
            "year": yr,
            "revenue": revenue,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "operating_income": operating_income,
            "interest": interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
        })

        bs_data.append({
            "year": yr,
            "cash": cash,
            "receivables": rec,
            "inventory": 0.0,
            "ppe": ppe,
            "other_assets": other_assets,
            "total_assets": total_assets,
            "floor_plan": 0.0,
            "debt": debt,
            "revolver": revolver,
            "other_liab": other_liab,
            "total_liab": total_liab,
            "equity": equity,
            "total_liab_equity": total_liab_equity,
        })

        cfs_data.append({
            "year": yr,
            "net_income": net_income,
            "depreciation": depreciation,
            "capex": params["capex_annual"],
            "delta_wc": delta_wc,
            "debt_repayment": params["debt_repayment_annual"],
            "fcfe": fcfe,
            "share_buyback": params["share_buyback_annual"],
            "revolver_draw": revolver_draw,
            "revolver_repayment": revolver_repayment,
            "ending_cash": cash,
        })

        checks.append({
            "year": yr,
            "gap": gap,
            "cash_ok": cash_ok,
            "cash": cash,
        })

        prior_rev = revenue
        prior_cash = cash
        prior_rec = rec
        prior_ppe = ppe
        prior_other_assets = other_assets
        prior_debt = debt
        prior_revolver = revolver
        prior_other_liab = other_liab
        prior_equity = equity

    return is_data, bs_data, cfs_data, checks


def assert_balanced(checks: list[dict], min_cash: float = 300.0) -> None:
    """Raise an error naming the year and gap if any balance check fails."""
    for c in checks:
        yr = c["year"]
        gap = c["gap"]
        if abs(gap) > 0.001:
            raise AssertionError(
                f"Model balance check failed in FY{yr}E: Assets - Liabilities - Equity gap = {gap:+.4f}"
            )
        if not c["cash_ok"]:
            raise AssertionError(
                f"Model cash check failed in FY{yr}E: Cash = ${c['cash']:.1f}M is below minimum ${min_cash:.1f}M"
            )


def print_statements(is_data, bs_data, cfs_data, checks):
    """Print the three linked financial statements and accounting checks."""
    hdr = f"{'Line Item (USD Millions)':<36}" + "".join(f"{'FY' + str(y) + 'E':>12}" for y in YEARS)

    print("=" * 96)
    print("1. PRO-FORMA INCOME STATEMENT: MARRIOTT INTERNATIONAL (MAR)")
    print("=" * 96)
    print(hdr)
    print("-" * 96)
    rows_is = [
        ("Total fee revenues", [d["revenue"] for d in is_data]),
        ("Fee revenue operating profit", [d["gross_profit"] for d in is_data]),
        ("General & Administrative (SG&A)", [d["sga"] for d in is_data]),
        ("Depreciation & Amortization", [d["depreciation"] for d in is_data]),
        ("Operating Income", [d["operating_income"] for d in is_data]),
        ("Interest Expense, net", [d["interest"] for d in is_data]),
        ("Pretax Income", [d["pretax_income"] for d in is_data]),
        ("Income Tax Provision", [d["tax"] for d in is_data]),
        ("Net Income", [d["net_income"] for d in is_data]),
    ]
    for name, vals in rows_is:
        print(f"{name:<36}" + "".join(f"{v:>12.1f}" for v in vals))

    print("\n" + "=" * 96)
    print("2. PRO-FORMA BALANCE SHEET: MARRIOTT INTERNATIONAL (MAR)")
    print("=" * 96)
    print(hdr)
    print("-" * 96)
    rows_bs = [
        ("Cash and cash equivalents", [d["cash"] for d in bs_data]),
        ("Accounts & notes receivable, net", [d["receivables"] for d in bs_data]),
        ("Merchandise inventory (None)", [d["inventory"] for d in bs_data]),
        ("Property and equipment, net", [d["ppe"] for d in bs_data]),
        ("Intangibles & other assets", [d["other_assets"] for d in bs_data]),
        ("Total Assets", [d["total_assets"] for d in bs_data]),
        ("Floor plan loans (None)", [d["floor_plan"] for d in bs_data]),
        ("Senior notes and term debt", [d["debt"] for d in bs_data]),
        ("Revolving credit facility", [d["revolver"] for d in bs_data]),
        ("Other liabilities & loyalty def.", [d["other_liab"] for d in bs_data]),
        ("Total Liabilities", [d["total_liab"] for d in bs_data]),
        ("Shareholders' Equity (Deficit)", [d["equity"] for d in bs_data]),
        ("Total Liabilities & Equity", [d["total_liab_equity"] for d in bs_data]),
    ]
    for name, vals in rows_bs:
        print(f"{name:<36}" + "".join(f"{v:>12.1f}" for v in vals))

    print("\n" + "=" * 96)
    print("3. PRO-FORMA CASH FLOW & FREE CASH FLOW TO EQUITY (FCFE)")
    print("=" * 96)
    print(hdr)
    print("-" * 96)
    rows_cfs = [
        ("Net Income", [d["net_income"] for d in cfs_data]),
        ("Depreciation & Amortization", [d["depreciation"] for d in cfs_data]),
        ("Capital expenditures (Capex)", [d["capex"] for d in cfs_data]),
        ("Change in net working capital", [d["delta_wc"] for d in cfs_data]),
        ("Term debt repayment", [d["debt_repayment"] for d in cfs_data]),
        ("Free Cash Flow to Equity (FCFE)", [d["fcfe"] for d in cfs_data]),
        ("Share repurchases & dividends", [d["share_buyback"] for d in cfs_data]),
        ("Revolver draw / (repayment)", [d["revolver_draw"] - d["revolver_repayment"] for d in cfs_data]),
        ("Cash, year end", [d["ending_cash"] for d in cfs_data]),
    ]
    for name, vals in rows_cfs:
        print(f"{name:<36}" + "".join(f"{v:>12.1f}" for v in vals))

    print("\n" + "=" * 96)
    print("4. BALANCE SHEET INTEGRITY & CASH CHECKS")
    print("=" * 96)
    print(hdr)
    print("-" * 96)
    print(f"{'Assets - liabilities - equity':<36}" + "".join(f"{c['gap']:>12.1f}" for c in checks))
    print(f"{'Cash at or above minimum ($300M)':<36}" + "".join(f"{'OK':>12}" if c['cash_ok'] else f"{'FAIL':>12}" for c in checks))


def perform_valuation(cfs_data, params=None, verbose=True):
    """Value equity as discounted FCFE plus Gordon Growth terminal value."""
    if params is None:
        params = BASE_ASSUMPTIONS

    fcfe_list = [d["fcfe"] for d in cfs_data]
    cost_of_equity = params["cost_of_equity"]
    terminal_growth = params["terminal_growth"]
    shares = params["shares_outstanding"]
    debt_repay = params["debt_repayment_annual"]

    # Present value of explicit FCFE (2026-2030) at Cost of Equity (8.90%)
    pv_explicit_fcfe = sum(
        f / (1.0 + cost_of_equity) ** yr for yr, f in enumerate(fcfe_list, start=1)
    )

    # Terminal value at Year 5 (2030) on normalized terminal FCFE
    fcfe_2030 = fcfe_list[-1]
    normalized_terminal_base = fcfe_2030 + debt_repay
    terminal_value_2030 = (
        normalized_terminal_base * (1.0 + terminal_growth) / (cost_of_equity - terminal_growth)
    )
    pv_terminal_value = terminal_value_2030 / (1.0 + cost_of_equity) ** 5

    equity_value = pv_explicit_fcfe + pv_terminal_value
    value_per_share = equity_value / shares
    share_of_value_after_2030 = pv_terminal_value / equity_value

    if verbose:
        print("\n" + "=" * 96)
        print("5. FCFE VALUATION SUMMARY: MARRIOTT INTERNATIONAL (MAR)")
        print("=" * 96)
        print(f"PV of explicit FCFE (2026-2030):   ${pv_explicit_fcfe:>10.2f}M")
        print(f"Normalized terminal base FCFE:      ${normalized_terminal_base:>10.2f}M  (2030 FCFE + 2030 repayment)")
        print(f"Terminal value at Year 5 (2030):    ${terminal_value_2030:>10.2f}M")
        print(f"PV of terminal value:               ${pv_terminal_value:>10.2f}M")
        print(f"Equity value:                       ${equity_value:>10.2f}M")
        print(f"Diluted shares outstanding:          {shares:>10.2f}M")
        print(f"Value per diluted share:            ${value_per_share:>10.2f}")
        print(f"Share of value after 2030:           {share_of_value_after_2030:>10.2%}")

    return {
        "pv_explicit_fcfe": pv_explicit_fcfe,
        "normalized_terminal_base": normalized_terminal_base,
        "terminal_value_2030": terminal_value_2030,
        "pv_terminal_value": pv_terminal_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
        "share_of_value_after_2030": share_of_value_after_2030,
    }


# ==============================================================================
# One-At-A-Time Sensitivity Engine (Lab 11)
# ==============================================================================

def run_sensitivity_analysis():
    """Execute one-at-a-time sensitivity across two independent operating drivers."""
    print("\n" + "=" * 96)
    print("6. ONE-AT-A-TIME SENSITIVITY ANALYSIS (LAB 11)")
    print("=" * 96)

    drivers = [
        {
            "name": "Net Room Growth",
            "key": "organic_revenue_growth",
            "unit": "% / yr",
            "format": lambda x: f"{x * 100:.1f}%",
            "cases": [
                ("Lower", 0.030),
                ("Base", 0.047),
                ("Higher", 0.060),
            ],
            "reason": "Range of 3.0% to 6.0% tests lower development delivery versus stronger net room additions.",
        },
        {
            "name": "Franchise Fee Margin",
            "key": "gross_margin",
            "unit": "% of rev",
            "format": lambda x: f"{x * 100:.2f}%",
            "cases": [
                ("Lower", 0.45),
                ("Base", 0.48),
                ("Higher", 0.51),
            ],
            "reason": "Range of 45.0% to 51.0% tests franchise-fee yield and operating leverage.",
        },
    ]

    base_op_income = None
    base_fcfe = None
    base_vps = None

    for d in drivers:
        print(f"\nDriver: {d['name']} (Unit: {d['unit']})")
        print(f"Rationale: {d['reason']}")
        print("-" * 96)
        hdr = (
            f"{'Run / Case':<10}"
            f"{'Input Value':<14}"
            f"{'2030 Op Income':<18}"
            f"{'2030 FCFE (FCFE)':<18}"
            f"{'Value / Share':<16}"
            f"{'Checks':<8}"
        )
        print(hdr)
        print("-" * 96)

        results = []
        for case_label, val in d["cases"]:
            # Fresh independent copy for every run
            run_params = copy.deepcopy(BASE_ASSUMPTIONS)
            run_params[d["key"]] = val

            # Run pro-forma engine
            is_data, bs_data, cfs_data, checks = run_proforma(run_params)

            # Check integrity
            checks_passed = True
            try:
                assert_balanced(checks, min_cash=run_params["minimum_cash"])
            except AssertionError:
                checks_passed = False

            # Valuation
            val_res = perform_valuation(cfs_data, params=run_params, verbose=False)

            op_inc_2030 = is_data[-1]["operating_income"]
            fcfe_2030 = cfs_data[-1]["fcfe"]
            vps = val_res["value_per_share"]

            if case_label == "Base":
                base_op_income = op_inc_2030
                base_fcfe = fcfe_2030
                base_vps = vps

            results.append({
                "case": case_label,
                "input_val": val,
                "input_str": d["format"](val),
                "op_income": op_inc_2030,
                "fcfe": fcfe_2030,
                "vps": vps,
                "checks": "PASS" if checks_passed else "FAIL",
            })

            print(
                f"{case_label:<10}"
                f"{d['format'](val):<14}"
                f"${op_inc_2030:>10.1f}M       "
                f"${fcfe_2030:>10.1f}M       "
                f"${vps:>8.2f}         "
                f"{'PASS' if checks_passed else 'FAIL':<8}"
            )

        # Signed changes and spans
        lower_res = next(r for r in results if r["case"] == "Lower")
        base_res = next(r for r in results if r["case"] == "Base")
        higher_res = next(r for r in results if r["case"] == "Higher")

        diff_op_lower = lower_res["op_income"] - base_res["op_income"]
        diff_op_higher = higher_res["op_income"] - base_res["op_income"]
        span_op = higher_res["op_income"] - lower_res["op_income"]

        diff_fcfe_lower = lower_res["fcfe"] - base_res["fcfe"]
        diff_fcfe_higher = higher_res["fcfe"] - base_res["fcfe"]
        span_fcfe = higher_res["fcfe"] - lower_res["fcfe"]

        diff_vps_lower = lower_res["vps"] - base_res["vps"]
        diff_vps_higher = higher_res["vps"] - base_res["vps"]
        span_vps = higher_res["vps"] - lower_res["vps"]

        print("-" * 96)
        print("Signed Changes from Base:")
        print(
            f"  * Lower  ({lower_res['input_str']}): "
            f"Op Income = {diff_op_lower:+.1f}M | "
            f"FCFE = {diff_fcfe_lower:+.1f}M | "
            f"Value/Share = ${diff_vps_lower:+.2f}"
        )
        print(
            f"  * Higher ({higher_res['input_str']}): "
            f"Op Income = {diff_op_higher:+.1f}M | "
            f"FCFE = {diff_fcfe_higher:+.1f}M | "
            f"Value/Share = ${diff_vps_higher:+.2f}"
        )
        print(
            f"  * Output Span (High - Low): "
            f"Op Income Span = ${span_op:.1f}M | "
            f"FCFE Span = ${span_fcfe:.1f}M | "
            f"Value Span = ${span_vps:.2f}/share"
        )


def verify_restored_base(initial_op_inc, initial_fcfe, initial_vps):
    """Restore base inputs and verify they match the initial run exactly."""
    print("\n" + "=" * 96)
    print("7. RESTORED BASE CHECK (LAB 11 INTEGRITY TEST)")
    print("=" * 96)

    restored_params = copy.deepcopy(BASE_ASSUMPTIONS)
    is_data, bs_data, cfs_data, checks = run_proforma(restored_params)
    assert_balanced(checks, min_cash=restored_params["minimum_cash"])
    val_res = perform_valuation(cfs_data, params=restored_params, verbose=False)

    restored_op_inc = is_data[-1]["operating_income"]
    restored_fcfe = cfs_data[-1]["fcfe"]
    restored_vps = val_res["value_per_share"]

    delta_op = abs(restored_op_inc - initial_op_inc)
    delta_fcfe = abs(restored_fcfe - initial_fcfe)
    delta_vps = abs(restored_vps - initial_vps)

    print(f"Initial Base 2030 Op Income:  ${initial_op_inc:.2f}M  | Restored: ${restored_op_inc:.2f}M  | Gap: {delta_op:.4f}")
    print(f"Initial Base 2030 FCFE:       ${initial_fcfe:.2f}M  | Restored: ${restored_fcfe:.2f}M  | Gap: {delta_fcfe:.4f}")
    print(f"Initial Base Value Per Share: ${initial_vps:.2f}    | Restored: ${restored_vps:.2f}    | Gap: {delta_vps:.4f}")

    if delta_op < 1e-3 and delta_fcfe < 1e-3 and delta_vps < 1e-3:
        print("[PASS] Restored Base Check: All inputs, statements, and outputs match initial run exactly.")
    else:
        raise AssertionError("Restored base run failed to match initial run.")


def main():
    break_test = "--break" in sys.argv

    # 1. Run Base Model
    is_data, bs_data, cfs_data, checks = run_proforma(break_test=break_test)
    print_statements(is_data, bs_data, cfs_data, checks)
    assert_balanced(checks)
    val_res = perform_valuation(cfs_data)

    initial_op_inc = is_data[-1]["operating_income"]
    initial_fcfe = cfs_data[-1]["fcfe"]
    initial_vps = val_res["value_per_share"]

    # 2. Run Sensitivity Analysis
    run_sensitivity_analysis()

    # 3. Verify Restored Base
    verify_restored_base(initial_op_inc, initial_fcfe, initial_vps)


if __name__ == "__main__":
    main()
