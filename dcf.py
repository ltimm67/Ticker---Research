"""Five-year FCFF DCF training and valuation model.
Includes sensitivity grid and reverse DCF bisection search.
Amounts are USD millions except per-share value.
"""

import sys

# Editable inputs (Marriott International, Inc. - NASDAQ: MAR)
starting_fcff = 3111.0  # USD millions (2025 Form 10-K Cash Flow)
growth_rates = [0.06, 0.055, 0.05, 0.045, 0.04]  # Years 1-5 forecast
wacc = 0.089  # 8.90% sourced estimate
terminal_growth = 0.025  # 2.50% long-run economy rate
cash = 385.0  # USD millions (2025 Form 10-K Balance Sheet)
debt = 16211.0  # USD millions (2025 Form 10-K Balance Sheet)
diluted_shares = 273.6  # Millions of shares (2025 Form 10-K Diluted shares)

# Sensitivity grid inputs
wacc_list = [0.079, 0.089, 0.099]  # 7.9%, 8.9%, 9.9%
terminal_growth_list = [0.020, 0.025, 0.030]  # 2.0%, 2.5%, 3.0%

# Reverse DCF inputs
target_share_price = 335.50  # USD per share as of Sept 10, 2026
bisection_lower_bound = -0.10  # -10 percentage points
bisection_upper_bound = 0.35  # +35 percentage points (expanded beyond +25%)

# Support training mode verification via --training flag
if "--training" in sys.argv:
    starting_fcff = 100.0
    growth_rates = [0.08, 0.06, 0.05, 0.04, 0.03]
    wacc = 0.10
    terminal_growth = 0.03
    cash = 50.0
    debt = 300.0
    diluted_shares = 50.0
    wacc_list = [0.09, 0.10, 0.11]
    terminal_growth_list = [0.02, 0.03, 0.04]
    target_share_price = 30.00
    bisection_lower_bound = -0.05
    bisection_upper_bound = 0.10


def money(value: float) -> str:
    """Format a USD-million value to four decimal places."""
    return f"{value:,.4f}"


def calculate_dcf(
    fcff_start: float,
    g_rates: list[float],
    w: float,
    tg: float,
    c: float,
    d: float,
    shares: float,
    shift: float = 0.0,
) -> tuple[list[float], float, float, float, float, float, float, float]:
    """Calculate DCF outputs, returning (fcff_by_year, pv_explicit, tv_5, pv_tv, ev, eq, val_per_share, tv_share_of_ev)."""
    if tg >= w:
        raise ValueError("Terminal growth must be less than WACC.")

    fcff_by_year = []
    fcff = fcff_start
    for growth in g_rates:
        rate = growth + shift
        if rate <= -1.0:
            raise ValueError("Growth rate cannot be -100% or below.")
        fcff *= 1 + rate
        fcff_by_year.append(fcff)

    pv_explicit = sum(f / (1 + w) ** year for year, f in enumerate(fcff_by_year, start=1))
    tv_5 = fcff_by_year[-1] * (1 + tg) / (w - tg)
    pv_tv = tv_5 / (1 + w) ** 5
    ev = pv_explicit + pv_tv
    eq = ev + c - d
    val_per_share = eq / shares
    tv_share_of_ev = pv_tv / ev

    return fcff_by_year, pv_explicit, tv_5, pv_tv, ev, eq, val_per_share, tv_share_of_ev


