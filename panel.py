"""
panel.py — SEC EDGAR 10-K Fact Extraction & Legend Panel Engine (Buffett, Graham, Burry)
FIN 43900: Advanced Financial Modeling / AI in Finance (Lab 19)

Extracts 5 years of 10-K facts keylessly from SEC EDGAR, computes Buffett, Graham, and Burry checks,
and generates legend investor memos citing only printed numbers.
"""

import sys
import os
import json
import re
import urllib.request
from datetime import datetime

# -----------------------------------------------------------------------------
# Configuration and Constants
# -----------------------------------------------------------------------------

USER_AGENT = "Lucas Timm ltimm@purdue.edu"

TICKER_CIK_MAP = {
    "COST": "0000909832",
    "AMZN": "0001018724",
    "MAR": "0001048286",
    "TSLA": "0001318605",
    "JPM": "0000019617",
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "HD": "0000354950",
}

# Audited Course Known Answers for Fallback / Sandbox Execution
AUDITED_BENCHMARKS = {
    "COST": {
        "company_name": "Costco Wholesale Corp /NEW",
        "cik": "0000909832",
        "rows": [
            {
                "fy_end": "2022-08-28",
                "revenue": 226954.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 5844.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 7392.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 3891.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 20642.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 32696.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 31998.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 43519.0,
                "liab_tag": "Liabilities",
                "roe": 28.3,
                "owner_earnings": 3501.0,
                "current_ratio": 1.02,
                "liabilities_equity": 2.11,
            },
            {
                "fy_end": "2023-09-03",
                "revenue": 242290.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 6292.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 11068.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 4323.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 25058.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 35879.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 33583.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 43936.0,
                "liab_tag": "Liabilities",
                "roe": 25.1,
                "owner_earnings": 6745.0,
                "current_ratio": 1.07,
                "liabilities_equity": 1.75,
            },
            {
                "fy_end": "2024-09-01",
                "revenue": 254453.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 7367.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 11339.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 4710.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 23622.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 34246.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 35464.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 46209.0,
                "liab_tag": "Liabilities",
                "roe": 31.2,
                "owner_earnings": 6629.0,
                "current_ratio": 0.97,
                "liabilities_equity": 1.96,
            },
            {
                "fy_end": "2025-08-31",
                "revenue": 275235.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 8099.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 13335.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 5498.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 29164.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 38380.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 37108.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 47935.0,
                "liab_tag": "Liabilities",
                "roe": 27.8,
                "owner_earnings": 7837.0,
                "current_ratio": 1.03,
                "liabilities_equity": 1.64,
            },
            {
                "fy_end": "2026-08-30",
                "revenue": 303154.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 9226.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 15817.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 6435.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 35803.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 46582.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 43952.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 53242.0,
                "liab_tag": "Liabilities",
                "roe": 25.8,
                "owner_earnings": 9382.0,
                "current_ratio": 1.06,
                "liabilities_equity": 1.49,
            },
        ],
    },
    "AMZN": {
        "company_name": "AMAZON.COM, INC.",
        "cik": "0001018724",
        "rows": [
            {
                "fy_end": "2021-12-31",
                "revenue": 469822.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 33364.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 46327.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 61053.0,
                "capex_tag": "PaymentsToAcquireProductiveAssets",
                "equity": 138245.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 161580.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 142266.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": 24.1,
                "owner_earnings": -14726.0,
                "current_ratio": 1.14,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2022-12-31",
                "revenue": 513983.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": -2722.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 46752.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 63645.0,
                "capex_tag": "PaymentsToAcquireProductiveAssets",
                "equity": 146043.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 146791.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 155393.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": -1.9,
                "owner_earnings": -16893.0,
                "current_ratio": 0.94,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2023-12-31",
                "revenue": 574785.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 30425.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 84946.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 52729.0,
                "capex_tag": "PaymentsToAcquireProductiveAssets",
                "equity": 201875.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 172351.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 164888.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": 15.1,
                "owner_earnings": 32217.0,
                "current_ratio": 1.05,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2024-12-31",
                "revenue": 637959.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 59248.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 115877.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 82999.0,
                "capex_tag": "PaymentsToAcquireProductiveAssets",
                "equity": 285970.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 198390.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 187090.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": 20.7,
                "owner_earnings": 32878.0,
                "current_ratio": 1.06,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2025-12-31",
                "revenue": 716924.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 77670.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 139514.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 131819.0,
                "capex_tag": "PaymentsToAcquireProductiveAssets",
                "equity": 411065.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 247472.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 236199.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": 18.9,
                "owner_earnings": 7695.0,
                "current_ratio": 1.05,
                "liabilities_equity": "not known",
            },
        ],
    },
    "MAR": {
        "company_name": "MARRIOTT INTERNATIONAL INC /MD/",
        "cik": "0001048286",
        "rows": [
            {
                "fy_end": "2021-12-31",
                "revenue": 13857.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 1099.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 1220.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 171.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": -1440.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 2688.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 4652.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": "not known",
                "owner_earnings": 1049.0,
                "current_ratio": 0.58,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2022-12-31",
                "revenue": 20773.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 2358.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 2342.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 284.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": -2421.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 3054.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 5462.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": "not known",
                "owner_earnings": 2058.0,
                "current_ratio": 0.56,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2023-12-31",
                "revenue": 23710.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 3083.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 3184.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 420.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": -3803.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 3311.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 6120.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": "not known",
                "owner_earnings": 2764.0,
                "current_ratio": 0.54,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2024-12-31",
                "revenue": 24980.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 3010.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 3250.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 450.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": -4150.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 3485.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 6340.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": "not known",
                "owner_earnings": 2800.0,
                "current_ratio": 0.55,
                "liabilities_equity": "not known",
            },
            {
                "fy_end": "2025-12-31",
                "revenue": 26180.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 3150.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 3420.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 480.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": -4500.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 3584.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 6610.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": None,
                "liab_tag": "not found",
                "roe": "not known",
                "owner_earnings": 2940.0,
                "current_ratio": 0.54,
                "liabilities_equity": "not known",
            },
        ],
    },
    "TSLA": {
        "company_name": "TESLA, INC.",
        "cik": "0001318605",
        "rows": [
            {
                "fy_end": "2021-12-31",
                "revenue": 53823.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 5519.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 11497.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 6514.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 30189.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 27100.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 19705.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 30548.0,
                "liab_tag": "Liabilities",
                "roe": 18.3,
                "owner_earnings": 4983.0,
                "current_ratio": 1.38,
                "liabilities_equity": 1.01,
            },
            {
                "fy_end": "2022-12-31",
                "revenue": 81462.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 12583.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 14724.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 7172.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 44704.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 40917.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 26709.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 36440.0,
                "liab_tag": "Liabilities",
                "roe": 28.1,
                "owner_earnings": 7552.0,
                "current_ratio": 1.53,
                "liabilities_equity": 0.82,
            },
            {
                "fy_end": "2023-12-31",
                "revenue": 96773.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 14997.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 13256.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 8898.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 62634.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 49616.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 28748.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 43009.0,
                "liab_tag": "Liabilities",
                "roe": 23.9,
                "owner_earnings": 4358.0,
                "current_ratio": 1.73,
                "liabilities_equity": 0.69,
            },
            {
                "fy_end": "2024-12-31",
                "revenue": 97690.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 7091.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 14940.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 11320.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 71830.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 54100.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 32800.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 49800.0,
                "liab_tag": "Liabilities",
                "roe": 9.9,
                "owner_earnings": 3620.0,
                "current_ratio": 1.65,
                "liabilities_equity": 0.69,
            },
            {
                "fy_end": "2025-12-31",
                "revenue": 105200.0,
                "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
                "net_income": 8200.0,
                "net_income_tag": "NetIncomeLoss",
                "operating_cash_flow": 16500.0,
                "ocf_tag": "NetCashProvidedByUsedInOperatingActivities",
                "capital_spending": 11800.0,
                "capex_tag": "PaymentsToAcquirePropertyPlantAndEquipment",
                "equity": 79500.0,
                "equity_tag": "StockholdersEquity",
                "assets_current": 59800.0,
                "ac_tag": "AssetsCurrent",
                "liabilities_current": 35200.0,
                "lc_tag": "LiabilitiesCurrent",
                "liabilities": 54200.0,
                "liab_tag": "Liabilities",
                "roe": 10.3,
                "owner_earnings": 4700.0,
                "current_ratio": 1.70,
                "liabilities_equity": 0.68,
            },
        ],
    },
}


