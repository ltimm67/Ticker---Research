"""Three-Statement Pro-Forma Valuation Model: Marriott International, Inc. (NASDAQ: MAR)
Five-Year Forecast: 2026E to 2030E
Standard-library only.
"""

import sys

# ==============================================================================
# Model Assumptions & Inputs (Marriott International, Inc.)
# ==============================================================================

# Operating Assumptions
# Organic growth anchored on Q2 2026 guidance: RevPAR 3.0%-3.5% + net rooms 4.5%-5.0%
organic_revenue_growth = 0.045  # 4.5% a year [guidance / judgment]
gross_margin = 0.214428  # 21.44% net operating fee margin on total revenue [history]
sga_ratios = [0.154942, 0.152500, 0.150000, 0.150000, 0.150000]  # SG&A / Gross Profit [judgment]
depreciation_ratio = 604.0 / (1954.0 + 21981.0)  # FY2025 D&A / opening (PP&E + intangibles) [history]
impairment_annual = 0.0  # Impairments included in baseline amortization [history]
capex_annual = 600.0  # Capital and technology expenditures, USD millions a year [guidance]
tax_rate = 0.2203  # 22.03% effective tax rate [history]

# Working Capital Assumptions
# Lodging franchisor carries zero merchandise inventory (lodging services)
inventory_days = 0.0  # Stated "None" [history / fact]
floor_plan_ratio = 0.0  # Stated "None" - no automotive dealer floor plan debt [fact]
wc_asset_ratio = 0.12  # Operating current assets (receivables/prepaids) as % of revenue change [history]
wc_liab_ratio = 0.06  # Operating current liabilities (accruals/deferred loyalty) as % of revenue change [history]

# Financing & Liquidity Assumptions
minimum_cash = 300.0  # Operating cash reserve floor, USD millions [judgment]
revolver_limit = 4500.0  # Credit facility capacity, USD millions [fact: 2025 Form 10-K Note 11]
revolver_rate = 0.060  # 6.0% short-term credit facility borrowing rate [judgment]
debt_repayment_annual = 300.0  # Senior notes principal retirement, USD millions a year [judgment]
share_buyback_annual = 2500.0  # Share repurchases + dividends, USD millions a year [guidance / judgment]
term_debt_rate = 0.047314  # Net effective borrowing rate ($767M net interest / $16,211M debt) [history]

# Valuation Assumptions
cost_of_equity = 0.089  # 8.90% cost of equity from Lab 06 CAPM estimate [judgment]
terminal_growth = 0.025  # 2.50% long-run sustainable GDP growth rate [judgment]
shares_outstanding = 273.60  # Diluted weighted-average shares, millions [fact: 2025 Form 10-K Note 3]

# Opening Balance Sheet (FY2025, USD millions)
# Sourced from 2025 Form 10-K, Item 8 Consolidated Balance Sheets
opening_bs = {
    "revenue": 26186.0,
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

years = [2026, 2027, 2028, 2029, 2030]


# ==============================================================================
# Model Engine
# ==============================================================================

def run_proforma():
    is_data = []
    bs_data = []
    cfs_data = []
    checks = []

    prior_rev = opening_bs["revenue"]
    prior_cash = opening_bs["cash"]
    prior_rec = opening_bs["receivables"]
    prior_ppe = opening_bs["ppe"]
    prior_other_assets = opening_bs["other_assets"]
    prior_debt = opening_bs["term_debt"]
    prior_revolver = opening_bs["revolver"]
    prior_other_liab = opening_bs["other_liab"]
    prior_equity = opening_bs["equity"]

    for i, yr in enumerate(years):
        sga_ratio = sga_ratios[i]

        # 1. Income Statement
        revenue = prior_rev * (1.0 + organic_revenue_growth)
        delta_rev = revenue - prior_rev
        gross_profit = revenue * gross_margin
        sga = gross_profit * sga_ratio
        depreciation = (prior_ppe + prior_other_assets) * depreciation_ratio
        impairment = impairment_annual
        operating_income = gross_profit - sga - depreciation - impairment

        interest = prior_debt * term_debt_rate + prior_revolver * revolver_rate
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * tax_rate
        net_income = pretax_income - tax

        # 2. Balance Sheet (except cash)
        delta_rec = delta_rev * 0.08
        rec = prior_rec + delta_rec

        # 40% of D&A applies to physical PP&E, 60% to contract investments/intangibles
        delta_ppe = capex_annual - (depreciation * 0.40)
        ppe = prior_ppe + delta_ppe

        delta_other_assets = (delta_rev * (wc_asset_ratio - 0.08)) - (depreciation * 0.60)
        other_assets = prior_other_assets + delta_other_assets

        debt = prior_debt - debt_repayment_annual

        delta_other_liab = delta_rev * wc_liab_ratio
        other_liab = prior_other_liab + delta_other_liab

        equity = prior_equity + net_income - share_buyback_annual

        # 3. Cash Flow / FCFE & Cash
        delta_wc = (delta_rec + (delta_rev * (wc_asset_ratio - 0.08))) - delta_other_liab
        fcfe = net_income + depreciation - capex_annual - delta_wc - debt_repayment_annual

        cash_before = prior_cash + fcfe - share_buyback_annual

        revolver = prior_revolver
        revolver_draw = 0.0
        revolver_repayment = 0.0

        if cash_before < minimum_cash:
            revolver_draw = min(minimum_cash - cash_before, revolver_limit - revolver)
            revolver += revolver_draw
            cash = cash_before + revolver_draw
        else:
            revolver_repayment = min(revolver, cash_before - minimum_cash)
            revolver -= revolver_repayment
            cash = cash_before - revolver_repayment

        # 4. Balance Sheet Checks
        # Simulate swap and break if flag is passed
        if "--break" in sys.argv and i == 0:
            cash = opening_bs["cash"]  # Hardcode 2026 cash to opening $385.0M instead of computed $315.5M

        total_assets = cash + rec + ppe + other_assets
        total_liab = debt + revolver + other_liab
        total_liab_equity = total_liab + equity
        raw_gap = total_assets - total_liab_equity
        gap = 0.0 if abs(raw_gap) < 1e-4 else raw_gap
        cash_ok = cash >= minimum_cash

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
            "capex": capex_annual,
            "delta_wc": delta_wc,
            "debt_repayment": debt_repayment_annual,
            "fcfe": fcfe,
            "share_buyback": share_buyback_annual,
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


def assert_balanced(checks: list[dict]) -> None:
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
                f"Model cash check failed in FY{yr}E: Cash = ${c['cash']:.1f}M is below minimum ${minimum_cash:.1f}M"
            )


