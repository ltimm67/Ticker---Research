"""Lab 14 — Portfolio Baselines.

Run with: python portfolio.py
All returns, volatilities, and weights below are decimal values (0.035 = 3.5%).
"""

import math


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