def run_base_case() -> None:
    """Run and print the base 12 lines matching the known training answers."""
    if terminal_growth >= wacc:
        raise SystemExit("Model stopped: terminal growth must be less than WACC.")

    (
        fcff_by_year,
        present_value_explicit_fcff,
        terminal_value_year_5,
        present_value_terminal_value,
        enterprise_value,
        equity_value,
        value_per_diluted_share,
        terminal_value_share_of_enterprise_value,
    ) = calculate_dcf(starting_fcff, growth_rates, wacc, terminal_growth, cash, debt, diluted_shares)

    for year, fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year}: {money(fcff)}")
    print(f"Present value of the explicit FCFF: {money(present_value_explicit_fcff)}")
    print(f"Terminal value at Year 5: {money(terminal_value_year_5)}")
    print(f"Present value of the terminal value: {money(present_value_terminal_value)}")
    print(f"Enterprise value: {money(enterprise_value)}")
    print(f"Equity value: {money(equity_value)}")
    print(f"Value per diluted share: {money(value_per_diluted_share)}")
    print(
        "Present value of the terminal value as a share of enterprise value: "
        f"{terminal_value_share_of_enterprise_value:.4f} "
        f"({terminal_value_share_of_enterprise_value:.2%})"
    )


def run_sensitivity_grid() -> None:
    """Run and print the sensitivity grid of value per diluted share."""
    print("\nSensitivity Grid: Value per Diluted Share ($)")
    col_headers = [f"{tg:.1%}" for tg in terminal_growth_list]
    header_row = f"{'WACC \\ terminal growth':<24}" + "".join(f"{h:>10}" for h in col_headers)
    print(header_row)

    for w in wacc_list:
        row_str = f"{w:<24.1%}"
        for tg in terminal_growth_list:
            if tg >= w:
                row_str += f"{'Invalid':>10}"
            else:
                _, _, _, _, _, _, val, _ = calculate_dcf(
                    starting_fcff, growth_rates, w, tg, cash, debt, diluted_shares
                )
                row_str += f"{val:>10.2f}"
        print(row_str)


def run_reverse_dcf() -> None:
    """Run bisection to solve for uniform shift to growth rates matching target price."""
    print("\nReverse DCF (Expectations Investing)")
    print(f"Target share price: ${target_share_price:,.2f}")
    print("Inputs held fixed:")
    print(f"  Starting FCFF: {money(starting_fcff)}")
    print(f"  Base growth rates: {[f'{g:.2%}' for g in growth_rates]}")
    print(f"  WACC: {wacc:.2%}")
    print(f"  Terminal growth: {terminal_growth:.2%}")
    print(f"  Cash: {money(cash)}")
    print(f"  Debt: {money(debt)}")
    print(f"  Diluted shares: {diluted_shares:,.2f}")

    # Check validity of search bracket
    for g in growth_rates:
        if g + bisection_lower_bound <= -1.0:
            print("Error: Bisection lower bound pushes growth rate to -100% or below. Search refused.")
            return

    def price_for_shift(shift: float) -> float:
        _, _, _, _, _, _, val, _ = calculate_dcf(
            starting_fcff, growth_rates, wacc, terminal_growth, cash, debt, diluted_shares, shift=shift
        )
        return val

    low = bisection_lower_bound
    high = bisection_upper_bound
    val_low = price_for_shift(low)
    val_high = price_for_shift(high)

    if (val_low - target_share_price) * (val_high - target_share_price) > 0:
        print(
            f"No solution in bracket [{low:+.2%}, {high:+.2%}]. "
            f"Value range at bounds is ${val_low:.2f} to ${val_high:.2f}."
        )
        return

    # Bisection search
    for _ in range(100):
        mid = (low + high) / 2.0
        val_mid = price_for_shift(mid)
        if abs(val_mid - target_share_price) < 1e-7:
            break
        if (val_low - target_share_price) * (val_mid - target_share_price) <= 0:
            high = mid
            val_high = val_mid
        else:
            low = mid
            val_low = val_mid

    solved_shift = mid
    shift_points = solved_shift * 100.0
    print(f"Solved uniform growth rate shift: {shift_points:+.2f} percentage points ({solved_shift:+.4f})")
    adjusted_rates = [g + solved_shift for g in growth_rates]
    print(f"Implied explicit growth rates: {[f'{r:.2%}' for r in adjusted_rates]}")


def main() -> None:
    run_base_case()
    run_sensitivity_grid()
    run_reverse_dcf()


if __name__ == "__main__":
    main()