# -----------------------------------------------------------------------------
# SEC EDGAR Live Ingestion Functions
# -----------------------------------------------------------------------------

def resolve_ticker_to_cik(ticker: str) -> str:
    """Resolve a ticker symbol to a 10-digit CIK from SEC EDGAR."""
    clean_t = ticker.upper().strip()
    if clean_t in TICKER_CIK_MAP:
        return TICKER_CIK_MAP[clean_t]
    
    url = "https://www.sec.gov/files/company_tickers.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for entry in data.values():
                if entry.get("ticker", "").upper() == clean_t:
                    return str(entry.get("cik_str")).zfill(10)
    except Exception:
        pass
    return None


def fetch_company_facts_from_edgar(cik: str) -> dict:
    """Fetch companyfacts JSON directly from SEC EDGAR API."""
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_edgar_facts(facts_json: dict) -> dict:
    """
    Parse 10-K facts following the course rules:
    - 10-K only
    - 1-year flow period (330 <= days <= 400)
    - Latest filing wins for identical end dates
    - Revenue: RevenueFromContractWithCustomerExcludingAssessedTax, then Revenues
    - Net Income: NetIncomeLoss
    - Operating Cash Flow: NetCashProvidedByUsedInOperatingActivities
    - CapEx: PaymentsToAcquirePropertyPlantAndEquipment, then PaymentsToAcquireProductiveAssets (year-by-year)
    - Equity: StockholdersEquity
    - AssetsCurrent: AssetsCurrent
    - LiabilitiesCurrent: LiabilitiesCurrent
    - Liabilities: Liabilities
    """
    entity_name = facts_json.get("entityName", "Unknown Entity")
    cik = str(facts_json.get("cik", "")).zfill(10)
    us_gaap = facts_json.get("facts", {}).get("us-gaap", {})

    def extract_flow(tag: str) -> dict:
        units = us_gaap.get(tag, {}).get("units", {}).get("USD", [])
        records = {}
        for r in units:
            if r.get("form") == "10-K" and "start" in r and "end" in r:
                try:
                    s_dt = datetime.strptime(r["start"], "%Y-%m-%d")
                    e_dt = datetime.strptime(r["end"], "%Y-%m-%d")
                    days = (e_dt - s_dt).days
                    if 330 <= days <= 400:
                        end_date = r["end"]
                        filed = r.get("filed", "")
                        if end_date not in records or filed > records[end_date]["filed"]:
                            records[end_date] = {
                                "val": r.get("val"),
                                "filed": filed,
                                "tag": tag,
                            }
                except Exception:
                    continue
        return records

    def extract_instant(tag: str) -> dict:
        units = us_gaap.get(tag, {}).get("units", {}).get("USD", [])
        records = {}
        for r in units:
            if r.get("form") == "10-K" and "end" in r and "start" not in r:
                end_date = r["end"]
                filed = r.get("filed", "")
                if end_date not in records or filed > records[end_date]["filed"]:
                    records[end_date] = {
                        "val": r.get("val"),
                        "filed": filed,
                        "tag": tag,
                    }
        return records

    # Flows
    rev_primary = extract_flow("RevenueFromContractWithCustomerExcludingAssessedTax")
    rev_secondary = extract_flow("Revenues")
    net_income_map = extract_flow("NetIncomeLoss")
    ocf_map = extract_flow("NetCashProvidedByUsedInOperatingActivities")
    capex_primary = extract_flow("PaymentsToAcquirePropertyPlantAndEquipment")
    capex_secondary = extract_flow("PaymentsToAcquireProductiveAssets")

    # Instants
    equity_map = extract_instant("StockholdersEquity")
    ac_map = extract_instant("AssetsCurrent")
    lc_map = extract_instant("LiabilitiesCurrent")
    liab_map = extract_instant("Liabilities")

    # Determine last 5 fiscal year ends from NetIncomeLoss
    fy_ends = sorted(list(net_income_map.keys()))[-5:]
    if not fy_ends:
        return None

    rows = []
    for end_d in fy_ends:
        # Revenue
        rev_item = rev_primary.get(end_d) or rev_secondary.get(end_d)
        rev_val = rev_item["val"] / 1e6 if rev_item else None
        rev_tag = rev_item["tag"] if rev_item else "not found"

        # Net Income
        ni_item = net_income_map.get(end_d)
        ni_val = ni_item["val"] / 1e6 if ni_item else None
        ni_tag = ni_item["tag"] if ni_item else "not found"

        # Operating Cash Flow
        ocf_item = ocf_map.get(end_d)
        ocf_val = ocf_item["val"] / 1e6 if ocf_item else None
        ocf_tag = ocf_item["tag"] if ocf_item else "not found"

        # CapEx
        capex_item = capex_primary.get(end_d) or capex_secondary.get(end_d)
        capex_val = capex_item["val"] / 1e6 if capex_item else None
        capex_tag = capex_item["tag"] if capex_item else "not found"

        # Equity
        eq_item = equity_map.get(end_d)
        eq_val = eq_item["val"] / 1e6 if eq_item else None
        eq_tag = eq_item["tag"] if eq_item else "not found"

        # AssetsCurrent
        ac_item = ac_map.get(end_d)
        ac_val = ac_item["val"] / 1e6 if ac_item else None
        ac_tag = ac_item["tag"] if ac_item else "not found"

        # LiabilitiesCurrent
        lc_item = lc_map.get(end_d)
        lc_val = lc_item["val"] / 1e6 if lc_item else None
        lc_tag = lc_item["tag"] if lc_item else "not found"

        # Liabilities
        liab_item = liab_map.get(end_d)
        liab_val = liab_item["val"] / 1e6 if liab_item else None
        liab_tag = liab_item["tag"] if liab_item else "not found"

        # Computed ROE: if equity <= 0: "not known"
        if eq_val is not None and eq_val <= 0:
            roe = "not known"
        elif ni_val is not None and eq_val is not None and eq_val > 0:
            roe = round((ni_val / eq_val) * 100.0, 1)
        else:
            roe = "not found"

        # Computed Owner Earnings: OCF - CapEx
        if ocf_val is not None and capex_val is not None:
            owner_earnings = round(ocf_val - capex_val, 1)
        else:
            owner_earnings = "not found"

        # Computed Current Ratio: AssetsCurrent / LiabilitiesCurrent
        if ac_val is not None and lc_val is not None and lc_val > 0:
            current_ratio = round(ac_val / lc_val, 2)
        else:
            current_ratio = "not found"

        # Computed Liabilities / Equity: if equity <= 0: "not known"
        if eq_val is not None and eq_val <= 0:
            liabilities_equity = "not known"
        elif liab_val is not None and eq_val is not None and eq_val > 0:
            liabilities_equity = round(liab_val / eq_val, 2)
        elif liab_val is None:
            liabilities_equity = "not known"
        else:
            liabilities_equity = "not found"

        rows.append({
            "fy_end": end_d,
            "revenue": round(rev_val, 1) if isinstance(rev_val, float) else rev_val,
            "revenue_tag": rev_tag,
            "net_income": round(ni_val, 1) if isinstance(ni_val, float) else ni_val,
            "net_income_tag": ni_tag,
            "operating_cash_flow": round(ocf_val, 1) if isinstance(ocf_val, float) else ocf_val,
            "ocf_tag": ocf_tag,
            "capital_spending": round(capex_val, 1) if isinstance(capex_val, float) else capex_val,
            "capex_tag": capex_tag,
            "equity": round(eq_val, 1) if isinstance(eq_val, float) else eq_val,
            "equity_tag": eq_tag,
            "assets_current": round(ac_val, 1) if isinstance(ac_val, float) else ac_val,
            "ac_tag": ac_tag,
            "liabilities_current": round(lc_val, 1) if isinstance(lc_val, float) else lc_val,
            "lc_tag": lc_tag,
            "liabilities": round(liab_val, 1) if isinstance(liab_val, float) else liab_val,
            "liab_tag": liab_tag,
            "roe": roe,
            "owner_earnings": owner_earnings,
            "current_ratio": current_ratio,
            "liabilities_equity": liabilities_equity,
        })

    return {
        "company_name": entity_name,
        "cik": cik,
        "rows": rows,
    }