def print_statements(is_data, bs_data, cfs_data, checks):
    hdr = f"{'Line Item (USD Millions)':<36}" + "".join(f"{'FY' + str(y) + 'E':>12}" for y in years)

    print("=" * 96)
    print("1. PRO-FORMA INCOME STATEMENT: MARRIOTT INTERNATIONAL (MAR)")
    print("=" * 96)
    print(hdr)
    print("-" * 96)
    rows_is = [
        ("Total Revenues", [d["revenue"] for d in is_data]),
        ("Net Operating Fee Margin", [d["gross_profit"] for d in is_data]),
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


def perform_valuation(cfs_data):
    fcfe_list = [d["fcfe"] for d in cfs_data]

    # Present value of explicit FCFE (2026-2030) at Cost of Equity (8.90%)
    pv_explicit_fcfe = sum(
        f / (1.0 + cost_of_equity) ** yr for yr, f in enumerate(fcfe_list, start=1)
    )

    # Terminal value at Year 5 (2030) on normalized terminal FCFE
    fcfe_2030 = fcfe_list[-1]
    normalized_terminal_base = fcfe_2030 + debt_repayment_annual
    terminal_value_2030 = (
        normalized_terminal_base * (1.0 + terminal_growth) / (cost_of_equity - terminal_growth)
    )
    pv_terminal_value = terminal_value_2030 / (1.0 + cost_of_equity) ** 5

    equity_value = pv_explicit_fcfe + pv_terminal_value
    value_per_share = equity_value / shares_outstanding
    share_of_value_after_2030 = pv_terminal_value / equity_value

    print("\n" + "=" * 96)
    print("5. FCFE VALUATION SUMMARY: MARRIOTT INTERNATIONAL (MAR)")
    print("=" * 96)
    print(f"PV of explicit FCFE (2026-2030):   ${pv_explicit_fcfe:>10.2f}M")
    print(f"Normalized terminal base FCFE:      ${normalized_terminal_base:>10.2f}M  (2030 FCFE + 2030 repayment)")
    print(f"Terminal value at Year 5 (2030):    ${terminal_value_2030:>10.2f}M")
    print(f"PV of terminal value:               ${pv_terminal_value:>10.2f}M")
    print(f"Equity value:                       ${equity_value:>10.2f}M")
    print(f"Diluted shares outstanding:          {shares_outstanding:>10.2f}M")
    print(f"Value per diluted share:            ${value_per_share:>10.2f}")
    print(f"Share of value after 2030:           {share_of_value_after_2030:>10.2%}")


def main():
    is_data, bs_data, cfs_data, checks = run_proforma()
    print_statements(is_data, bs_data, cfs_data, checks)
    assert_balanced(checks)
    perform_valuation(cfs_data)


if __name__ == "__main__":
    main()

