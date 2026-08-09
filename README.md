# 📈 Groww Mutual Funds MCP Server

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![Model Context Protocol](https://img.shields.io/badge/MCP-1.0.0-orange.svg)](https://modelcontextprotocol.io)
[![FastMCP](https://img.shields.io/badge/FastMCP-Server-purple.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An intelligent, professional-grade **Model Context Protocol (MCP)** server that connects Claude (and other MCP-enabled AI assistants) directly to **Groww's live API**. 

When you ask your AI assistant for mutual fund recommendations or analysis (e.g., *"Show me the best Flexi Cap funds with high returns and moderate risk"*), the AI intelligently selects and applies multi-dimensional filters, queries Groww's backend in real time, and performs deep portfolio analysis to pick the best mutual funds for your needs.

---

## 🤖 How the AI Uses This MCP Server

Rather than manually browsing financial portals, your AI assistant autonomously handles fund discovery and analysis for you:

1. **Intelligent Query Interpretation**: You talk to Claude in plain natural language (e.g., *"Find top-rated equity mutual funds managed by Quant or PPFAS sorted by 3-year returns"*).
2. **Autonomous Filter Application**: Claude automatically translates your request into exact filter criteria defined in [filters.py](file:///d:/Projects/GROWW%20MCP/filters.py) and invokes the `search_mutual_funds` tool.
3. **Live Groww API Execution**: The MCP server connects directly to Groww's live production endpoints (`groww.in/v1/api`), fetching real-time data.
4. **Deep-Dive Fund Diagnostics**: To pick and analyze the best funds, Claude invokes `fetch_mutual_fund_details` to examine the fund's **top 10 holding companies**, **fund managers' experience & education**, **Sharpe/Sortino/Alpha/Beta risk metrics**, **CAGR vs category average**, **NAV**, **AUM**, **Expense Ratio**, and **Exit Load**.

---
## 📽️ Demo Video


https://github.com/user-attachments/assets/9c28dd77-0fd1-4947-a0bf-f7c50a4e5248





## 📸 Screenshots

### Real-Time Search & Deep-Dive Analysis
*Claude executing real-time screener queries and analyzing detailed metrics, portfolio holdings, risk parameters, and CAGR.*
<img width="875" height="1027" alt="screenzy-1786277257050" src="https://github.com/user-attachments/assets/93e35df2-711f-43ce-8b57-3a5dcab9798f" />


---

## 🔥 Key Capabilities

- **Direct Live Groww API Data**: Always returns real-time, production-grade financial data directly from Groww—no stale datasets or mock data.
- **Top 10 Portfolio Company Holdings**: Extracts the exact top companies invested in by the fund, along with sector allocation and corpus percentage (`corpus_percent`).
- **Fund Manager Profiling**: Fetches fund managers' full names, educational background, and total career experience.
- **Advanced Volatility & Risk Metrics**: Evaluates **Sharpe Ratio**, **Sortino Ratio**, **Alpha**, **Beta**, and **Standard Deviation** alongside scheme risk levels (`Low` to `Very High`).
- **CAGR & Benchmark Comparison**: Compares 1Y, 3Y, 5Y, and since-launch CAGR against the benchmark index and category average, plus 1Y/2Y/3Y SIP return calculations.
- **Clean LLM Optimization**: Raw API JSON responses are automatically pruned to remove UI clutter, saving token context while preserving essential analytical data.

---

## ⚙️ Filter Capabilities Available to AI

The AI dynamically applies these filter enums from [filters.py](file:///d:/Projects/GROWW%20MCP/filters.py) according to your prompt requirements:

- **Groww Verdict (`GrowwVerdict`)**: `TOP_BUY`, `BUY`, `HOLD`, `SELL`
- **Asset Categories (`AssetCategory`)**: `Equity`, `Debt`, `Hybrid`, `Commodities`
- **Sub-Categories (`SubCategory`)**:
  - *Equity*: `Flexi Cap`, `Large Cap`, `Mid Cap`, `Small Cap`, `Large & MidCap`, `Multi Cap`, `ELSS`, `Sectoral`, `Thematic`, `Value Oriented`, `International`
  - *Debt*: `Liquid`, `Corporate Bond`, `Banking and PSU`, `Credit Risk`, `Dynamic Bond`, `Gilt`, `Money Market`, `Overnight`, `Short Duration`, `Ultra Short Duration`, etc.
  - *Hybrid*: `Aggressive Hybrid`, `Arbitrage`, `Balanced Hybrid`, `Conservative Hybrid`, `Dynamic Asset Allocation`, `Equity Savings`, `Multi Asset Allocation`
  - *Commodities*: `Gold`, `Silver`
- **Risk Profile (`RiskLevel`)**: `Low`, `Moderately Low`, `Moderate`, `Moderately High`, `High`, `Very High`
- **Sorting Options (`SortOption`)**: Popularity (`3`), Prime Verdict (`10`), 1Y Returns (`4`), 3Y Returns (`0`), 5Y Returns (`5`)
- **AMC / Fund Houses (`FundHouse`)**: 50+ fund houses supported (e.g., `Axis Mutual Fund`, `HDFC Mutual Fund`, `SBI Mutual Fund`, `Quant Mutual Fund`, `PPFAS Mutual Fund`, `Mirae Asset Mutual Fund`, etc.)
- **Index Only**: Option to narrow results strictly to Index Funds.

---

## 🚀 Installation & Authentication

### 1. Clone the Repository
```bash
git clone https://github.com/codeterrayt/Mutual-Funds-Groww-MCP.git
cd Mutual-Funds-Groww-MCP
```

### 2. Configure Authentication in `auth.py`
Because live data is fetched directly from Groww's authenticated backend endpoints, you need to fill in your session credentials in [auth.py](file:///d:/Projects/GROWW%20MCP/auth.py).

1. Log into your account on [groww.in](https://groww.in).
2. Open **Developer Tools** in your browser (`F12` or `Ctrl + Shift + I`) and switch to the **Network** tab.
3. Search for any fund or refresh the page.
4. Select any network request to `groww.in/v1/api` and check the **Headers** section:
   - Copy the **`authorization`** header value (e.g., `Bearer eyJ...`).
   - Copy the **`cookie`** header value.
5. Open [auth.py](file:///d:/Projects/GROWW%20MCP/auth.py) and fill in your credentials:

```python
# auth.py
AUTHORIZATION_TOKEN = "Bearer eyJ....."
COOKIE = "dso.....;"
```

---

## 🔌 Registering with Claude Desktop

Register this MCP server in Claude Desktop's process configuration file so Claude can execute these tools.

### Claude Desktop Configuration Location
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### `claude_desktop_config.json` Snippet

#### Option 1: Using `uv` (Recommended)
`uv` will automatically manage dependencies using `pyproject.toml` and run the server.

```json
{
  "mcpServers": {
    "groww-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "d:/Projects/GROWW MCP",
        "run",
        "main.py"
      ]
    }
  }
}
```

#### Option 2: Using standard Python executable
If you prefer running using your python environment:

```json
{
  "mcpServers": {
    "groww-mcp": {
      "command": "d:/Projects/GROWW MCP/.venv/Scripts/python.exe",
      "args": [
        "d:/Projects/GROWW MCP/main.py"
      ]
    }
  }
}
```
*(Note: Replace `d:/Projects/GROWW MCP` with your local repository path, ensuring path slashes are written as `/`).*

After editing the config, **stop Claude From System Tray and restart Claude Desktop**. You will see the tools active in Claude Desktop.

<img width="2182" height="1128" alt="screenzy-1786276796934" src="https://github.com/user-attachments/assets/34e07f47-d1af-4a02-b037-dd2c3971edac" />

---

## 🛠️ MCP Tools Overview

### 1. `search_mutual_funds`
Searches and screens live mutual fund schemes from Groww based on criteria provided by the AI.
- **Parameters**: `groww_verdict`, `categories`, `sub_categories`, `index_only`, `fund_houses`, `risk_levels`, `sort_by`, `search_query`, `page`, `size`.

### 2. `fetch_mutual_fund_details`
Retrieves in-depth holdings, risk metrics, returns CAGR, and fund manager profiles using the fund's `search_id`.
- **Parameters**: `search_id` (e.g., `quant-small-cap-fund-direct-growth`).

---

## ⚖️ Disclaimer

*This project is an open-source tool for personal research and analysis. It is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Groww (groww.in).*

## 📄 License
This project is open-source software licensed under the MIT License.
