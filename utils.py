import uuid
from functools import lru_cache

@lru_cache(maxsize=1)
def get_v5_id() -> str:
    """
    Generates a UUID v5 without taking any parameters.
    Creates an internal random key on first call, caches it, 
    and returns the same UUID v5 on every subsequent call.
    """
    internal_seed = uuid.uuid4().hex
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, internal_seed))

def prune_mutual_fund_data(raw_data: dict) -> dict:
    """
    Takes raw Groww API JSON response data and returns a pruned,
    LLM-optimized dictionary stripping out UI bloat and noise.
    """
    content = raw_data.get("content", [])
    
    pruned_funds = [
        {
            "search_id": item.get("search_id") or item.get("id"),
            "scheme_name": item.get("scheme_name"),
            "fund_house": item.get("fund_house"),
            "fund_manager": item.get("fund_manager"),
            "category": item.get("category"),
            "sub_category": item.get("sub_category"),
            "risk": item.get("risk"),
            "aum_in_cr": round(item.get("aum"), 2) if item.get("aum") is not None else None,
            "groww_rating": item.get("groww_rating"),
            "groww_verdict": item.get("groww_verdict"),
            "groww_scheme_ranking": item.get("groww_scheme_ranking"),
            "min_sip": item.get("min_sip_investment"),
            "min_lumpsum": item.get("min_investment_amount"),
            "returns_pct": {
                "1y": item.get("return1y"),
                "3y": item.get("return3y"),
                "5y": item.get("return5y")
            },
            "codes": {
                "scheme_code": item.get("scheme_code"),
                "direct_scheme_code": item.get("direct_scheme_code")
            }
        }
        for item in content
    ]

    return {
        "total_results": raw_data.get("total_results", len(pruned_funds)),
        "funds": pruned_funds
    }


def extract_mutual_fund_details(data: dict, top_n_holdings: int = 10) -> dict:
    """
    Parses raw mutual fund scheme detail API response and extracts key financial,
    risk, performance, and operational metrics required for analysis.
    """
    if not data:
        return {}

    # Safely unpack sub-dictionaries/lists
    return_stats = data.get("return_stats", [{}])[0] if data.get("return_stats") else {}
    sip_returns = data.get("sip_return") or {}
    category_info = data.get("category_info") or {}
    rating_desc = data.get("groww_scheme_rating_description") or {}

    # Sort holdings descending by corpus_per and limit to top_n_holdings
    raw_holdings = data.get("holdings", [])
    sorted_holdings = sorted(
        raw_holdings,
        key=lambda x: x.get("corpus_per") or 0.0,
        reverse=True
    )[:top_n_holdings]

    holdings = [
        {
            "company_name": item.get("company_name"),
            "sector": item.get("sector_name"),
            "instrument": item.get("instrument_name"),
            "corpus_percent": round(item.get("corpus_per", 0), 2) if item.get("corpus_per") else 0.0,
        }
        for item in sorted_holdings
    ]

    # Extract fund managers
    managers = [
        {
            "name": mgr.get("person_name"),
            "education": mgr.get("education"),
            "experience": mgr.get("experience"),
        }
        for mgr in data.get("fund_manager_details", [])
    ]

    return {
        # Core Scheme Information
        "scheme_name": data.get("scheme_name"),
        "search_id": data.get("search_id"),
        "fund_house": data.get("fund_house"),
        "category": data.get("category"),
        "sub_category": data.get("sub_category"),
        "benchmark": data.get("benchmark"),
        "launch_date": data.get("launch_date"),
        "plan_type": data.get("plan_type"),
        "scheme_type": data.get("scheme_type"),
        "description": data.get("description"),

        # Verdict & Rating
        "groww_rating": data.get("groww_scheme_rating"),
        "groww_ranking": data.get("groww_scheme_ranking"),
        "verdict_remark": rating_desc.get("short_remark") if isinstance(rating_desc, dict) else None,

        # Key Financial Parameters
        "nav": data.get("nav"),
        "nav_date": data.get("nav_date"),
        "aum_cr": data.get("aum"),
        "expense_ratio": data.get("expense_ratio"),
        "exit_load": data.get("exit_load"),

        # Investment Thresholds
        "investment_limits": {
            "min_lumpsum": data.get("min_investment_amount"),
            "min_sip": data.get("min_sip_investment"),
            "min_additional": data.get("mini_additional_investment"),
            "min_withdrawal": data.get("min_withdrawal"),
        },

        # Risk & Volatility Metrics
        "risk_profile": {
            "risk_level": return_stats.get("risk") or data.get("nfo_risk"),
            "sharpe_ratio": return_stats.get("sharpe_ratio"),
            "sortino_ratio": return_stats.get("sortino_ratio"),
            "alpha": return_stats.get("alpha"),
            "beta": return_stats.get("beta"),
            "standard_deviation": return_stats.get("standard_deviation"),
        },

        # Performance Returns
        "returns": {
            "cagr": {
                "1y": return_stats.get("return1y"),
                "3y": return_stats.get("return3y"),
                "5y": return_stats.get("return5y"),
                "since_launch": return_stats.get("return_since_created"),
            },
            "category_average": {
                "1y": return_stats.get("cat_return1y"),
                "3y": return_stats.get("cat_return3y"),
                "5y": return_stats.get("cat_return5y"),
            },
            "sip_returns": {
                "1y": sip_returns.get("return1y"),
                "2y": sip_returns.get("return2y"),
                "3y": sip_returns.get("return3y"),
            },
        },

        # Tax Information
        "tax_impact": category_info.get("tax_impact"),

        # Management & Portfolio
        "top_holdings": holdings,
        "fund_managers": managers if managers else data.get("fund_manager"),
    }