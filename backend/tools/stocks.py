
from typing import Any, Dict
from langchain.tools import tool
import yfinance as yf
import pandas as pd
from pydantic import BaseModel
import functools

DATA_REGISTRY: Dict[str, Any] = {}


@functools.lru_cache(maxsize=None)  # Unlimited cache size
def _get_stock_history(ticker: str, period: str = "5d"):
    data = yf.Ticker(ticker).history(period=period)
    return data


@tool
def get_stock_price(ticker: str) -> str:
    """
    Get the latest stock price for a given ticker symbol.
    Args:
        ticker (str): The stock ticker symbol.
    Returns:
        str: The latest stock price.

    """
    data = _get_stock_history(ticker, "1d")
    if data.empty:
        return f"No data found for ticker symbol: {ticker}"
    latest_price = data['Close'].iloc[-1]
    return latest_price


@tool
def get_stock_history(ticker: str, period: str = "5d") -> Dict[str, Any]:
    """
    This tool MUST be used whenever the user asks for stock history.
    Never answer directly. Always call this tool.
    Args:
        ticker (str): The stock ticker symbol.
        period (str): The period over which to retrieve historical data (e.g., '1mo', '3mo', '1y').
    Returns:
        str: A JSON string containing stock_history and metadata.
    """

    print(f"Fetching history for {ticker} over period {period}")

    data = _get_stock_history(ticker, period)

    if data.empty:
        return f"No data found for ticker symbol: {ticker}"

    data.index = data.index.strftime('%Y-%m-%d')
    data = data.reset_index()
    # round numeric columns to 2 decimal places
    data["Close"] = data["Close"].round(2)

    data_key = f"{ticker}_{period}"
    DATA_REGISTRY[data_key] = data[['Date', 'Close']].to_dict(orient='records')

    history = data[['Date', 'Close']].head(3).to_dict(orient='records')

    metadata = {
        "ticker": ticker,
        "period": period,
        "data_points": len(history),
        "columns": ['Date', 'Close'],
        "data_key": data_key,
        "data_sample_for_reference": history
    }
    return metadata
