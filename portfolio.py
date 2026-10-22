"""Lab 14 — Portfolio Baselines.

Run with: python portfolio.py
All returns, volatilities, and weights below are decimal values (0.035 = 3.5%).
"""

import csv
import math
import statistics


# EDITABLE INPUTS
SLEEVES = {
    "Bills": {"return": 0.035, "volatility": 0.005},
    "10-year": {"return": 0.043, "volatility": 0.070},
    "IG bonds": {"return": 0.050, "volatility": 0.060},
    "Equity": {"return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Bills": {"Bills": 1.00, "10-year": 0.10, "IG bonds": 0.05, "Equity": 0.00},
    "10-year": {"Bills": 0.10, "10-year": 1.00, "IG bonds": 0.80, "Equity": -0.10},
    "IG bonds": {"Bills": 0.05, "10-year": 0.80, "IG bonds": 1.00, "Equity": 0.25},
    "Equity": {"Bills": 0.00, "10-year": -0.10, "IG bonds": 0.25, "Equity": 1.00},
}

OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = ("Bills", "10-year")


def validate_correlations(correlations, sleeves):
    """Raise ValueError when a correlation table is incomplete, invalid, or asymmetric."""
    names = tuple(sleeves)
    for left in names:
        if left not in correlations:
            raise ValueError(f"Correlation table is missing row: {left}")
        for right in names:
            if right not in correlations[left]:
                raise ValueError(f"Correlation table is missing {left}/{right}.")
            value = correlations[left][right]
            if not -1.0 <= value <= 1.0:
                raise ValueError(f"Correlation for {left}/{right} must be between -1 and 1.")
            if abs(value - correlations.get(right, {}).get(left, float("inf"))) > 1e-12:
                raise ValueError(f"Correlation table is not symmetric at {left}/{right}.")


def covariance_matrix(sleeves, correlations):
    """Return covariance[i][j] = correlation[i][j] × volatility[i] × volatility[j]."""
    return {
        left: {
            right: correlations[left][right] * sleeves[left]["volatility"] * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def expected_return(weights, sleeves):
    """Calculate the weighted expected return."""
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_volatility(weights, covariance):
    """Calculate sqrt(sum of w_i × covariance_i,j × w_j for every pair of sleeves)."""
    variance = sum(
        weights[left] * covariance[left][right] * weights[right]
        for left in weights
        for right in weights
    )
    return math.sqrt(variance)


def reserve_weight(weights, eligible):
    """Return the combined weight of reserve-eligible sleeves."""
    return sum(weights[name] for name in eligible)


def equal_weight_portfolio(sleeves):
    """Give every sleeve the same weight."""
    return {name: 1.0 / len(sleeves) for name in sleeves}


def inverse_volatility_portfolio(sleeves):
    """Set each weight proportional to one divided by its volatility."""
    inverse_volatilities = {name: 1.0 / data["volatility"] for name, data in sleeves.items()}
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def generate_long_only_mixes(asset_names, step=0.05):
    """Yield every long-only weight mix that sums to 100%, in fixed increments."""
    if step <= 0 or abs(round(1 / step) * step - 1) > 1e-9:
        raise ValueError("Step must divide 100% exactly.")
    units = round(1 / step)

    def build(index, remaining, values):
        if index == len(asset_names) - 1:
            yield dict(zip(asset_names, values + [remaining * step]))
            return
        for amount in range(remaining + 1):
            yield from build(index + 1, remaining - amount, values + [amount * step])

    yield from build(0, units, [])


def lowest_risk_mix(sleeves, correlations, objective, reserve_eligible, reserve_minimum, step=0.05):
    """Find the lowest-volatility long-only mix meeting return and reserve rules."""
    validate_correlations(correlations, sleeves)
    covariance = covariance_matrix(sleeves, correlations)
    best = None
    for weights in generate_long_only_mixes(list(sleeves), step):
        result_return = expected_return(weights, sleeves)
        reserves = reserve_weight(weights, reserve_eligible)
        if result_return < objective or reserves < reserve_minimum:
            continue
        result = {
            "weights": weights,
            "return": result_return,
            "volatility": portfolio_volatility(weights, covariance),
            "reserve_weight": reserves,
        }
        if best is None or result["volatility"] < best["volatility"]:
            best = result
    return best


def estimate_from_csv(csv_source, last_36_months=False):
    """Estimate annualized return, volatility, and correlation from monthly price CSV data."""
    if hasattr(csv_source, "read"):
        rows = list(csv.reader(csv_source))
    else:
        with open(csv_source, newline="", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))
    if len(rows) < 3 or len(rows[0]) < 2:
        raise ValueError("CSV needs a date, at least one asset, and two price rows.")

    names = [name.strip() for name in rows[0][1:]]
    if not all(names) or len(set(names)) != len(names):
        raise ValueError("Each asset column needs a unique ticker or name.")
    prices = {name: [] for name in names}
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(names) + 1:
            raise ValueError(f"Row {row_number} does not match the header columns.")
        for name, text in zip(names, row[1:]):
            try:
                price = float(text)
            except ValueError as error:
                raise ValueError(f"Row {row_number} has a non-numeric price for {name}.") from error
            if price <= 0:
                raise ValueError(f"Row {row_number} has a non-positive price for {name}.")
            prices[name].append(price)

    monthly_returns = {
        name: [later / earlier - 1.0 for earlier, later in zip(values, values[1:])]
        for name, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {name: values[-36:] for name, values in monthly_returns.items()}
    if len(next(iter(monthly_returns.values()))) < 2:
        raise ValueError("Need at least three price rows for volatility and correlation.")

    sleeves = {
        name: {"return": statistics.mean(values) * 12, "volatility": statistics.stdev(values) * math.sqrt(12)}
        for name, values in monthly_returns.items()
    }
    correlations = {name: {} for name in names}
    for left in names:
        for right in names:
            if left == right:
                correlations[left][right] = 1.0
                continue
            left_values, right_values = monthly_returns[left], monthly_returns[right]
            left_stdev, right_stdev = statistics.stdev(left_values), statistics.stdev(right_values)
            if left_stdev == 0 or right_stdev == 0:
                raise ValueError(f"Cannot calculate correlation: {left} or {right} has zero variation.")
            covariance = sum(
                (a - statistics.mean(left_values)) * (b - statistics.mean(right_values))
                for a, b in zip(left_values, right_values)
            ) / (len(left_values) - 1)
            correlations[left][right] = covariance / (left_stdev * right_stdev)
    return sleeves, correlations


def print_portfolio(name, weights, sleeves, covariance, objective, eligible):
    """Print one portfolio's calculated results."""
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariance)
    reserves = reserve_weight(weights, eligible)
    ordered_weights = " / ".join(f"{weights[sleeve] * 100:.1f}" for sleeve in sleeves)
    print(name)
    print(f"  Weights (Bills / 10-year / IG / Equity): {ordered_weights}")
    print(f"  Expected return: {result_return * 100:.2f}%")
    print(f"  Volatility:      {result_volatility * 100:.2f}%")
    print(f"  Reserve-eligible: {reserves * 100:.1f}%")
    print(f"  Meets {objective * 100:.1f}% objective: {'yes' if result_return >= objective else 'no'}\n")


def main():
    validate_correlations(CORRELATIONS, SLEEVES)
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": {"Bills": 0.0, "10-year": 0.0, "IG bonds": 0.40, "Equity": 0.60},
        "Equal weight": equal_weight_portfolio(SLEEVES),
        "Inverse volatility": inverse_volatility_portfolio(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN, RESERVE_ELIGIBLE)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Input error: {error}")