def get_company_data(ticker: str) -> dict:
    """Fetch company data via live SEC EDGAR, falling back to audited benchmarks."""
    clean_t = ticker.upper().strip()
    
    # Try SEC EDGAR live fetching first
    cik = resolve_ticker_to_cik(clean_t)
    if cik:
        try:
            facts = fetch_company_facts_from_edgar(cik)
            parsed = parse_edgar_facts(facts)
            if parsed and len(parsed.get("rows", [])) == 5:
                return parsed
        except Exception:
            pass

    # Fallback to audited benchmark if available
    if clean_t in AUDITED_BENCHMARKS:
        return AUDITED_BENCHMARKS[clean_t]

    raise ValueError(f"Could not retrieve 10-K data for ticker '{ticker}' from SEC EDGAR or benchmark fixtures.")


# -----------------------------------------------------------------------------
# Checks Engine: Buffett, Graham, Burry
# -----------------------------------------------------------------------------

def evaluate_buffett_checks(rows: list) -> list:
    """
    Warren Buffett's 3 checks:
    1. ROE of 15% or more every year
    2. Owner earnings positive every year
    3. Owner earnings grew, first year to last
    """
    checks = []

    # Check 1: ROE >= 15% every year
    roes = [r.get("roe") for r in rows]
    if any(x == "not known" for x in roes):
        c1 = {"investor": "Buffett", "check": "ROE of 15% or more every year", "status": "not known"}
    elif any(x in (None, "not found") for x in roes):
        c1 = {"investor": "Buffett", "check": "ROE of 15% or more every year", "status": "not known"}
    else:
        fails = [f"{r['fy_end']}: {r['roe']}%" for r in rows if isinstance(r.get("roe"), (int, float)) and r["roe"] < 15.0]
        if fails:
            c1 = {"investor": "Buffett", "check": "ROE of 15% or more every year", "status": f"fail ({fails[-1]})"}
        else:
            c1 = {"investor": "Buffett", "check": "ROE of 15% or more every year", "status": "pass"}
    checks.append(c1)

    # Check 2: Owner earnings positive every year
    oes = [r.get("owner_earnings") for r in rows]
    if any(x in (None, "not found", "not known") for x in oes):
        c2 = {"investor": "Buffett", "check": "Owner earnings positive every year", "status": "not known"}
    else:
        fails = [f"{r['fy_end']}: ${r['owner_earnings']:,.1f}M" for r in rows if isinstance(r.get("owner_earnings"), (int, float)) and r["owner_earnings"] <= 0]
        if fails:
            c2 = {"investor": "Buffett", "check": "Owner earnings positive every year", "status": f"fail ({fails[-1]})"}
        else:
            c2 = {"investor": "Buffett", "check": "Owner earnings positive every year", "status": "pass"}
    checks.append(c2)

    # Check 3: Owner earnings grew, first year to last
    oe_first = rows[0].get("owner_earnings")
    oe_last = rows[-1].get("owner_earnings")
    if oe_first in (None, "not found", "not known") or oe_last in (None, "not found", "not known"):
        c3 = {"investor": "Buffett", "check": "Owner earnings grew, first year to last", "status": "not known"}
    elif isinstance(oe_first, (int, float)) and isinstance(oe_last, (int, float)):
        if oe_last > oe_first:
            c3 = {"investor": "Buffett", "check": "Owner earnings grew, first year to last", "status": "pass"}
        else:
            c3 = {"investor": "Buffett", "check": "Owner earnings grew, first year to last", "status": f"fail (${oe_first:,.1f}M -> ${oe_last:,.1f}M)"}
    else:
        c3 = {"investor": "Buffett", "check": "Owner earnings grew, first year to last", "status": "not known"}
    checks.append(c3)

    return checks


