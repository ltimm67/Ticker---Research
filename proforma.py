"""Three-Statement Pro-Forma Valuation Model: Asbury Automotive Group (NYSE: ABG)
Five-Year Forecast: 2026E to 2030E
Standard-library only.
"""

# ==============================================================================
# Model Assumptions & Inputs
# ==============================================================================

# Operating Assumptions
organic_revenue_growth = 0.018  # 1.8% a year [judgment]
gross_margin = 0.1705  # 17.05% [judgment]
sga_ratios = [0.665, 0.655, 0.645, 0.645, 0.645]  # SG&A / Gross Profit 2026-2030 [judgment]
depreciation_ratio = 82.4 / 3070.4  # FY2025 depreciation / opening PP&E [history]
impairment_annual = 120.0  # USD millions a year (non-cash) [judgment]
capex_annual = 250.0  # USD millions a year [guidance]
tax_rate = 0.255  # 25.5% [judgment]

# Working Capital Assumptions
# Inventory days = FY2025 inventory / cost of sales * 365 [history]
inventory_days = 2135.8 / (17999.0 - 3071.7) * 365
floor_plan_ratio = 2027.0 / 2135.8  # Floor plan loans / inventory [history]
other_wc_ratio = 0.008  # 0.8% of change in revenue [judgment]

# Financing & Liquidity Assumptions
minimum_cash = 25.0  # USD millions [history]
revolver_limit = 850.0  # USD millions [judgment]
revolver_rate = 0.06  # 6.0% [judgment]
debt_repayment_annual = 150.0  # USD millions a year [judgment]
share_buyback_annual = 150.0  # USD millions a year [judgment]
floor_plan_rate = 0.0467  # 4.67% [history]
term_debt_rate = 0.0544  # 5.44% [history]

# Valuation Assumptions
cost_of_equity = 0.10  # 10.0% [judgment]
terminal_growth = 0.025  # 2.5% [judgment]
shares_outstanding = 17.951349  # Millions of shares [fact: 10-Q, 30 June 2026]

# Opening Balance Sheet (FY2025, USD millions)
opening_bs = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liab": 2127.5,
    "equity": 3891.7,
}

years = [2026, 2027, 2028, 2029, 2030]


# ==============================================================================
# Model Engine
# ==============================================================================

