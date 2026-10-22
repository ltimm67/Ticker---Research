"""Lab 15 — Portfolio Stability Decision app.

Run with: python -m streamlit run app.py
"""

from copy import deepcopy
from io import StringIO

import streamlit as st

import portfolio


STEP = 0.05


def result_for(sleeves, correlations, objective, eligible, reserve_minimum):
    """Use the optimizer in portfolio.py; this app does not duplicate portfolio math."""
    return portfolio.lowest_risk_mix(sleeves, correlations, objective, eligible, reserve_minimum, step=STEP)


def display_result(title, result):
    """Render a portfolio result or an honest infeasibility message."""
    st.subheader(title)
    if result is None:
        st.warning("No mix meets the objective and reserve rule at 5-point weight steps.")
        return
    st.write(" / ".join(f"{name}: {weight * 100:.0f}%" for name, weight in result["weights"].items()))
    first, second, third = st.columns(3)
    first.metric("Expected return", f"{result['return'] * 100:.2f}%")
    second.metric("Volatility", f"{result['volatility'] * 100:.2f}%")
    third.metric("Reserve-eligible", f"{result['reserve_weight'] * 100:.1f}%")


def largest_weight_change(loaded, edited):
    """Return the largest absolute allocation change in percentage points."""
    if loaded is None or edited is None:
        return None
    return max(abs(edited["weights"][name] - loaded["weights"][name]) * 100 for name in loaded["weights"])


def load_inputs(uploaded_file, last_36_months):
    """Return CSV estimates when uploaded, otherwise the Meridian training inputs."""
    if uploaded_file is None:
        return deepcopy(portfolio.SLEEVES), deepcopy(portfolio.CORRELATIONS), "Meridian training inputs"
    text = uploaded_file.getvalue().decode("utf-8-sig")
    sleeves, correlations = portfolio.estimate_from_csv(StringIO(text), last_36_months)
    label = "CSV estimates (last 36 months)" if last_36_months else "CSV estimates (all months)"
    return sleeves, correlations, label


def main():
    st.set_page_config(page_title="Portfolio Stability Decision", page_icon="📊")
    st.title("Portfolio Stability Decision")
    st.caption("Built with AI help, a learning demonstration, not investment advice.")

    with st.sidebar:
        st.header("Mandate and data")
        objective = st.number_input("Objective return (%)", value=6.5, step=0.1) / 100
        reserve_minimum = st.number_input("Minimum reserve-eligible weight (%)", value=3.0, step=0.5) / 100
        uploaded_file = st.file_uploader("Upload prices.csv", type="csv")
        last_36_months = st.toggle("Use only the last 36 monthly returns", value=False)

    try:
        edited_sleeves, edited_correlations, source_label = load_inputs(uploaded_file, last_36_months)
        loaded_sleeves, loaded_correlations, loaded_label = load_inputs(uploaded_file, False)
    except (UnicodeDecodeError, ValueError) as error:
        st.error(f"Could not use the CSV: {error}")
        return

    st.write(f"**Data:** {source_label}. Returns are historical estimates, not forecasts.")
    st.subheader("Expected-return estimates")
    columns = st.columns(len(edited_sleeves))
    for column, name in zip(columns, edited_sleeves):
        with column:
            edited_sleeves[name]["return"] = st.number_input(
                f"{name} return (%)", value=edited_sleeves[name]["return"] * 100,
                step=0.1, key=f"return_{name}"
            ) / 100

    st.subheader("Reserve-eligible assets")
    eligible = []
    check_columns = st.columns(len(edited_sleeves))
    for column, name in zip(check_columns, edited_sleeves):
        with column:
            default_reserve = name in portfolio.RESERVE_ELIGIBLE or name == "SGOV"
            if st.checkbox(name, value=default_reserve, key=f"eligible_{name}"):
                eligible.append(name)

    edited_result = result_for(edited_sleeves, edited_correlations, objective, eligible, reserve_minimum)
    # Keep the user-selected reserve designation fixed when comparing data windows.
    loaded_eligible = [name for name in eligible if name in loaded_sleeves]
    loaded_result = result_for(loaded_sleeves, loaded_correlations, objective, loaded_eligible, reserve_minimum)

    left, right = st.columns(2)
    with left:
        display_result("Current controls", edited_result)
    with right:
        display_result(f"As loaded: {loaded_label}", loaded_result)

    change = largest_weight_change(loaded_result, edited_result)
    if change is not None:
        st.success(f"Largest weight change from loaded inputs: {change:.0f} percentage points.")
    else:
        st.info("Largest weight change is unavailable because one result is infeasible.")
    st.caption("The search tries every long-only 5-point mix and selects the eligible mix with the lowest volatility.")


if __name__ == "__main__":
    main()