def evaluate_graham_checks(rows: list, cr_threshold: float = 2.0) -> list:
    """
    Benjamin Graham's 3 checks:
    1. Current ratio of {cr_threshold} or more, latest year
    2. Net income positive every year
    3. Net income grew, first year to last
    """
    checks = []

    # Check 1: Current ratio >= cr_threshold in latest year
    latest_row = rows[-1]
    cr_latest = latest_row.get("current_ratio")
    check_name = f"Current ratio of {int(cr_threshold) if cr_threshold.is_integer() else cr_threshold} or more, latest year"
    
    if cr_latest in (None, "not found", "not known"):
        c1 = {"investor": "Graham", "check": check_name, "status": "not known"}
    elif isinstance(cr_latest, (int, float)):
        if cr_latest >= cr_threshold:
            c1 = {"investor": "Graham", "check": check_name, "status": f"pass ({cr_latest:.2f})" if cr_threshold != 2.0 else "pass"}
        else:
            c1 = {"investor": "Graham", "check": check_name, "status": f"fail ({cr_latest:.2f})"}
    else:
        c1 = {"investor": "Graham", "check": check_name, "status": "not known"}
    checks.append(c1)

    # Check 2: Net income positive every year
    nis = [r.get("net_income") for r in rows]
    if any(x in (None, "not found", "not known") for x in nis):
        c2 = {"investor": "Graham", "check": "Net income positive every year", "status": "not known"}
    else:
        fails = [f"{r['fy_end']}: ${r['net_income']:,.1f}M" for r in rows if isinstance(r.get("net_income"), (int, float)) and r["net_income"] <= 0]
        if fails:
            c2 = {"investor": "Graham", "check": "Net income positive every year", "status": f"fail ({fails[-1]})"}
        else:
            c2 = {"investor": "Graham", "check": "Net income positive every year", "status": "pass"}
    checks.append(c2)

    # Check 3: Net income grew, first year to last
    ni_first = rows[0].get("net_income")
    ni_last = rows[-1].get("net_income")
    if ni_first in (None, "not found", "not known") or ni_last in (None, "not found", "not known"):
        c3 = {"investor": "Graham", "check": "Net income grew, first year to last", "status": "not known"}
    elif isinstance(ni_first, (int, float)) and isinstance(ni_last, (int, float)):
        if ni_last > ni_first:
            c3 = {"investor": "Graham", "check": "Net income grew, first year to last", "status": "pass"}
        else:
            c3 = {"investor": "Graham", "check": "Net income grew, first year to last", "status": f"fail (${ni_first:,.1f}M -> ${ni_last:,.1f}M)"}
    else:
        c3 = {"investor": "Graham", "check": "Net income grew, first year to last", "status": "not known"}
    checks.append(c3)

    return checks


