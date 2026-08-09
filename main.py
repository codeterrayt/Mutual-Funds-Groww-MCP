import warnings
from typing import List, Optional, Annotated
import httpx
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from filters import AssetCategory, FundHouse, RiskLevel, GrowwVerdict, SortOption, SubCategory
from growwroutes import GROWW_API_URL, IN_DETAIL_MUTUAL_FUND_FETCH_ROUTE, LIST_MUTUAL_FUNDS_ROUTE
from constants import API_TIMEOUT, GROWW_HEADERS, TOP_HOLDING_COMPANIES_LIMIT
from utils import extract_mutual_fund_details, prune_mutual_fund_data

warnings.filterwarnings("ignore")


mcp = FastMCP("GROWW MCP", host="0.0.0.0", port=8000)

@mcp.tool()
async def search_mutual_funds(
    groww_verdict: Annotated[
        Optional[List[GrowwVerdict]], 
        Field(description="Filter by Prime/Groww verdict ratings (TOP_BUY, BUY, HOLD, SELL).")
    ] = None,
    categories: Annotated[
        Optional[List[AssetCategory]], 
        Field(description="Broad asset category (Equity, Debt, Hybrid, Commodities).")
    ] = None,
    sub_categories: Annotated[
        Optional[List[SubCategory]], 
        Field(description="Specific sub-categories (Flexi Cap, Large Cap, Liquid, Gold, etc.).")
    ] = None,
    index_only: Annotated[
        bool, 
        Field(description="Toggle True to filter exclusively for Index Funds.")
    ] = False,
    fund_houses: Annotated[
        Optional[List[FundHouse]], 
        Field(description="Filter by one or more AMC Fund Houses.")
    ] = None,
    risk_levels: Annotated[
        Optional[List[RiskLevel]], 
        Field(description="Filter by scheme risk levels (Low to Very High).")
    ] = None,
    sort_by: Annotated[
        SortOption, 
        Field(description="Sort funds by Popularity ('3'), Prime Verdict ('10'), 1Y ('4'), 3Y ('0'), or 5Y Returns ('5').")
    ] = SortOption.POPULARITY,
    search_query: Annotated[
        Optional[str], 
        Field(description="Optional text query to match specific fund names.")
    ] = None,
    page: Annotated[
        int, 
        Field(description="Page number for pagination.")
    ] = 0,
    size: Annotated[
        int, 
        Field(description="Number of schemes to fetch per page.")
    ] = 10
) -> dict:
    """
    Search and filter mutual funds in real-time using Groww's live API endpoint.
    """
    params = [
        ("doc_type", "scheme"),
        ("plan_type", "Regular"),
        ("scheme_type", "Growth"),
        ("page", str(page)),
        ("size", str(size)),
        ("sort_by", sort_by.value if isinstance(sort_by, SortOption) else sort_by),
        ("index", "true" if index_only else "false")
    ]

    if groww_verdict:
        for verdict in groww_verdict:
            params.append(("groww_verdict", verdict.value))

    if categories:
        for cat in categories:
            params.append(("cat", cat.value))

    if sub_categories:
        for sub_cat in sub_categories:
            params.append(("sub_cat", sub_cat.value))

    if fund_houses:
        for fh in fund_houses:
            params.append(("fund_house", fh.value))

    if risk_levels:
        for risk in risk_levels:
            params.append(("risk", risk.value))

    if search_query:
        params.append(("q", search_query))

    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            response = await client.get(
                f"{GROWW_API_URL}{LIST_MUTUAL_FUNDS_ROUTE}",
                headers=GROWW_HEADERS,
                params=params
            )
            response.raise_for_status()
            return prune_mutual_fund_data(response.json())

    except httpx.HTTPStatusError as exc:
        return {
            "status": "error",
            "code": exc.response.status_code,
            "message": f"Groww API HTTP error: {exc.response.text}"
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Failed to connect to Groww API: {str(exc)}"
        }


@mcp.tool()
async def fetch_mutual_fund_details(
    search_id: Annotated[
        str, 
        Field(description="Unique search identifier for the mutual fund scheme (e.g., 'axis-silver-fof-regular-growth').")
    ]
) -> dict:
    """Fetch in-depth details of a specific mutual fund scheme using its search_id."""

    async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
        response = await client.get(
            f"{GROWW_API_URL}{IN_DETAIL_MUTUAL_FUND_FETCH_ROUTE}/{search_id}", 
            headers=GROWW_HEADERS, 
        )
        print(response)
        response.raise_for_status()
        return extract_mutual_fund_details(response.json(), TOP_HOLDING_COMPANIES_LIMIT)


if __name__ == "__main__":
    print("MCP is running..")
    mcp.run()