def run_proforma():
    # Containers for results across years
    is_data = []
    bs_data = []
    cfs_data = []
    checks = []

    # State variables tracking opening balances
    prior_rev = opening_bs["revenue"]
    prior_inv = opening_bs["inventory"]
    prior_ppe = opening_bs["ppe"]
    prior_other_assets = opening_bs["other_assets"]
    prior_cash = opening_bs["cash"]
    prior_fp = opening_bs["floor_plan"]
    prior_debt = opening_bs["term_debt"]
    prior_revolver = opening_bs["revolver"]
    prior_other_liab = opening_bs["other_liab"]
    prior_equity = opening_bs["equity"]

    for i, yr in enumerate(years):
        sga_ratio = sga_ratios[i]

        # ----------------------------------------------------------------------
        # 1. Income Statement
        # ----------------------------------------------------------------------
        revenue = prior_rev * (1.0 + organic_revenue_growth)
        gross_profit = revenue * gross_margin
        sga = gross_profit * sga_ratio
        depreciation = prior_ppe * depreciation_ratio
        impairment = impairment_annual
        operating_income = gross_profit - sga - depreciation - impairment

        interest = (
            prior_fp * floor_plan_rate
            + prior_debt * term_debt_rate
            + prior_revolver * revolver_rate
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * tax_rate
        net_income = pretax_income - tax

        # ----------------------------------------------------------------------
        # 2. Balance Sheet (except cash)
        # ----------------------------------------------------------------------
        cogs = revenue - gross_profit
        inventory = cogs * inventory_days / 365.0
        floor_plan = inventory * floor_plan_ratio
        ppe = prior_ppe + capex_annual - depreciation
        delta_rev = revenue - prior_rev
        other_assets = prior_other_assets + other_wc_ratio * delta_rev - impairment
        debt = prior_debt - debt_repayment_annual
        other_liab = prior_other_liab  # flat
        equity = prior_equity + net_income - share_buyback_annual

        # ----------------------------------------------------------------------
        # 3. Cash Flow / FCFE & Cash
        # ----------------------------------------------------------------------
        delta_inv = inventory - prior_inv
        delta_owc = other_wc_ratio * delta_rev
        delta_fp = floor_plan - prior_fp

        fcfe = (
            net_income
            + depreciation
            + impairment
            - capex_annual
            - delta_inv
            - delta_owc
            + delta_fp
            - debt_repayment_annual
        )

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

        # ----------------------------------------------------------------------
        # 4. Balance Sheet Checks
        # ----------------------------------------------------------------------
        total_assets = cash + inventory + ppe + other_assets
        total_liab = floor_plan + debt + revolver + other_liab
        total_liab_equity = total_liab + equity
        gap = total_assets - total_liab_equity
        cash_ok = cash >= minimum_cash

        # Store records
        is_data.append({
            "year": yr,
            "revenue": revenue,
            "cogs": cogs,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "impairment": impairment,
            "operating_income": operating_income,
            "interest": interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
        })

        bs_data.append({
            "year": yr,
            "cash": cash,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "total_assets": total_assets,
            "floor_plan": floor_plan,
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
            "impairment": impairment,
            "capex": capex_annual,
            "delta_inv": delta_inv,
            "delta_owc": delta_owc,
            "delta_fp": delta_fp,
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

        # Advance state to next year
        prior_rev = revenue
        prior_inv = inventory
        prior_ppe = ppe
        prior_other_assets = other_assets
        prior_cash = cash
        prior_fp = floor_plan
        prior_debt = debt
        prior_revolver = revolver
        prior_other_liab = other_liab
        prior_equity = equity

    return is_data, bs_data, cfs_data, checks


def assert_balanced(checks: list[dict]) -> None:
    """Raise an error naming the year and gap if any check fails."""
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
    print("1. PRO-FORMA INCOME STATEMENT")
    print("=" * 96)
    print(hdr)
    print("-" * 96)
    rows_is = [
        ("Revenue", [d["revenue"] for d in is_data]),
        ("Gross profit", [d["gross_profit"] for d in is_data]),
        ("SG&A expense", [d["sga"] for d in is_data]),
        ("Depreciation", [d["depreciation"] for d in is_data]),
        ("Impairment (non-cash)", [d["impairment"] for d in is_data]),
        ("Operating income", [d["operating_income"] for d in is_data]),
        ("Interest expense", [d["interest"] for d in is_data]),
        ("Pretax income", [d["pretax_income"] for d in is_data]),
        ("Income tax expense", [d["tax"] for d in is_data]),
        ("Net income", [d["net_income"] for d in is_data]),
    ]
    for name, vals in rows_is:
        print(f"{name:<36}" + "".join(f"{v:>12.1f}" for v in vals))

    print("\n" + "=" * 96)
    print("2. PRO-FORMA BALANCE SHEET")
    print("=" * 96)
    print(hdr)
    print("-" * 96)
    rows_bs = [
        ("Cash and equivalents", [d["cash"] for d in bs_data]),
        ("Inventory", [d["inventory"] for d in bs_data]),
        ("Property, plant & equipment", [d["ppe"] for d in bs_data]),
        ("Other assets", [d["other_assets"] for d in bs_data]),
        ("Total Assets", [d["total_assets"] for d in bs_data]),
        ("Floor plan notes payable", [d["floor_plan"] for d in bs_data]),
        ("Term debt", [d["debt"] for d in bs_data]),
        ("Revolving credit facility", [d["revolver"] for d in bs_data]),
        ("Other liabilities", [d["other_liab"] for d in bs_data]),
        ("Total Liabilities", [d["total_liab"] for d in bs_data]),
        ("Common Equity", [d["equity"] for d in bs_data]),
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
        ("Net income", [d["net_income"] for d in cfs_data]),
        ("Depreciation", [d["depreciation"] for d in cfs_data]),
        ("Impairment (non-cash)", [d["impairment"] for d in cfs_data]),
        ("Capital expenditures (Capex)", [d["capex"] for d in cfs_data]),
        ("Change in inventory", [d["delta_inv"] for d in cfs_data]),
        ("Change in other working capital", [d["delta_owc"] for d in cfs_data]),
        ("Change in floor plan notes", [d["delta_fp"] for d in cfs_data]),
        ("Term debt repayment", [d["debt_repayment"] for d in cfs_data]),
        ("Free cash flow to equity (FCFE)", [d["fcfe"] for d in cfs_data]),
        ("Share buybacks", [d["share_buyback"] for d in cfs_data]),
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
    print(f"{'Cash at or above minimum ($25M)':<36}" + "".join(f"{'OK':>12}" if c['cash_ok'] else f"{'FAIL':>12}" for c in checks))


def perform_valuation(cfs_data):
    fcfe_list = [d["fcfe"] for d in cfs_data]

    # Present value of the explicit 5-year FCFE at cost of equity
    pv_explicit_fcfe = sum(
        f / (1.0 + cost_of_equity) ** yr for yr, f in enumerate(fcfe_list, start=1)
    )

    # Terminal value at end of 2030
    # Formula: (2030 FCFE + 2030 repayment) * (1 + terminal_growth) / (cost_of_equity - terminal_growth)
    fcfe_2030 = fcfe_list[-1]
    repayment_2030 = debt_repayment_annual
    normalized_terminal_base = fcfe_2030 + repayment_2030
    terminal_value_2030 = (
        normalized_terminal_base * (1.0 + terminal_growth) / (cost_of_equity - terminal_growth)
    )
    pv_terminal_value = terminal_value_2030 / (1.0 + cost_of_equity) ** 5

    equity_value = pv_explicit_fcfe + pv_terminal_value
    value_per_share = equity_value / shares_outstanding
    share_of_value_after_2030 = pv_terminal_value / equity_value

    print("\n" + "=" * 96)
    print("5. FCFE VALUATION SUMMARY")
    print("=" * 96)
    print(f"PV of explicit FCFE (2026-2030):   ${pv_explicit_fcfe:>10.2f}M")
    print(f"Normalized terminal base FCFE:      ${normalized_terminal_base:>10.2f}M  (2030 FCFE + 2030 repayment)")
    print(f"Terminal value at Year 5 (2030):    ${terminal_value_2030:>10.2f}M")
    print(f"PV of terminal value:               ${pv_terminal_value:>10.2f}M")
    print(f"Equity value:                       ${equity_value:>10.2f}M")
    print(f"Diluted shares outstanding:          {shares_outstanding:>10.6f}M")
    print(f"Value per share:                    ${value_per_share:>10.2f}")
    print(f"Share of value after 2030:           {share_of_value_after_2030:>10.2%}")


def main():
    is_data, bs_data, cfs_data, checks = run_proforma()
    print_statements(is_data, bs_data, cfs_data, checks)
    assert_balanced(checks)
    perform_valuation(cfs_data)


if __name__ == "__main__":
    main()