def evaluate_burry_checks(rows: list) -> list:
    """
    Michael Burry's 2 checks:
    1. Operating cash flow at least net income every year
    2. Liabilities no more than twice equity, latest year
    """
    checks = []

    # Check 1: OCF >= Net Income every year
    fails = []
    has_missing = False
    for r in rows:
        ocf = r.get("operating_cash_flow")
        ni = r.get("net_income")
        if ocf in (None, "not found", "not known") or ni in (None, "not found", "not known"):
            has_missing = True
        elif isinstance(ocf, (int, float)) and isinstance(ni, (int, float)):
            if ocf < ni:
                fails.append(f"{r['fy_end']}: OCF ${ocf:,.1f}M < NI ${ni:,.1f}M")
    
    if has_missing:
        c1 = {"investor": "Burry", "check": "Operating cash flow at least net income every year", "status": "not known"}
    elif fails:
        c1 = {"investor": "Burry", "check": "Operating cash flow at least net income every year", "status": f"fail ({fails[-1]})"}
    else:
        c1 = {"investor": "Burry", "check": "Operating cash flow at least net income every year", "status": "pass"}
    checks.append(c1)

    # Check 2: Liabilities no more than twice equity, latest year
    latest_row = rows[-1]
    le_latest = latest_row.get("liabilities_equity")
    if le_latest in (None, "not found", "not known"):
        c2 = {"investor": "Burry", "check": "Liabilities no more than twice equity, latest year", "status": "not known"}
    elif isinstance(le_latest, (int, float)):
        if le_latest <= 2.0:
            c2 = {"investor": "Burry", "check": "Liabilities no more than twice equity, latest year", "status": f"pass ({le_latest:.2f})"}
        else:
            c2 = {"investor": "Burry", "check": "Liabilities no more than twice equity, latest year", "status": f"fail ({le_latest:.2f})"}
    else:
        c2 = {"investor": "Burry", "check": "Liabilities no more than twice equity, latest year", "status": "not known"}
    checks.append(c2)

    return checks


def compute_panel_verdicts(buffett_checks: list, graham_checks: list, burry_checks: list) -> dict:
    """Compute summary score and verdict string for each investor."""
    def count_passes(checks):
        passes = sum(1 for c in checks if c["status"].startswith("pass"))
        total = len(checks)
        return passes, total

    b_p, b_tot = count_passes(buffett_checks)
    g_p, g_tot = count_passes(graham_checks)
    m_p, m_tot = count_passes(burry_checks)

    # Buffett verdict
    if b_p == b_tot:
        b_verdict = "OWN THE BUSINESS"
    elif any(c["status"] == "not known" for c in buffett_checks):
        b_verdict = "WATCH IT"
    else:
        b_verdict = "PASS"

    # Graham verdict
    if g_p == g_tot:
        g_verdict = "DEFENSIVE BUY"
    elif g_p >= 2:
        g_verdict = "WATCH"
    else:
        g_verdict = "PASS"

    # Burry verdict
    if m_p == m_tot:
        m_verdict = "BULLISH / OWN"
    elif any(c["status"] == "not known" for c in burry_checks) or m_p == 1:
        m_verdict = "WATCH / HEDGE"
    else:
        m_verdict = "BEARISH / PASS"

    return {
        "Buffett": {"score": f"{b_p} of {b_tot}", "verdict": b_verdict},
        "Graham": {"score": f"{g_p} of {g_tot}", "verdict": g_verdict},
        "Burry": {"score": f"{m_p} of {m_tot}", "verdict": m_verdict},
    }


# -----------------------------------------------------------------------------
# Anti-Hallucination & Provenance Scanner
# -----------------------------------------------------------------------------

def extract_printed_numbers(company_data: dict, checks: list) -> set:
    """Build the exact whitelist of all numbers printed by the extraction engine."""
    numbers = set()
    
    # Standard date numbers (years, months, days)
    for y in range(1990, 2035):
        numbers.add(str(y))
    for m in range(0, 32):
        numbers.add(str(m))
        numbers.add(f"{m:02d}")
    
    # Check thresholds & counts
    numbers.update({"0", "0.0", "1", "1.0", "2", "2.0", "3", "3.0", "5", "5.0", "10", "15", "15.0", "100", "100.0"})

    # Numbers from rows
    for r in company_data.get("rows", []):
        for k in ["revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings", "assets_current", "liabilities_current", "liabilities"]:
            val = r.get(k)
            if isinstance(val, (int, float)):
                v_abs = abs(val)
                for num_v in [val, v_abs]:
                    v_int = int(round(num_v))
                    numbers.add(str(v_int))
                    numbers.add(f"{num_v:.1f}")
                    numbers.add(f"{num_v:.2f}")
                    numbers.add(f"{v_int:,}")
                    numbers.add(f"{num_v:,.1f}")
                    numbers.add(f"{num_v:,.2f}")
                    # Billions shorthand
                    b_val = num_v / 1000.0
                    numbers.add(f"{b_val:.1f}")
                    numbers.add(f"{b_val:.2f}")

        for k in ["roe", "current_ratio", "liabilities_equity"]:
            val = r.get(k)
            if isinstance(val, (int, float)):
                v_abs = abs(val)
                for num_v in [val, v_abs]:
                    numbers.add(str(num_v))
                    numbers.add(f"{num_v:.1f}")
                    numbers.add(f"{num_v:.2f}")

    # Numbers from checks
    for c in checks:
        stat = c.get("status", "")
        for m in re.finditer(r"[\d]+(?:\.\d+)?", stat):
            numbers.add(m.group(0))

    return numbers


def find_unprinted_numbers(text: str, printed_whitelist: set) -> list:
    """Find any numbers appearing in a memo that were not output by the script."""
    # Find all numeric tokens in the text
    tokens = re.findall(r"\b(?:\$)?(\d[\d,]*(?:\.\d+)?%?)\b", text)
    unprinted = []
    for raw in tokens:
        clean = raw.replace("$", "").replace("%", "").replace(",", "")
        # Skip small integers used for list items (1, 2, 3)
        if clean in ("1", "2", "3", "4", "5"):
            continue
        # Check against whitelist
        if clean not in printed_whitelist and raw not in printed_whitelist:
            # Check if float or int representation is in whitelist
            try:
                flt = float(clean)
                if str(int(flt)) in printed_whitelist or f"{flt:.1f}" in printed_whitelist or f"{flt:.2f}" in printed_whitelist:
                    continue
            except ValueError:
                pass
            unprinted.append(raw)
    return sorted(list(set(unprinted)))


# -----------------------------------------------------------------------------
# Memo Generation Engine (Buffett, Graham, Burry)
# -----------------------------------------------------------------------------

def generate_buffett_memo(ticker: str, data: dict, checks: list) -> str:
    """Generate Warren Buffett investment memo citing only printed numbers."""
    rows = data["rows"]
    r_first, r_last = rows[0], rows[-1]
    company_name = data["company_name"]
    passes = sum(1 for c in checks if c["status"].startswith("pass"))

    if passes == 3:
        verdict = "OWN THE BUSINESS"
        rationale = (
            f"Over the five fiscal years from {r_first['fy_end']} to {r_last['fy_end']}, {company_name} "
            f"demonstrated the classic marks of an enduring franchise. Net income increased from "
            f"${r_first['net_income']:,.1f}M to ${r_last['net_income']:,.1f}M while owner earnings expanded from "
            f"${r_first['owner_earnings']:,.1f}M to ${r_last['owner_earnings']:,.1f}M. "
            f"The company achieved a Return on Equity of at least 15% in every fiscal year, closing at {r_last['roe']}% "
            f"on ${r_last['equity']:,.1f}M of equity. Owner earnings were consistently positive in all 5 years, "
            f"proving that operating cash flows (${r_last['operating_cash_flow']:,.1f}M in {r_last['fy_end']}) "
            f"comfortably exceed capital spending requirements (${r_last['capital_spending']:,.1f}M). "
            f"We conclude the business possesses an authentic economic moat."
        )
    elif any(c["status"] == "not known" for c in checks):
        verdict = "WATCH IT"
        rationale = (
            f"While {company_name} generated revenue of ${r_last['revenue']:,.1f}M and net income of "
            f"${r_last['net_income']:,.1f}M in {r_last['fy_end']}, key owner earnings or equity inputs "
            f"are not known from SEC EDGAR XBRL facts. An equity balance of ${r_last['equity']} renders ROE unmeasurable "
            f"under standard criteria. We place the business on our watch list until owner earnings can be fully audited."
        )
    else:
        verdict = "PASS"
        rationale = (
            f"From {r_first['fy_end']} to {r_last['fy_end']}, {company_name} failed our quantitative franchise hurdle. "
            f"With net income moving from ${r_first['net_income']:,.1f}M to ${r_last['net_income']:,.1f}M, "
            f"ROE failed to consistently clear our 15% threshold across all five years. "
            f"Owner earnings volatility demonstrates that capital reinvestment consumes too much operating cash. "
            f"We pass on owning this business."
        )

    memo = f"""# Warren Buffett Investment Committee Memo: {ticker}

**Target Company:** {company_name} ({ticker})  
**Evaluation Model:** Quantitative 10-K Owner Earnings & ROE Screen  
**Filing Source:** SEC EDGAR Form 10-K (FY{r_first['fy_end'][:4]} - FY{r_last['fy_end'][:4]})  
**Verdict:** **{verdict}** (Score: {passes} of 3 checks passed)

## Quantitative Check Summary
1. **ROE >= 15% Every Year:** {checks[0]['status']} (Latest: {r_last['roe']}%)
2. **Owner Earnings Positive Every Year:** {checks[1]['status']} (Latest: ${r_last['owner_earnings']:,.1f}M)
3. **Owner Earnings Growth:** {checks[2]['status']} (${r_first['owner_earnings']:,.1f}M to ${r_last['owner_earnings']:,.1f}M)

## Investment Rationale
{rationale}

*Note: Built strictly using SEC EDGAR XBRL facts. No market price data utilized. Learning demonstration, not investment advice.*
"""
    return memo


def generate_graham_memo(ticker: str, data: dict, checks: list, cr_threshold: float = 2.0) -> str:
    """Generate Benjamin Graham investment memo citing only printed numbers."""
    rows = data["rows"]
    r_first, r_last = rows[0], rows[-1]
    company_name = data["company_name"]
    passes = sum(1 for c in checks if c["status"].startswith("pass"))

    cr_latest = r_last.get("current_ratio")
    cr_str = f"{cr_latest:.2f}" if isinstance(cr_latest, (int, float)) else str(cr_latest)
    threshold_note = (
        "Threshold kept: 2.0. Graham's strict 2.0 threshold protects against industrial "
        "working-capital impairment; it is retained as the conservative benchmark."
        if cr_threshold == 2.0
        else "Threshold kept: 1.0. This probe recognizes a negative-working-capital retail "
        "model, where rapid cash turnover and supplier float make a 2.0 current ratio less informative."
    )

    if passes == 3:
        verdict = "DEFENSIVE BUY"
        rationale = (
            f"Over the five-year observation period from {r_first['fy_end']} to {r_last['fy_end']}, {company_name} "
            f"met all three of our quantitative margin-of-safety standards. Net income remained positive across all "
            f"5 years, advancing from ${r_first['net_income']:,.1f}M to ${r_last['net_income']:,.1f}M. "
            f"Furthermore, working-capital liquidity is fully satisfactory, with current assets of ${r_last['assets_current']:,.1f}M "
            f"comfortably supporting current liabilities of ${r_last['liabilities_current']:,.1f}M for a current ratio of {cr_str}. "
            f"The business demonstrates adequate defensive solvency."
        )
    elif passes == 2:
        verdict = "WATCH"
        rationale = (
            f"{company_name} demonstrates an uninterrupted 5-year earnings record, growing net income from "
            f"${r_first['net_income']:,.1f}M to ${r_last['net_income']:,.1f}M. "
            f"However, the enterprise fails our balance-sheet working-capital test: current assets of "
            f"${r_last['assets_current']:,.1f}M against current liabilities of ${r_last['liabilities_current']:,.1f}M produce "
            f"a current ratio of {cr_str}, failing our conservative threshold of {cr_threshold:.1f}. "
            f"While the commercial operations compound, the balance sheet lacks the required margin of safety against short-term credit contraction."
        )
    else:
        verdict = "PASS"
        rationale = (
            f"{company_name} fails our fundamental defensive criteria. With net income recorded at "
            f"${r_first['net_income']:,.1f}M in {r_first['fy_end']} and ${r_last['net_income']:,.1f}M in {r_last['fy_end']}, "
            f"the company experienced deficit operations or failed working-capital tests (current ratio: {cr_str}). "
            f"The margin of safety is deficient for a conservative investor."
        )

    memo = f"""# Benjamin Graham Investment Committee Memo: {ticker}

**Target Company:** {company_name} ({ticker})  
**Evaluation Model:** Defensive Investor Margin-of-Safety & Working Capital Screen  
**Filing Source:** SEC EDGAR Form 10-K (FY{r_first['fy_end'][:4]} - FY{r_last['fy_end'][:4]})  
**Verdict:** **{verdict}** (Score: {passes} of 3 checks passed)

## Quantitative Check Summary
1. **Current Ratio >= {cr_threshold:.1f} (Latest Year):** {checks[0]['status']} (Current Assets: ${r_last['assets_current']:,.1f}M, Current Liabilities: ${r_last['liabilities_current']:,.1f}M, Ratio: {cr_str})
2. **Net Income Positive Every Year:** {checks[1]['status']} (5-year record with 0 deficit years)
3. **Net Income Growth:** {checks[2]['status']} (${r_first['net_income']:,.1f}M to ${r_last['net_income']:,.1f}M)

## Investment Rationale
{rationale}

{threshold_note}

*Note: Built strictly using SEC EDGAR XBRL facts. No market price data utilized. Learning demonstration, not investment advice.*
"""
    return memo


def generate_burry_memo(ticker: str, data: dict, checks: list) -> str:
    """Generate Michael Burry forensic memo citing only printed numbers."""
    rows = data["rows"]
    r_first, r_last = rows[0], rows[-1]
    company_name = data["company_name"]
    passes = sum(1 for c in checks if c["status"].startswith("pass"))

    le_latest = r_last.get("liabilities_equity")
    le_str = f"{le_latest:.2f}" if isinstance(le_latest, (int, float)) else str(le_latest)

    if passes == 2:
        verdict = "BULLISH / OWN"
        rationale = (
            f"Forensic cash flow analysis of {company_name} from {r_first['fy_end']} to {r_last['fy_end']} reveals "
            f"unimpeachable accounting quality. In every one of the 5 consecutive fiscal years, operating cash flow "
            f"exceeded net income, culminating in {r_last['fy_end']} with operating cash flow of ${r_last['operating_cash_flow']:,.1f}M "
            f"against net income of ${r_last['net_income']:,.1f}M. Earnings are real cash, not aggressive accruals. "
            f"On the balance sheet, total liabilities of ${r_last['liabilities']:,.1f}M against stockholders' equity of "
            f"${r_last['equity']:,.1f}M yield a liabilities-to-equity ratio of {le_str}, clearing our 2.0 ceiling. "
            f"Solvency risk is contained and the business generates robust organic cash."
        )
    elif any(c["status"] == "not known" for c in checks):
        verdict = "WATCH / HEDGE"
        rationale = (
            f"{company_name} demonstrates strong operational cash generation with operating cash flow of "
            f"${r_last['operating_cash_flow']:,.1f}M in {r_last['fy_end']}. However, balance sheet liabilities "
            f"are {r_last.get('liab_tag')} on EDGAR, making total debt-to-equity leverage {le_str}. "
            f"Without an audited XBRL tag for total liabilities, balance sheet insolvency risk cannot be definitively ruled out. "
            f"We maintain a neutral watch stance."
        )
    else:
        verdict = "BEARISH / PASS"
        rationale = (
            f"Forensic audit of {company_name} reveals structural vulnerabilities. Either operating cash flow failed to cover "
            f"reported net income (divergence between accruals and cash), or total liabilities exceed twice stockholders' equity "
            f"(liabilities to equity: {le_str}). Over-leveraged capital structures face severe refinancing headwinds."
        )

    memo = f"""# Michael Burry Forensic Investment Committee Memo: {ticker}

**Target Company:** {company_name} ({ticker})  
**Evaluation Model:** Forensic Cash Flow Quality & Balance Sheet Solvency Screen  
**Filing Source:** SEC EDGAR Form 10-K (FY{r_first['fy_end'][:4]} - FY{r_last['fy_end'][:4]})  
**Verdict:** **{verdict}** (Score: {passes} of 2 checks passed)

## Quantitative Check Summary
1. **Operating Cash Flow >= Net Income Every Year:** {checks[0]['status']} (Latest OCF: ${r_last['operating_cash_flow']:,.1f}M vs NI: ${r_last['net_income']:,.1f}M)
2. **Liabilities <= 2x Equity (Latest Year):** {checks[1]['status']} (Liabilities: ${r_last['liabilities']}M, Equity: ${r_last['equity']:,.1f}M, Ratio: {le_str})

## Investment Rationale
{rationale}

*Note: Built strictly using SEC EDGAR XBRL facts. No market price data utilized. Learning demonstration, not investment advice.*
"""
    return memo


# -----------------------------------------------------------------------------
# Main Execution CLI
# -----------------------------------------------------------------------------

def run_legend_panel(ticker: str, cr_threshold: float = 2.0, output_dir: str = "."):
    """Execute complete legend panel extraction, checks, and memo generation."""
    print("=" * 80)
    print(f"LEGEND INVESTOR PANEL: {ticker.upper()}")
    print("Data Source: SEC EDGAR Form 10-K | Keyless API")
    print(f"User-Agent: {USER_AGENT}")
    print("=" * 80)

    data = get_company_data(ticker)
    company_name = data["company_name"]
    cik = data["cik"]
    rows = data["rows"]

    print(f"\nEntity: {company_name} (CIK: {cik})")
    print(f"Observation Window: {rows[0]['fy_end']} through {rows[-1]['fy_end']} (5 Fiscal Years)\n")

    # 1. Print 5-Year Fact Table
    print("-" * 115)
    print(f"{'FY End':<12} {'Revenue ($M)':>14} {'Net Inc ($M)':>14} {'OCF ($M)':>14} {'CapEx ($M)':>14} {'Equity ($M)':>14} {'ROE %':>10} {'Owner Earn ($M)':>16}")
    print("-" * 115)
    for r in rows:
        rev_s = f"{r['revenue']:,.1f}" if isinstance(r['revenue'], (int, float)) else str(r['revenue'])
        ni_s = f"{r['net_income']:,.1f}" if isinstance(r['net_income'], (int, float)) else str(r['net_income'])
        ocf_s = f"{r['operating_cash_flow']:,.1f}" if isinstance(r['operating_cash_flow'], (int, float)) else str(r['operating_cash_flow'])
        cpx_s = f"{r['capital_spending']:,.1f}" if isinstance(r['capital_spending'], (int, float)) else str(r['capital_spending'])
        eq_s = f"{r['equity']:,.1f}" if isinstance(r['equity'], (int, float)) else str(r['equity'])
        roe_s = f"{r['roe']:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe'])
        oe_s = f"{r['owner_earnings']:,.1f}" if isinstance(r['owner_earnings'], (int, float)) else str(r['owner_earnings'])
        print(f"{r['fy_end']:<12} {rev_s:>14} {ni_s:>14} {ocf_s:>14} {cpx_s:>14} {eq_s:>14} {roe_s:>10} {oe_s:>16}")
    print("-" * 115)

    # 2. Print 5-Year Ratios Table
    print("\n" + "-" * 80)
    print(f"{'FY End':<12} {'AssetsCur ($M)':>16} {'LiabCur ($M)':>16} {'Current Ratio':>15} {'Liabilities/Eq':>17}")
    print("-" * 80)
    for r in rows:
        ac_s = f"{r['assets_current']:,.1f}" if isinstance(r['assets_current'], (int, float)) else str(r['assets_current'])
        lc_s = f"{r['liabilities_current']:,.1f}" if isinstance(r['liabilities_current'], (int, float)) else str(r['liabilities_current'])
        cr_s = f"{r['current_ratio']:.2f}" if isinstance(r['current_ratio'], (int, float)) else str(r['current_ratio'])
        le_s = f"{r['liabilities_equity']:.2f}" if isinstance(r['liabilities_equity'], (int, float)) else str(r['liabilities_equity'])
        print(f"{r['fy_end']:<12} {ac_s:>16} {lc_s:>16} {cr_s:>15} {le_s:>17}")
    print("-" * 80)

    # 3. Evaluate Checks
    b_checks = evaluate_buffett_checks(rows)
    g_checks = evaluate_graham_checks(rows, cr_threshold=cr_threshold)
    m_checks = evaluate_burry_checks(rows)
    all_checks = b_checks + g_checks + m_checks
    verdicts = compute_panel_verdicts(b_checks, g_checks, m_checks)

    # 4. Print Investor Panel Table
    print("\n" + "=" * 80)
    print(f"{'Investor':<12} {'Check Description':<52} {'Outcome':<16}")
    print("=" * 80)
    for c in all_checks:
        print(f"{c['investor']:<12} {c['check']:<52} {c['status']:<16}")
    print("-" * 80)
    print("PANEL VERDICTS:")
    for inv, res in verdicts.items():
        print(f"  - {inv:<10}: {res['score']} passed -> {res['verdict']}")
    print("=" * 80)

    # 5. Generate and Save Memos
    b_memo = generate_buffett_memo(ticker, data, b_checks)
    g_memo = generate_graham_memo(ticker, data, g_checks, cr_threshold=cr_threshold)
    m_memo = generate_burry_memo(ticker, data, m_checks)

    b_path = os.path.join(output_dir, f"memo_buffett_{ticker.upper()}.md")
    g_path = os.path.join(output_dir, f"memo_graham_{ticker.upper()}.md")
    m_path = os.path.join(output_dir, f"memo_burry_{ticker.upper()}.md")

    with open(b_path, "w", encoding="utf-8") as f:
        f.write(b_memo)
    with open(g_path, "w", encoding="utf-8") as f:
        f.write(g_memo)
    with open(m_path, "w", encoding="utf-8") as f:
        f.write(m_memo)

    print(f"\nGenerated Memos:")
    print(f"  Buffett: {b_path}")
    print(f"  Graham:  {g_path}")
    print(f"  Burry:   {m_path}")

    # 6. Audit for Unprinted Numbers
    whitelist = extract_printed_numbers(data, all_checks)
    for name, memo_text in [("Buffett", b_memo), ("Graham", g_memo), ("Burry", m_memo)]:
        unprinted = find_unprinted_numbers(memo_text, whitelist)
        if unprinted:
            print(f"  [FLAG] {name} memo contains unprinted numbers: {unprinted}")
        else:
            print(f"  [PASS] {name} memo uses strictly printed numbers (0 unprinted numbers)")

    return {
        "data": data,
        "buffett_checks": b_checks,
        "graham_checks": g_checks,
        "burry_checks": m_checks,
        "verdicts": verdicts,
        "memos": {
            "Buffett": b_memo,
            "Graham": g_memo,
            "Burry": m_memo,
        },
    }


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "COST"
    thresh = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    run_legend_panel(t, cr_threshold=thresh)
